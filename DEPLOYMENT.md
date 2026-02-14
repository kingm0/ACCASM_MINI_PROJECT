# Deployment Guide

This guide will help you deploy your Flask PDF processing application to various platforms.

## Prerequisites

1. **API Keys**: You'll need:
   - Groq API Key (from https://console.groq.com/)
   - Gemini API Key (from https://makersuite.google.com/app/apikey)

2. **Model Files**: Ensure you have:
   - YOLO model files in `segmentation/documents-segment-classification-main/yolo-coco/`
   - StructEqTable model files (if using table processing)

## Important Notes Before Deployment

⚠️ **Security Issues to Fix:**
1. **Hardcoded API Keys**: Your `main.py` contains hardcoded API keys. These should be moved to environment variables.
2. **Hardcoded Paths**: Some paths are hardcoded (e.g., `/Users/kingm01/Downloads/Mini-Project/`). These need to be made relative or configurable.

## Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Local Docker Testing
```bash
# Build the Docker image
docker build -t pdf-processor .

# Run the container
docker run -p 5002:5002 \
  -e GROQ_API_KEY=your-key \
  -e GEMINI_API_KEY=your-key \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/static:/app/static \
  pdf-processor
```

#### Deploy to Cloud Platforms with Docker

**Railway:**
1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

**Render:**
1. Connect your GitHub repository
2. Select "New Web Service"
3. Use the Dockerfile
4. Add environment variables in the dashboard

**AWS/GCP/Azure:**
- Use their container services (ECS, Cloud Run, Container Instances)
- Push your Docker image to their container registries

### Option 2: Heroku Deployment

1. **Install Heroku CLI** (if not already installed)
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create a Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GROQ_API_KEY=your-groq-key
   heroku config:set GEMINI_API_KEY=your-gemini-key
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

**Note**: Heroku has file size limits. You may need to use external storage (S3, etc.) for model files.

### Option 3: Railway Deployment

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   railway init
   ```

4. **Set Environment Variables** (in Railway dashboard or CLI)
   ```bash
   railway variables set GROQ_API_KEY=your-key
   railway variables set GEMINI_API_KEY=your-key
   railway variables set SECRET_KEY=your-secret-key
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### Option 4: Render Deployment

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Environment**: Python 3
5. Add environment variables in the dashboard
6. Deploy

### Option 5: DigitalOcean App Platform

1. Go to [DigitalOcean](https://www.digitalocean.com/products/app-platform)
2. Create a new app from GitHub
3. Configure:
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn --bind 0.0.0.0:$PORT app:app`
4. Add environment variables
5. Deploy

## Environment Variables

Create a `.env` file (or set in your platform's dashboard):

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
GROQ_API_KEY=your-groq-api-key
GEMINI_API_KEY=your-gemini-api-key
PORT=5002
```

## Code Changes Needed Before Deployment

### 1. Fix Hardcoded API Keys

In `your_colab_code/main.py`, replace hardcoded API keys:

```python
# Instead of:
os.environ["GROQ_API_KEY"] = "gsk_..."

# Use:
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
```

### 2. Fix Hardcoded Paths

In `your_colab_code/main.py` line 37, change:
```python
# Instead of:
yolo_path = '/Users/kingm01/Downloads/Mini-Project/segmentation/documents-segment-classification-main/yolo-coco'

# Use:
yolo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                        'segmentation', 
                        'documents-segment-classification-main', 
                        'yolo-coco')
```

### 3. Update Secret Key

In `app.py` line 8, use environment variable:
```python
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-change-in-production')
```

## Post-Deployment Checklist

- [ ] Environment variables are set correctly
- [ ] API keys are configured (not hardcoded)
- [ ] Model files are accessible
- [ ] Static files are being served correctly
- [ ] Upload directory has write permissions
- [ ] Application is accessible via URL
- [ ] Test PDF upload functionality
- [ ] Check logs for any errors

## Troubleshooting

### Common Issues

1. **Port Issues**: Some platforms use `$PORT` environment variable. Update your Procfile accordingly.

2. **Model Files Not Found**: 
   - Ensure model files are in the repository (or use external storage)
   - Check paths are relative, not absolute

3. **Memory Issues**: 
   - ML models can be memory-intensive
   - Consider using platforms with higher memory limits
   - Or optimize model loading

4. **Timeout Issues**: 
   - PDF processing can take time
   - Increase timeout in gunicorn: `--timeout 600`
   - Consider async processing with Celery

5. **Missing Dependencies**:
   - Ensure `poppler-utils` is installed (for pdf2image)
   - Check all system dependencies in Dockerfile

## Scaling Considerations

For production:
- Use a proper database instead of in-memory storage
- Implement job queues (Celery + Redis) for async processing
- Use cloud storage (S3, etc.) for file uploads
- Implement caching (Redis)
- Add monitoring and logging
- Use a reverse proxy (Nginx)

## Support

For issues specific to deployment platforms, refer to their documentation:
- [Heroku Docs](https://devcenter.heroku.com/)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Docker Docs](https://docs.docker.com/)

