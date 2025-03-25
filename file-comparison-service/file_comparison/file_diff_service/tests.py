import os
import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

class FileDiffServiceTestCase(TestCase):
    def setUp(self):
        """
        Set up test environment before each test method.
        """
        self.client = Client()
        
        self.temp_upload_dir = os.path.join(settings.BASE_DIR, 'temp_uploads')
        os.makedirs(self.temp_upload_dir, exist_ok=True)
        
        self.sample_file1 = SimpleUploadedFile(
            "file1.txt", 
            b"Hello, this is file 1 content\nLine 2 of file 1\nUnique to file 1", 
            content_type="text/plain"
        )
        self.sample_file2 = SimpleUploadedFile(
            "file2.txt", 
            b"Hello, this is different content\nLine 2 is also different\nUnique to file 2", 
            content_type="text/plain"
        )
        
        self.identical_file1 = SimpleUploadedFile(
            "identical1.txt", 
            b"This is an identical file content\nWith multiple lines", 
            content_type="text/plain"
        )
        self.identical_file2 = SimpleUploadedFile(
            "identical2.txt", 
            b"This is an identical file content\nWith multiple lines", 
            content_type="text/plain"
        )

    def test_index_page(self):
        """
        Test the index page rendering and initial file status
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
        self.assertIn('file1_exists', response.context)
        self.assertIn('file2_exists', response.context)

    def test_file_upload(self):
        """
        Test file upload functionality
        """
        file_data = {
            'file1': self.sample_file1,
            'file2': self.sample_file2
        }
        
        response = self.client.post(reverse('upload_files'), file_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Files uploaded successfully')
        
        file1_path = os.path.join(self.temp_upload_dir, 'file1.txt')
        file2_path = os.path.join(self.temp_upload_dir, 'file2.txt')
        self.assertTrue(os.path.exists(file1_path))
        self.assertTrue(os.path.exists(file2_path))

    def test_incomplete_file_upload(self):
        """
        Test file upload with missing files
        """
        response = self.client.post(reverse('upload_files'), {'file1': self.sample_file1})
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Both files are required')

    def test_show_differences(self):
        """
        Test difference calculation between two different files
        """
        file_data = {
            'file1': self.sample_file1,
            'file2': self.sample_file2
        }
        self.client.post(reverse('upload_files'), file_data)
        
        response = self.client.get(reverse('show_difference'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'difference.html')
        
        context = response.context
        self.assertIn('diff', context)
        self.assertIsNotNone(context['diff'])

    def test_identical_files_difference(self):
        """
        Test difference calculation for identical files
        """
        file_data = {
            'file1': self.identical_file1,
            'file2': self.identical_file2
        }
        self.client.post(reverse('upload_files'), file_data)
        
        response = self.client.get(reverse('show_difference'))
        
        self.assertEqual(response.status_code, 200)
        context = response.context
        
        self.assertIsNone(context['diff'])

    def test_promote_page(self):
        """
        Test promote page rendering
        """
        file_data = {
            'file1': self.sample_file1,
            'file2': self.sample_file2
        }
        self.client.post(reverse('upload_files'), file_data)
        
        response = self.client.get(reverse('promote_page'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promote.html')
        
        context = response.context
        self.assertIn('file1_content', context)
        self.assertIn('file2_content', context)

    def test_promote_file_content_overwrite(self):
        """
        Test content promotion with overwrite
        """
        file_data = {
            'file1': self.sample_file1,
            'file2': self.sample_file2
        }
        self.client.post(reverse('upload_files'), file_data)
        
        promote_data = {
            'source_file': 'file1.txt',
            'target_file': 'file2.txt',
            'merge_type': 'overwrite'
        }
        response = self.client.post(reverse('promote_file_content'), promote_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Content overwrited successfully')

    def test_promote_file_content_merge(self):
        """
        Test content promotion with merge
        """
        file_data = {
            'file1': self.sample_file1,
            'file2': self.sample_file2
        }
        self.client.post(reverse('upload_files'), file_data)
        
        promote_data = {
            'source_file': 'file1.txt',
            'target_file': 'file2.txt',
            'merge_type': 'merge'
        }
        response = self.client.post(reverse('promote_file_content'), promote_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Content merged successfully')

    def test_no_files_uploaded(self):
        """
        Test routes when no files are uploaded
        """
        diff_response = self.client.get(reverse('show_difference'))
        self.assertTemplateUsed(diff_response, 'difference.html')
        self.assertIn('error', diff_response.context)

        promote_response = self.client.get(reverse('promote_page'))
        self.assertEqual(promote_response.status_code, 404)

    def tearDown(self):
        """
        Clean up temporary files after tests
        """
        for filename in os.listdir(self.temp_upload_dir):
            file_path = os.path.join(self.temp_upload_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")