import os
import logging
import difflib
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)

# Temporary upload directory
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'temp_uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

def index(request):
    """
    Main index page for file upload and management
    """
    # Check if files exist from previous upload
    file1_path = os.path.join(UPLOAD_DIR, 'file1.txt')
    file2_path = os.path.join(UPLOAD_DIR, 'file2.txt')
    
    context = {
        'file1_exists': os.path.exists(file1_path),
        'file2_exists': os.path.exists(file2_path)
    }
    return render(request, 'index.html', context)

@csrf_exempt
def upload_files(request):
    """Handle file uploads."""
    if request.method == 'POST':
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        
        if not file1 or not file2:
            return JsonResponse({'error': 'Both files are required'}, status=400)
        
        try:
            # Save files with predictable names
            file1_path = os.path.join(UPLOAD_DIR, 'file1.txt')
            file2_path = os.path.join(UPLOAD_DIR, 'file2.txt')
            
            # Write files
            with open(file1_path, 'wb+') as destination:
                for chunk in file1.chunks():
                    destination.write(chunk)
            
            with open(file2_path, 'wb+') as destination:
                for chunk in file2.chunks():
                    destination.write(chunk)
            
            return JsonResponse({
                'message': 'Files uploaded successfully',
                'file1': file1_path,
                'file2': file2_path
            })
        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            return JsonResponse({'error': f'File upload failed: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def show_difference(request):
    """
    Show differences between the two uploaded files
    """
    file1_path = os.path.join(UPLOAD_DIR, 'file1.txt')
    file2_path = os.path.join(UPLOAD_DIR, 'file2.txt')
    
    # Check if files exist
    if not (os.path.exists(file1_path) and os.path.exists(file2_path)):
        return render(request, 'difference.html', {
            'error': 'Files not found. Please upload files first.'
        })
    
    try:
        # Read file contents with error handling for encoding
        try:
            with open(file1_path, 'r', encoding='utf-8') as f1, \
                 open(file2_path, 'r', encoding='utf-8') as f2:
                file1_lines = f1.readlines()
                file2_lines = f2.readlines()
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding if UTF-8 fails
            with open(file1_path, 'r', encoding='latin-1') as f1, \
                 open(file2_path, 'r', encoding='latin-1') as f2:
                file1_lines = f1.readlines()
                file2_lines = f2.readlines()
        
        # Use difflib to generate differences
        diff = list(difflib.unified_diff(
            file1_lines, 
            file2_lines, 
            fromfile='File 1', 
            tofile='File 2'
        ))
        
        context = {
            'diff': diff if diff else None,
            'file1_name': 'file1.txt',
            'file2_name': 'file2.txt'
        }
        return render(request, 'difference.html', context)
    
    except Exception as e:
        logger.error(f"Difference calculation error: {str(e)}")
        return render(request, 'difference.html', {
            'error': f'Error calculating differences: {str(e)}'
        })

def promote_page(request):
    """
    Render the promote page with file contents
    """
    file1_path = os.path.join(UPLOAD_DIR, 'file1.txt')
    file2_path = os.path.join(UPLOAD_DIR, 'file2.txt')
    
    # Check if files exist
    if not (os.path.exists(file1_path) and os.path.exists(file2_path)):
        return JsonResponse({'error': 'Files not found. Please upload files first.'}, status=404)
    
    try:
        with open(file1_path, 'r', encoding='utf-8') as f1, \
             open(file2_path, 'r', encoding='utf-8') as f2:
            file1_content = f1.read(500)
            file2_content = f2.read(500)
        
        context = {
            'file1_name': 'file1.txt',
            'file2_name': 'file2.txt',
            'file1_content': file1_content + ('...' if len(file1_content) == 500 else ''),
            'file2_content': file2_content + ('...' if len(file2_content) == 500 else '')
        }
        return render(request, 'promote.html', context)
    
    except Exception as e:
        logger.error(f"Promote page error: {str(e)}")
        return JsonResponse({'error': f'Error preparing promote page: {str(e)}'}, status=500)

@csrf_exempt
def promote_file_content(request):
    """Promote content from one file to another."""
    if request.method == 'POST':
        source_file = request.POST.get('source_file', 'file1.txt')
        target_file = request.POST.get('target_file', 'file2.txt')
        merge_type = request.POST.get('merge_type', 'overwrite')
        
        # Construct full file paths
        source_path = os.path.join(UPLOAD_DIR, source_file)
        target_path = os.path.join(UPLOAD_DIR, target_file)
        
        # Check if files exist
        if not (os.path.exists(source_path) and os.path.exists(target_path)):
            return JsonResponse({'error': 'Files not found. Please upload files first.'}, status=404)
        
        try:
            # Read source and target file contents
            with open(source_path, 'r', encoding='utf-8') as src, \
                 open(target_path, 'r', encoding='utf-8') as tgt:
                source_content = src.read()
                target_content = tgt.read()
            
            # Determine final content based on merge type
            if merge_type == 'overwrite':
                final_content = source_content
            else:  # merge
                final_content = target_content + "\n" + source_content
            
            # Write back to target file
            with open(target_path, 'w', encoding='utf-8') as tgt:
                tgt.write(final_content)
            
            return JsonResponse({
                'message': f'Content {merge_type}d successfully',
                'target_file': target_file
            })
        except Exception as e:
            logger.error(f"Content promotion error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)