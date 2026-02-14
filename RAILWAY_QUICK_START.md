# Railway Quick Start - Step by Step

## What You Need to Do

### 1. Upload Model Files (5 minutes)

**Upload these 3 files to Google Drive:**
- `yolov8.weights` (large file, ~250MB)
- `yolov8.cfg` (small file)
- `classes.names` (small file)

**Steps:**
1. Go to https://drive.google.com
2. Create a folder "ACCASM-Models"
3. Upload the 3 files
4. For each file:
   - Right-click → "Get link"
   - Set to "Anyone with the link"
   - Copy the link
   - Extract the FILE_ID (the long string between `/d/` and `/view`)
   - Save it - you'll need it for Railway

**Example:**
- Link: `https://drive.google.com/file/d/1ABC123xyz789/view?usp=sharing`
- FILE_ID: `1ABC123xyz789`
- Direct URL: `https://drive.google.com/uc?export=download&id=1ABC123xyz789`

### 2. Get API Keys (2 minutes)

- **Groq API Key**: https://console.groq.com/ → Create API Key
- **Gemini API Key**: https://makersuite.google.com/app/apikey → Create API Key
- **Secret Key**: Run this command:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

### 3. Push to GitHub (1 minute)

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 4. Deploy on Railway (5 minutes)

1. Go to https://railway.app
2. Sign up (use GitHub login)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Wait for initial deployment

### 5. Set Environment Variables (3 minutes)

In Railway dashboard → Your Service → Variables:

Add these 7 variables:

```
GROQ_API_KEY=your-actual-groq-key
GEMINI_API_KEY=your-actual-gemini-key
SECRET_KEY=your-generated-secret-key
YOLO_WEIGHTS_URL=https://drive.google.com/uc?export=download&id=YOUR_WEIGHTS_ID
YOLO_CFG_URL=https://drive.google.com/uc?export=download&id=YOUR_CFG_ID
YOLO_CLASSES_URL=https://drive.google.com/uc?export=download&id=YOUR_CLASSES_ID
PORT=5002
```

**Replace:**
- `YOUR_WEIGHTS_ID` with the FILE_ID from yolov8.weights
- `YOUR_CFG_ID` with the FILE_ID from yolov8.cfg
- `YOUR_CLASSES_ID` with the FILE_ID from classes.names

### 6. Redeploy (automatic)

Railway will automatically redeploy when you add environment variables.

### 7. Test (2 minutes)

1. Get your Railway URL (Settings → Generate Domain)
2. Visit the URL
3. Upload a test PDF
4. Verify it works!

## Total Time: ~20 minutes

## Need Help?

Check `RAILWAY_DEPLOYMENT.md` for detailed instructions and troubleshooting.

