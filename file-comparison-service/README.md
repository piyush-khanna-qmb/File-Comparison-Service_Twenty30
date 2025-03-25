AUTHOR: Piyush Khanna
DATED: 26/03/2025 - 2:55AM  IST
FUNCTIONALITY: Readme file for the running and testing the Take-Home test webapp, named file-comparison-app, as assigned by Mr. Varun Kapoor from Twenty30 Health on 24/03/2025.

__________________________________________________________________________

DOCKER SETUP

# Create directory where you want to pull docker image
mkdir Docker-Test
cd Docker-Test

# Pull the image from dockerhub using below given command
docker pull piyushkhannadev/file-comparison-app:latest
docker run -p 8000:8000 piyushkhannadev/file-comparison-app

# Open up browser and enter the url to access application:
http://localhost:8000/

__________________________________________________________________________

APPLICATION USAGE

# Upload two files each using the file selector

# Press 'Upload Files' button to upload those files to the server. 
. 'Current Files' indicates the presence of files on server
. After pressing upload, the options to check difference or promote will be enabled

# Check Difference
. This hits the /difference route and shows the difference between both files.
(The process may take some while for files larger than 3MB)

# Promote Content
. This hits the /promote route and opens up a page which shows a snippet of both the files and provides option to swap the file that will be overwritten/merged.
. Press the 'Merge File' button to copy and merge the content of file1 into file2.
. Press the 'Overwrite Target' button to overwrite the contents of file2 with that of file1

__________________________________________________________________________

TESTING AND COVERAGE REPORT GENERATION

# cd into the directory which contains the image

# Run the following command to test the app
docker run -it piyushkhannadev/file-comparison-app /bin/bash

# Once inside the container:
coverage run manage.py test
coverage report
