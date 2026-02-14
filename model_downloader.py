import os
import urllib.request
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_google_drive_link(url):
    """Convert Google Drive share link to direct download link"""
    if 'drive.google.com' in url and '/file/d/' in url:
        file_id = url.split('/file/d/')[1].split('/')[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        logger.info(f"Downloading {destination.name}...")
        urllib.request.urlretrieve(url, destination)
        logger.info(f"✓ Successfully downloaded {destination.name}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to download {destination.name}: {e}")
        return False

def ensure_models_exist():
    """Download model files if they don't exist"""
    base_dir = Path(__file__).parent
    model_dir = base_dir / "segmentation" / "documents-segment-classification-main" / "yolo-coco"
    model_dir.mkdir(parents=True, exist_ok=True)
    
    models = {
        "yolov8.weights": os.getenv("YOLO_WEIGHTS_URL", ""),
        "yolov8.cfg": os.getenv("YOLO_CFG_URL", ""),
        "classes.names": os.getenv("YOLO_CLASSES_URL", "")
    }
    
    all_downloaded = True
    
    for filename, url in models.items():
        filepath = model_dir / filename
        
        if filepath.exists():
            logger.info(f"✓ {filename} already exists")
            continue
        
        if not url:
            logger.warning(f"⚠ {filename} not found and no URL provided")
            all_downloaded = False
            continue
        
        # Convert Google Drive link if needed
        download_url = convert_google_drive_link(url)
        
        if not download_file(download_url, filepath):
            all_downloaded = False
    
    if not all_downloaded:
        logger.warning("Some model files are missing. The application may not work correctly.")
    
    return all_downloaded

if __name__ == "__main__":
    ensure_models_exist()

