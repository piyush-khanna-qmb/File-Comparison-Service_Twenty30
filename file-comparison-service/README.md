# File Comparison App - README

**Author**: Piyush Khanna  
**Date**: 26/03/2025 - 2:55 AM IST  
**Functionality**: This README provides instructions on how to run and test the *file-comparison-app*, a Take-Home web app assignment from Mr. Varun Kapoor at Twenty30 Health, assigned on 24/03/2025.

---

## Docker Setup

Follow these steps to run the app using Docker.

### 1. Create a Directory for Docker Image

```bash
mkdir Docker-Test
cd Docker-Test
```

### 2. Pull the Docker Image

Run the following command to pull the latest image from Docker Hub:

```bash
docker pull piyushkhannadev/file-comparison-app:latest
```

### 3. Run the Docker Container

To run the application, use the command:

```bash
docker run -p 8000:8000 piyushkhannadev/file-comparison-app
```

### 4. Access the Application

Open your web browser and visit the following URL to access the application:

```
http://localhost:8000/
```

---

## Application Usage

### 1. Upload Files

- Use the file selector to upload two files.
- Press the **"Upload Files"** button to upload the selected files to the server. 
- The **"Current Files"** section will show the files currently present on the server.
- After uploading, options to check the difference or promote the files will be enabled.

### 2. Check Difference

- Press **"Check Difference"** to compare the files. 
- This will hit the `/difference` route and display the differences between the two files.
  - Note: The process may take some time for files larger than 3MB.

### 3. Promote Content

- Press **"Promote Content"** to open a page showing snippets of both files.
- Here, you can choose which file will be overwritten or merged.
  - **"Merge File"**: Merges the content of file1 into file2.
  - **"Overwrite Target"**: Overwrites the content of file2 with file1's content.

---

## Testing and Coverage Report Generation

### 1. Access the Container

To run tests and generate coverage reports, follow these steps:

```bash
docker run -it piyushkhannadev/file-comparison-app /bin/bash
```

### 2. Run Tests

Once inside the container, run the following commands to execute tests and generate a coverage report:

```bash
coverage run manage.py test
coverage report
```

---

**End of README**  
Feel free to reach out for any clarifications or issues.