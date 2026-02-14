# Gemini AI Integration Setup Guide

## Overview

This project now supports two processing methods:

1. **ML Model Processing** - Your existing machine learning model for document analysis
2. **Gemini AI Processing** - Google's Gemini AI for intelligent document analysis

## Setup Instructions

### 1. Install Additional Dependencies

```bash
pip install -r requirements_gemini.txt
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### 3. Set Environment Variable

Set your Gemini API key as an environment variable:

**On macOS/Linux:**

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**On Windows:**

```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Or modify the gemini_integration.py file:**
Replace `'YOUR_GEMINI_API_KEY_HERE'` with your actual API key in the `GeminiProcessor.__init__()` method.

### 4. Run the Application

```bash
python app.py
```

## Features

### Enhanced Upload Interface

- **Modern UI/UX**: Beautiful gradient design with hover effects
- **Drag & Drop**: Support for dragging PDF files directly onto the upload area
- **Two Processing Options**:
  - 🧠 **Process with ML Model**: Uses your existing ML pipeline
  - ✨ **Process with Gemini AI**: Uses Google's Gemini AI for analysis

### Loading Experience

- **Animated Loading Page**: Modern spinner with progress indicators
- **Step-by-Step Progress**: Shows processing stages
- **Responsive Design**: Works on all devices

### Gemini AI Results

- **Comprehensive Analysis**: Summary, insights, keywords, and recommendations
- **Beautiful Results Page**: Card-based layout with gradients and animations
- **Download Report**: Export analysis as text file
- **Interactive Elements**: Hover effects and smooth transitions

## How It Works

### ML Model Processing (Original)

1. User uploads PDF
2. Shows loading animation
3. Processes with your existing ML model
4. Displays results with images, text, and audio

### Gemini AI Processing (New)

1. User uploads PDF
2. Shows loading animation
3. Converts PDF to images
4. Sends images to Gemini AI for analysis
5. Displays structured results (summary, insights, keywords, recommendations)

## Customization

### Modifying the Gemini Prompt

Edit the `analysis_prompt` in `gemini_integration.py` to customize what kind of analysis Gemini performs:

```python
self.analysis_prompt = """
Your custom prompt here...
"""
```

### Styling

- Modify CSS in the template files to change colors, fonts, or layout
- All templates use modern CSS with gradients and animations
- Responsive design works on mobile and desktop

## Troubleshooting

### Common Issues

1. **"No API key found"**

   - Make sure you've set the GEMINI_API_KEY environment variable
   - Or update the key directly in gemini_integration.py

2. **"Error processing document"**

   - Check if the PDF file is valid and not corrupted
   - Ensure you have sufficient API quota

3. **Loading page doesn't redirect**
   - Check browser console for JavaScript errors
   - Ensure all static files are properly served

### API Limits

- Gemini API has rate limits and usage quotas
- Check your usage in the Google AI Studio dashboard
- Consider implementing caching for repeated requests

## File Structure

```
├── app.py                          # Main Flask application
├── gemini_integration.py           # Gemini AI integration
├── templates/
│   ├── use.html                    # Enhanced upload page
│   ├── loading.html                # Loading animation page
│   ├── gemini_result.html          # Gemini results page
│   └── result.html                 # ML model results page
├── requirements_gemini.txt         # Additional dependencies
└── GEMINI_SETUP.md                # This setup guide
```

## Next Steps

1. Set up your Gemini API key
2. Test with sample PDF files
3. Customize the analysis prompt for your specific use case
4. Modify the UI styling to match your brand
5. Add error handling and logging as needed

Enjoy your enhanced document processing system! 🚀
