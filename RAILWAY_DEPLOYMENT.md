# Railway Deployment Guide with Cloud Storage

This guide will walk you through deploying your application to Railway with model files stored in cloud storage.

## Step 1: Upload Model Files to Cloud Storage

You need to upload these 3 files:
- `yolov8.weights`
- `yolov8.cfg`
- `classes.names`

### Option A: Google Drive (Recommended - Easiest)

1. **Upload files to Google Drive**
   - Go to https://drive.google.com
   - Create a folder called "ACCASM-Models" (or any name)
   - Upload your 3 model files to this folder

2. **Get shareable links for each file**
   - Right-click on each file → "Get link"
   - Set permission to "Anyone with the link"
   - Copy the link (looks like: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`)

3. **Convert to direct download links**
   - Extract the FILE_ID from the link (the long string between `/d/` and `/view`)
   - Format: `https://drive.google.com/uc?export=download&id=FILE_ID`
   
   **Example:**
   - Share link: `https://drive.google.com/file/d/1ABC123xyz789/view?usp=sharing`
   - Direct download: `https://drive.google.com/uc?export=download&id=1ABC123xyz789`

### Option B: Dropbox

1. Upload files to Dropbox
2. Right-click → Copy link
3. Convert link:
   - Replace `www.dropbox.com` with `dl.dropboxusercontent.com`
   - Replace `?dl=0` with `?dl=1`
   
   **Example:**
   - Share link: `https://www.dropbox.com/s/abc123/file.weights?dl=0`
   - Direct download: `https://dl.dropboxusercontent.com/s/abc123/file.weights?dl=1`

### Option C: GitHub Releases

1. Go to your GitHub repository
2. Create a new release (Releases → Draft a new release)
3. Upload model files as release assets
4. Use direct URLs: `https://github.com/username/repo/releases/download/v1.0/filename`

## Step 2: Push Code to GitHub

Make sure all your code is committed and pushed:

```bash
git add .
git commit -m "Add model downloader for Railway deployment"
git push origin main
```

## Step 3: Deploy to Railway

### 3.1 Create Railway Account and Project

1. Go to https://railway.app
2. Sign up/Login (you can use GitHub to sign in)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Authorize Railway to access your GitHub
6. Select your repository: `ACCASM_MINI_PROJECT`
7. Railway will automatically start deploying

### 3.2 Configure Environment Variables

In Railway dashboard:

1. Click on your service
2. Go to "Variables" tab
3. Click "New Variable" and add each of these:

```
GROQ_API_KEY=your-groq-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-generated-secret-key-here
YOLO_WEIGHTS_URL=https://drive.google.com/uc?export=download&id=YOUR_WEIGHTS_FILE_ID
YOLO_CFG_URL=https://drive.google.com/uc?export=download&id=YOUR_CFG_FILE_ID
YOLO_CLASSES_URL=https://drive.google.com/uc?export=download&id=YOUR_CLASSES_FILE_ID
PORT=5002
```

**Important:**
- Replace `YOUR_WEIGHTS_FILE_ID` with the actual file ID from your Google Drive link
- Replace `YOUR_CFG_FILE_ID` with the actual file ID for yolov8.cfg
- Replace `YOUR_CLASSES_FILE_ID` with the actual file ID for classes.names
- Generate SECRET_KEY using: `python -c "import secrets; print(secrets.token_hex(32))"`

### 3.3 Monitor Deployment

1. Go to "Deployments" tab in Railway
2. Watch the build logs
3. Look for messages like:
   - "Downloading yolov8.weights..."
   - "✓ Successfully downloaded yolov8.weights"
   - "Application initialized successfully"

### 3.4 Get Your Application URL

1. Once deployed, Railway will provide a URL
2. Click "Settings" → "Generate Domain" to get a custom domain
3. Your app will be live at: `https://your-app-name.up.railway.app`

## Step 4: Verify Deployment

1. **Visit your Railway URL**
   - Should see your homepage

2. **Check logs for model download**
   - Go to Railway dashboard → Deployments → View logs
   - Should see successful model downloads

3. **Test PDF upload**
   - Upload a test PDF
   - Verify processing works

## Troubleshooting

### Models Not Downloading

**Check:**
- URLs are correct in environment variables
- Files are accessible (test URLs in browser)
- Check Railway logs for specific errors

**Fix:**
- Verify Google Drive links are set to "Anyone with the link"
- Make sure file IDs are correct
- Try downloading manually to verify URLs work

### Application Crashes on Startup

**Check logs for:**
- Missing environment variables
- Model file download failures
- Import errors

**Common fixes:**
- Ensure all environment variables are set
- Verify API keys are correct
- Check that model URLs are accessible

### Timeout Errors

**If PDF processing times out:**
- Railway timeout is set to 600 seconds (10 minutes)
- For very large PDFs, consider:
  - Splitting PDFs into smaller chunks
  - Using async processing (future enhancement)

### Memory Issues

**If you get memory errors:**
- Railway free tier has memory limits
- Consider upgrading to Railway Pro plan
- Or optimize model loading

## Post-Deployment Checklist

- [ ] All environment variables set correctly
- [ ] Model files downloaded successfully (check logs)
- [ ] Application accessible via Railway URL
- [ ] Homepage loads correctly
- [ ] PDF upload works
- [ ] Processing completes successfully
- [ ] Results display correctly

## Next Steps

Once deployed:
1. Test with various PDF sizes
2. Monitor Railway dashboard for resource usage
3. Set up custom domain (optional)
4. Configure auto-deployments from GitHub (already enabled)

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check Railway logs for detailed error messages

