from picamera2 import Picamera2
from datetime import datetime, timedelta
import os
import shutil
from ftplib import FTP
import logging
import schedule
import time

# Constants
FTP_HOST = "66.220.9.50"
FTP_USER = "daLich"
FTP_PASS = "Type0Neg1024!"
BASE_FOLDER = "/home/marcus/pi/timelapse"

# Configure logging
logging.basicConfig(
    filename="timelapse.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def upload_to_drivehq(zip_file):
    """Uploads a zip file to the DriveHQ FTP server."""
    try:
        with FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            with open(zip_file, 'rb') as file:
                ftp.storbinary(f'STOR {os.path.basename(zip_file)}', file)
        logging.info(f"Successfully uploaded: {zip_file}")
    except Exception as e:
        logging.error(f"Failed to upload {zip_file}: {e}")

def zip_and_upload_previous_day():
    """Zips and uploads the previous day's folder."""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    folder_path = os.path.join(BASE_FOLDER, yesterday)
    
    if os.path.exists(folder_path):
        try:
            # Create zip file
            zip_path = shutil.make_archive(folder_path, 'zip', folder_path)
            logging.info(f"Created zip file: {zip_path}")
            
            # Upload to DriveHQ
            upload_to_drivehq(zip_path)
            
            # Cleanup
            shutil.rmtree(folder_path)
            os.remove(zip_path)
            logging.info(f"Cleaned up folder and zip file for: {yesterday}")
        except Exception as e:
            logging.error(f"Error zipping or cleaning up: {e}")
    else:
        logging.warning(f"No folder found for {yesterday} to zip and upload.")

def capture_image():
    """Captures an image and saves it to a date-specific folder."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(BASE_FOLDER, current_date)
    os.makedirs(folder_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%H-%M-%S")
    file_name = os.path.join(folder_path, f"image_{timestamp}.jpg")
    
    try:
        camera = Picamera2()
        config = camera.create_still_configuration()
        camera.configure(config)
        camera.start()
        time.sleep(2)  # Allow the camera to stabilize
        camera.capture_file(file_name)
        camera.close()
        logging.info(f"Captured image: {file_name}")
    except Exception as e:
        logging.error(f"Failed to capture image: {e}")

def schedule_tasks():
    """Schedules tasks for midnight processing."""
    schedule.every().day.at("00:00").do(zip_and_upload_previous_day)
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to reduce CPU usage

if __name__ == "__main__":
    # Start capturing images in a separate loop
    try:
        while True:
            capture_image()
            time.sleep(300)  # Wait 5 minutes between captures
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
