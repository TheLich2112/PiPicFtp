README for Timelapse Automation with Raspberry Pi

Created by Marcus Hazel-McGown - MM0ZIF https://mm0zif.radio
this project is beerware, if you like it donate a beer!

Overview
This project is a Python-based timelapse automation tool designed for Raspberry Pi, using the PiCamera and FTP for remote storage. The script captures images at regular intervals, organizes them into daily folders, and uploads the previous day's images as a compressed ZIP file to a remote FTP server.

Features
Automatically captures images every 5 minutes.
Organizes captured images into date-specific folders.
Compresses the previous day's folder into a ZIP file.
Uploads ZIP files to a remote FTP server (e.g., DriveHQ).
Logs operations and errors for debugging and tracking.
Requirements
Hardware: Raspberry Pi with a camera module (e.g., PiCamera v1 or v2).
Software:
Python 3.7 or higher.
Required Python libraries:
picamera2
schedule
shutil
ftplib
logging
Install dependencies via pip:

bash
Copy code
pip install picamera2 schedule
Setup
Clone the Repository:

bash
Copy code
git clone <repository_url>
cd <repository_folder>
Update Configuration:

Open the script file (timelapse_script.py) and update the following constants as needed:
FTP_HOST: Your FTP server address.
FTP_USER: Your FTP username.
FTP_PASS: Your FTP password.
BASE_FOLDER: Directory to save images locally (default: /home/marcus/pi/timelapse).
Make the Script Executable:

bash
Copy code
chmod +x timelapse_script.py
Run the Script:

bash
Copy code
python3 timelapse_script.py
Folder Structure
Captured images and compressed archives are organized as follows:

yaml
Copy code
/home/pi/timelapse/
    ├── 2024-12-05/
    │   ├── image_00-00-00.jpg
    │   ├── image_00-05-00.jpg
    │   └── ...
    ├── 2024-12-06/
    │   ├── image_00-00-00.jpg
    │   ├── image_00-05-00.jpg
    │   └── ...
Usage
Image Capture:
The script captures images every 5 minutes and saves them to folders named by date.
Midnight Processing:
At midnight, the script compresses the previous day's folder into a ZIP file and uploads it to the configured FTP server.
The original folder and ZIP file are deleted after successful upload.
Error Handling and Logging
Logs are stored in timelapse.log for tracking:

Successful Operations:
Captured images.
Created ZIP files.
Uploaded ZIP files.
Errors:
FTP upload failures.
Camera initialization errors.
File operation issues.
Customization
Capture Interval: Modify the interval between image captures by changing the time.sleep(300) value in the capture_image loop. For example, use time.sleep(600) for a 10-minute interval.

Upload Schedule: Change the scheduled task time for midnight processing by updating:

python
Copy code
schedule.every().day.at("00:00").do(zip_and_upload_previous_day)
Storage Location: Update the BASE_FOLDER path to change where images are saved locally.

Stopping the Script
To stop the script, press Ctrl+C in the terminal. The script will log this action.

Known Issues
Ensure the Raspberry Pi has sufficient storage for images until the midnight cleanup process.
Verify that the FTP server has enough space and supports large file uploads if daily ZIP files are large.
Future Enhancements
Add support for cloud storage services (e.g., Google Drive, AWS S3).
Add email or notification alerts for upload successes or failures.
Implement dynamic capture intervals based on lighting conditions.
