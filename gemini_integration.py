import os
import io
import base64
import google.generativeai as genai
from pdf2image import convert_from_path
from PIL import Image
import json
import re

class GeminiProcessor:
    def __init__(self):
        # Initialize Gemini API
        # You'll need to set your Gemini API key here
        # Get your API key from: https://makersuite.google.com/app/apikey
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Define the analysis prompt
        self.analysis_prompt = """
                    You are an expert document analyst and accessibility writer.  
        I am giving you a full 5th-grade school textbook in PDF format that contains text, pictures, graphs, tables, and diagrams.  

        Your task is to read and understand the entire textbook and then summarize it in a way that a 5th-grade blind student can easily understand when the content is read aloud.  

        Please follow these rules:  
        1. Use very simple words and short sentences (no more than 12 words each).  
        2. Be relevant and upto the mark with consice answers.
        3. Describe every picture, graph, diagram, and table in clear spoken words.  
        - For pictures: mention the main objects and what is happening.  
        - For diagrams: explain the steps in order (Step 1, Step 2, etc.).  
        - For graphs: name the axes, describe the trend (up, down, flat), and give one or two example numbers.  
        - For tables: explain what the columns and rows mean, then give one or two easy comparisons.  
        4. At the end, create one complete “read-aloud script” with all the summaries and descriptions combined. This script should be easy to use directly for audio playback.  
        5. If something in the PDF is unclear or unreadable, say so directly.  
        6. It should not give unnecessary information and vague words and unnecessary information.
        7. Do not Miss any information given in the question and and provide any irrelavent text in the output, just give the ans without any other single word.
        8. Read the Mathematical equations and all efficiently and do not use any chat initialization syntax and everything.
        9. Do not miss any information about the question, such as the values and everything given.

        Important: Write everything in a warm, formal tone, explaining the relevant data only, as if you are talking to a small child who cannot see. Focus on clarity and comfort.


        """
    
    def process_pdf_with_gemini(self, pdf_path):
        """
        Process a PDF file using Gemini AI
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            images = convert_from_path(pdf_path, dpi=150)
            
            page_urls = []
            page_images_dir = os.path.join('static', 'page_images')
            os.makedirs(page_images_dir, exist_ok=True)
            
            pdf_basename = os.path.basename(pdf_path).replace('.pdf', '')
            
            for i, image in enumerate(images):
                page_filename = f"page_{i+1}_{pdf_basename}.png"
                page_path = os.path.join(page_images_dir, page_filename)
                image.save(page_path, 'PNG')
                page_urls.append(f"static/page_images/{page_filename}")
            
            results = []
            for i, image in enumerate(images):
                print(f"Processing page {i+1} of {len(images)}...")
                
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                
                prompt = f"{self.analysis_prompt}\n\nThis is page {i+1} of the document."
                
                response = self.model.generate_content([prompt, Image.open(io.BytesIO(img_bytes))])
                
                results.append({
                    'page': i+1,
                    'content': response.text
                })
            
            page_explanations = [result['content'] for result in results]
            
            return {
                'page_explanations': page_explanations,
                'page_urls': page_urls
            }
            
        except FileNotFoundError as e:
            print(f"File error: {e}")
            return self._get_error_response(str(e))
        except Exception as e:
            print(f"Error processing PDF with Gemini: {e}")
            return self._get_error_response(str(e))
    
    def _combine_page_analyses(self, page_results):
        """
        Combine analyses from multiple pages into a single comprehensive analysis
        """
        try:
            # Extract JSON from each page
            page_data = []
            for result in page_results:
                try:
                    json_match = re.search(r'\{.*\}', result['content'], re.DOTALL)
                    if json_match:
                        page_json = json.loads(json_match.group())
                        page_data.append(page_json)
                except (json.JSONDecodeError, AttributeError):
                    page_data.append({
                        'summary': result['content'][:200] + "...",
                        'insights': "Content analysis available",
                        'keywords': ["document", "content", "analysis"],
                        'recommendations': "Review document content"
                    })
            
            # Combine all page data
            combined_summary = " ".join([data.get('summary', '') for data in page_data])
            print(combined_summary)
            combined_insights = " ".join([data.get('insights', '') for data in page_data])
            print(combined_insights)
            
            # Collect all keywords
            all_keywords = []
            for data in page_data:
                keywords = data.get('keywords', [])
                if isinstance(keywords, list):
                    all_keywords.extend(keywords)
            
            # Remove duplicates and limit to top keywords
            unique_keywords = list(set(all_keywords))[:10]
            
            combined_recommendations = " ".join([data.get('recommendations', '') for data in page_data])
            print(combined_recommendations)
            return {
                'summary': combined_summary[:500] + "..." if len(combined_summary) > 500 else combined_summary,
                'insights': combined_insights[:500] + "..." if len(combined_insights) > 500 else combined_insights,
                'keywords': unique_keywords,
                'recommendations': combined_recommendations[:500] + "..." if len(combined_recommendations) > 500 else combined_recommendations
            }
            
        except Exception as e:
            print(f"Error combining analyses: {e}")
            return self._get_error_response(str(e))
    
    def _get_error_response(self, error_message):
        """
        Return a default response when processing fails
        """
        return {
            'page_explanations': [f"Document processing encountered an error: {error_message}. Please try again or contact support."],
            'page_urls': []
        }
    
    def analyze_text_content(self, text_content):
        """
        Analyze text content directly (alternative method)
        """
        try:
            prompt = f"{self.analysis_prompt}\n\nDocument text content:\n{text_content}"
            
            response = self.model.generate_content(prompt)
            
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # If no JSON found, create a structured response
                return {
                    'summary': response.text[:500] + "..." if len(response.text) > 500 else response.text,
                    'insights': "AI analysis completed successfully.",
                    'keywords': ["analysis", "content", "document"],
                    'recommendations': "Review the generated summary for key information."
                }
                
        except Exception as e:
            print(f"Error analyzing text content: {e}")
            return self._get_error_response(str(e))

# Example usage function
def process_document_with_gemini(pdf_path):
    """
    Main function to process a document with Gemini AI
    """
    processor = GeminiProcessor()
    return processor.process_pdf_with_gemini(pdf_path)

# Test function (you can modify the prompt here)
def test_gemini_analysis():
    """
    Test function to verify Gemini integration
    """
    processor = GeminiProcessor()
    
    # Test with sample text
    sample_text = """
    This is a sample document about machine learning and artificial intelligence.
    The document discusses various algorithms, neural networks, and their applications
    in real-world scenarios. It covers topics like supervised learning, unsupervised learning,
    and reinforcement learning approaches.
    """
    
    result = processor.analyze_text_content(sample_text)
    print("Gemini Analysis Result:")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    # Run test
    test_gemini_analysis()
