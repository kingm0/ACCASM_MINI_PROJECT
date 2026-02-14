# Model Files Setup

## Important: Model Files Not Included in Repository

Due to GitHub's file size limits, the following model files are **NOT** included in this repository:

### Required Model Files:

1. **YOLO Model Files** (Required for PDF segmentation):
   - `segmentation/documents-segment-classification-main/yolo-coco/yolov8.weights`
   - `segmentation/documents-segment-classification-main/yolo-coco/yolov8.cfg`
   - `segmentation/documents-segment-classification-main/yolo-coco/classes.names`

2. **StructEqTable Model** (If using table processing):
   - `U4R/StructTable-InternVL2-1B/` (checkpoint files)

### How to Get Model Files:

#### Option 1: Download from Original Sources
- YOLO weights: Download from the original YOLO repository or training source
- StructEqTable: Follow instructions in `StructEqTable-Deploy/README.md`

#### Option 2: Use Git LFS (Recommended for Large Files)
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.weights"
git lfs track "*.cfg"
git lfs track "*.pt"

# Add and commit
git add .gitattributes
git commit -m "Add Git LFS tracking for model files"
```

#### Option 3: External Storage
Store model files in:
- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Or any cloud storage service

Then download them during deployment or at runtime.

### For Deployment:

1. **Local Development**: Place model files in the correct directories as specified in the code
2. **Cloud Deployment**: 
   - Upload model files to cloud storage
   - Download them during deployment (in Dockerfile or startup script)
   - Or mount them as volumes in Docker

### Example Dockerfile Addition:

```dockerfile
# Download model files during build
RUN mkdir -p segmentation/documents-segment-classification-main/yolo-coco
RUN curl -L "YOUR_MODEL_URL" -o segmentation/documents-segment-classification-main/yolo-coco/yolov8.weights
```

### Example Runtime Download:

```python
import os
import urllib.request

def download_model_if_needed():
    model_path = "segmentation/documents-segment-classification-main/yolo-coco/yolov8.weights"
    if not os.path.exists(model_path):
        print("Downloading model file...")
        urllib.request.urlretrieve("YOUR_MODEL_URL", model_path)
```

