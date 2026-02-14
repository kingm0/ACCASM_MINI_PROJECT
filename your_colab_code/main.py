
import subprocess

def run_structeqtable(image_path):
    script_path = "StructEqTable-Deploy/tools/demo/demo.py"
    ckpt_path = "U4R/StructTable-InternVL2-1B"

    command = [
        "python3", script_path,
        "--image_path", image_path,
        "--ckpt_path", ckpt_path,
        "--output_format", "latex"
    ]

    # Run the command and capture output
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("Success!")
        return result.stdout  # This is your LaTeX output
    else:
        print("Error:", result.stderr)
        return None

import numpy as np
import time
import cv2
import os
import uuid
import re
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO
from pix2tex.cli import LatexOCR
from pylatexenc.latex2text import LatexNodes2Text
from gtts import gTTS
from groq import Groq

def process_pdf(input_pdf):
    """Process PDF file: extract images, detect objects, and generate audio."""
    print("Processing PDF...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yolo_path = os.getenv('YOLO_PATH', os.path.join(base_dir, 'segmentation', 'documents-segment-classification-main', 'yolo-coco'))
    labels_path = os.path.join(yolo_path, "classes.names")
    
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"YOLO labels file not found: {labels_path}")
    
    with open(labels_path, 'r') as f:
        labels = f.read().strip().split("\n")
    
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
    
    weights_path = os.path.join(yolo_path, "yolov8.weights")
    config_path = os.path.join(yolo_path, "yolov8.cfg")
    
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"YOLO weights file not found: {weights_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"YOLO config file not found: {config_path}")
    
    print("[INFO] Loading YOLO model from disk...")
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    base_output_folder = 'static/cropped_images'
    os.makedirs(base_output_folder, exist_ok=True)

    def pdf2img_and_detect_objects(folder_name="segmentated_images"):
        """Convert PDF to images and detect objects using YOLO."""
        image_paths = []
        output_dir = os.path.join("static", folder_name)
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            if not os.path.exists(input_pdf):
                raise FileNotFoundError(f"PDF file not found: {input_pdf}")
            
            images = convert_from_path(input_pdf, dpi=90)
            
            layer_names = net.getLayerNames()
            output_layers = net.getUnconnectedOutLayers()
            output_layer_names = [layer_names[i - 1] for i in output_layers]
            
            for page_idx, pil_image in enumerate(images):
                temp_filename = f'image_{page_idx}.png'
                pil_image.save(temp_filename, "PNG")
                
                cv_image = cv2.imread(temp_filename)
                if cv_image is None:
                    print(f"Warning: Failed to load image {temp_filename}")
                    continue
                
                height, width = cv_image.shape[:2]
                
                blob = cv2.dnn.blobFromImage(cv_image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                net.setInput(blob)
                
                start_time = time.time()
                layer_outputs = net.forward(output_layer_names)
                processing_time = time.time() - start_time
                print(f"[INFO] YOLO processing took {processing_time:.6f} seconds")
                
                boxes = []
                confidences = []
                class_ids = []
                
                for output in layer_outputs:
                    for detection in output:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        
                        if confidence > 0.05:
                            box = detection[0:4] * np.array([width, height, width, height])
                            center_x, center_y, box_width, box_height = box.astype("int")
                            x = int(center_x - (box_width / 2))
                            y = int(center_y - (box_height / 2))
                            
                            boxes.append([x, y, int(box_width), int(box_height)])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
                
                if len(boxes) > 0:
                    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.3)
                    
                    if len(indices) > 0:
                        for idx in indices.flatten():
                            x, y, w, h = boxes[idx]
                            class_id = class_ids[idx]
                            confidence = confidences[idx]
                            class_name = labels[class_id]
                            
                            class_folder = os.path.join(base_output_folder, class_name)
                            os.makedirs(class_folder, exist_ok=True)
                            
                            x_end = min(x + w, width)
                            y_end = min(y + h, height)
                            x = max(x, 0)
                            y = max(y, 0)
                            
                            cropped_img = cv_image[y:y_end, x:x_end]
                            
                            if cropped_img.size > 0:
                                crop_filename = os.path.join(
                                    class_folder, 
                                    f"{class_name}_cropped_{page_idx}_{temp_filename}"
                                )
                                cv2.imwrite(crop_filename, cropped_img)
                                print(f"Saved cropped {class_name} image: {crop_filename}")
                            
                            color = [int(c) for c in colors[class_id]]
                            cv2.rectangle(cv_image, (x, y), (x + w, y + h), color, 2)
                            label_text = f"{class_name}: {confidence:.4f}"
                            cv2.putText(cv_image, label_text, (x, y - 5), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                resized_image = cv2.resize(cv_image, (960, 520))
                output_filename = f"output_image_{uuid.uuid4().hex[:6]}.jpg"
                output_path = os.path.join(output_dir, output_filename)
                cv2.imwrite(output_path, resized_image)
                image_paths.append(output_path)
                
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
            
            print("Processing completed successfully!")
            
        except Exception as e:
            print(f"Error during PDF processing: {e}")
            raise
        
        return image_paths
    image_paths = pdf2img_and_detect_objects()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running the application.")
    
    latex_model = LatexOCR()

    def process_image_folder(folder_path, groq_client):
        """Process images in a folder and return results."""
        extracted_texts = []
        audio_paths = []
        predictions = []
        image_paths_list = []
        
        if not os.path.isdir(folder_path):
            print(f"Warning: Folder path does not exist: {folder_path}")
            return extracted_texts, audio_paths, predictions, image_paths_list
        
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(image_extensions)]
        
        if not image_files:
            print(f"No image files found in: {folder_path}")
            return extracted_texts, audio_paths, predictions, image_paths_list
        
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            image_paths_list.append(image_path)
            
            try:
                img = Image.open(image_path)
                prediction = latex_model(img)
                
                if not isinstance(prediction, str):
                    print(f"Error: Invalid prediction for {image_file}")
                    audio_paths.append("ERROR in Prediction")
                    extracted_texts.append("ERROR in Prediction")
                    predictions.append("ERROR in Prediction")
                    continue
                
                predictions.append(prediction)
                print(f"Predicted LaTeX for {image_file}: {prediction}")
                
                plain_text = LatexNodes2Text().latex_to_text(prediction)
                print(f"Plain text for {image_file}: {plain_text}")
                
                completion = groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "user", 
                         "content": f"Convert the following plain text content to readable English:\n\n{plain_text}"},
                    ],
                    stop="```",
                )
                
                response_text = completion.choices[0].message.content
                match = re.search(r'"(.*?)"', response_text)
                extracted_text = match.group(1) if match else response_text.strip()
                print(f"English text: {extracted_text}")
                
                output_dir = os.path.join("static", "outputs")
                os.makedirs(output_dir, exist_ok=True)
                
                audio_filename = f"audio_{uuid.uuid4().hex[:6]}.mp3"
                audio_path = os.path.join(output_dir, audio_filename)
                
                tts = gTTS(text=extracted_text, lang='en')
                tts.save(audio_path)
                
                audio_paths.append(audio_path)
                extracted_texts.append(extracted_text)
                
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
                audio_paths.append("ERROR in Prediction")
                extracted_texts.append("ERROR in Prediction")
                predictions.append("ERROR in Prediction")
        
        return extracted_texts, audio_paths, predictions, image_paths_list
    
    groq_client = Groq(api_key=groq_api_key)
    
    equation_folder = "static/cropped_images/Equation"
    text_folder = "static/cropped_images/Text"
    
    eq_texts, eq_audio, eq_predictions, eq_images = process_image_folder(equation_folder, groq_client)
    txt_texts, txt_audio, txt_predictions, txt_images = process_image_folder(text_folder, groq_client)
    
    extracted_texts = eq_texts + txt_texts
    audio_paths = eq_audio + txt_audio
    predictions = eq_predictions + txt_predictions
    images1 = eq_images + txt_images
    
    return image_paths, predictions, extracted_texts, audio_paths, images1