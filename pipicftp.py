from datetime import datetime, timedelta
import os
import shutil
from ftplib import FTP
import logging
import time
from picamera2 import Picamera2

# Constants
FTP_HOST = "IP-of-ftp"
FTP_USER = "Username"
FTP_PASS = "Password"
BASE_FOLDER = "/home/username/pi/timelapse"

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
        logging.info("Initializing Picamera2")
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (1920, 1080)})
        logging.info("Configuring camera")
        picam2.configure(config)
        logging.info("Starting camera")
        picam2.start()
        time.sleep(2)  # Give the camera time to initialize
        logging.info(f"Capturing image to {file_name}")
        picam2.capture_file(file_name)
        picam2.stop()
        logging.info(f"Image captured successfully: {file_name}")
    except Exception as e:
        logging.error(f"Failed to capture image: {e}")
    finally:
        picam2.close()  # Ensure the camera is properly closed

if __name__ == "__main__":
    try:
        while True:
            start_time = time.time()  # Record the start time
            capture_image()           # Capture the image
            elapsed_time = time.time() - start_time
            logging.info(f"Capture completed in {elapsed_time:.2f} seconds")
            
            # Calculate remaining time to maintain a 5-minute interval
            sleep_time = max(0, 300 - elapsed_time)
            logging.info(f"Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
