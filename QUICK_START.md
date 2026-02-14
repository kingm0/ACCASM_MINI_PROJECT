# Quick Start Deployment Guide

## 🚀 Fastest Deployment Options

### Option 1: Railway (Easiest - Recommended for Beginners)

1. **Sign up** at [railway.app](https://railway.app)
2. **Create new project** → "Deploy from GitHub repo"
3. **Connect your repository**
4. **Add environment variables** in Railway dashboard:
   - `GROQ_API_KEY` - Your Groq API key
   - `GEMINI_API_KEY` - Your Gemini API key  
   - `SECRET_KEY` - A random secret string (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
5. **Deploy** - Railway will automatically detect the Procfile and deploy!

### Option 2: Render (Free Tier Available)

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: Your app name
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
5. **Add Environment Variables**:
   - `GROQ_API_KEY`
   - `GEMINI_API_KEY`
   - `SECRET_KEY`
6. Click **"Create Web Service"**

### Option 3: Docker (For Any Platform)

```bash
# 1. Build the image
docker build -t pdf-processor .

# 2. Run locally
docker run -p 5002:5002 \
  -e GROQ_API_KEY=your-key \
  -e GEMINI_API_KEY=your-key \
  -e SECRET_KEY=your-secret \
  pdf-processor

# 3. Push to Docker Hub and deploy to any platform
docker tag pdf-processor yourusername/pdf-processor
docker push yourusername/pdf-processor
```

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] You have Groq API key from https://console.groq.com/
- [ ] You have Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Model files are in the repository (YOLO models in `segmentation/` folder)
- [ ] All code changes are committed to Git
- [ ] Environment variables are set (not hardcoded in code)

## 🔧 Environment Variables

You need to set these in your deployment platform:

```bash
GROQ_API_KEY=your-groq-api-key
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=generate-a-random-secret-key
PORT=5002  # Some platforms set this automatically
```

## ⚠️ Important Notes

1. **File Size Limits**: Some platforms (like Heroku) have file size limits. If your model files are large, consider:
   - Using external storage (AWS S3, etc.)
   - Loading models from URLs at runtime
   - Using platform-specific storage solutions

2. **Memory Requirements**: ML models need memory. Consider:
   - Railway: Upgrade to paid plan for more memory
   - Render: Use Standard plan for better performance
   - Docker: Allocate sufficient resources

3. **Processing Time**: PDF processing can take time. The app is configured with a 300-second timeout, but you may need to increase it for large PDFs.

## 🐛 Troubleshooting

**Issue**: App crashes on startup
- Check that all environment variables are set
- Verify model files exist in the correct paths
- Check logs for specific error messages

**Issue**: Timeout errors
- Increase timeout in Procfile: `--timeout 600`
- Consider implementing async processing

**Issue**: Missing dependencies
- Ensure `poppler-utils` is installed (included in Dockerfile)
- Check that all Python packages are in requirements.txt

## 📚 Full Documentation

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🆘 Need Help?

- Check platform-specific documentation
- Review error logs in your deployment platform
- Ensure all prerequisites are met

