import numpy as np
import argparse
import time
import cv2
import os

# construct the argument parse and parse the arguments
yolo_path = 'yolo-coco'
# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.join(yolo_path, "classes.names")
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.join(yolo_path, "yolov3.weights")
configPath = os.path.join(yolo_path, "yolov3.cfg")

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

from tkinter import filedialog as fd
filename = fd.askopenfilename()

from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox

print(filename)

# Use default poppler path on Linux or update if necessary
def pdf2img():
    try:
        # Assuming poppler is installed system-wide. If not, provide path.
        images = convert_from_path(filename, dpi=50)  # No poppler_path needed in Linux if installed globally
        for i, image in enumerate(images):
            fname = f'image{i}.png'
            image.save(fname, "PNG")

            # load our input image and grab its spatial dimensions
            image = cv2.imread(fname)
            (H, W) = image.shape[:2]

            # determine only the *output* layer names that we need from YOLO
            # Check the shape and content of `getUnconnectedOutLayers()` and `getLayerNames()`
            ln = net.getLayerNames()

            # Get the output layer indices
            outLayers = net.getUnconnectedOutLayers()

            # Ensure you are using 0-based indexing when accessing layers
            ln = [ln[i - 1] for i in outLayers]

            # Print to debug
            print(f"Layer Names: {ln}")


            # construct a blob from the input image and then perform a forward pass of the YOLO object detector
            blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()

            # show timing information on YOLO 
            print("[INFO] YOLO took {:.6f} seconds".format(end - start))

            # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []

            # loop over each of the layer outputs
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    if confidence > 0.5:
                        # Scale the bounding box coordinates back relative to the size of the image
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # Update our list of bounding box coordinates, confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

            # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
            if len(boxes) > 0:  # Ensure there are boxes to process
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.3)

                # Ensure idxs is not empty
                if len(idxs) > 0:
                    for i in idxs.flatten():
                        # Extract bounding box coordinates
                        (x, y) = (boxes[i][0], boxes[i][1])
                        (w, h) = (boxes[i][2], boxes[i][3])

                        # Draw a bounding box rectangle and label on the image
                        color = [int(c) for c in COLORS[classIDs[i]]]
                        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                        text = f"{LABELS[classIDs[i]]}: {confidences[i]:.4f}"
                        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            imgresize = cv2.resize(image, (960, 520))
            cv2.imshow("Image", imgresize)
            cv2.waitKey(0)

    except Exception as e:
        messagebox.showinfo("Result", f"Error: {e}")
    else:
        messagebox.showinfo("Result", "Success")


master = Tk()
Label(master, text="File Location").grid(row=0, sticky=W)

b = Button(master, text="Convert", command=pdf2img)
b.grid(row=2, column=1, columnspan=2, rowspan=2, padx=5, pady=5)

mainloop()
# import numpy as np
# import argparse
# import time
# import cv2
# import os
# from pdf2image import convert_from_path
# from tkinter import filedialog as fd
# from tkinter import *
# from tkinter import messagebox
# from PIL import Image
# from io import BytesIO
# from pix2tex.cli import LatexOCR
# from pylatexenc.latex2text import LatexNodes2Text
# from gtts import gTTS
# from IPython.display import Audio

# # YOLO setup
# yolo_path = 'yolo-coco'
# labelsPath = os.path.join(yolo_path, "classes.names")
# LABELS = open(labelsPath).read().strip().split("\n")
# np.random.seed(42)
# COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
# weightsPath = os.path.join(yolo_path, "yolov3.weights")
# configPath = os.path.join(yolo_path, "yolov3.cfg")
# print("[INFO] loading YOLO from disk...")
# net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# # Initialize LaTeX OCR model
# model = LatexOCR()

# # Function to process PDF to images and extract equations
# def pdf2img_and_extract_equations():
#     try:
#         # Select PDF file
#         filename = fd.askopenfilename()
#         images = convert_from_path(filename, dpi=500)

#         equation_images = []  # To store cropped images of equations

#         for i, image in enumerate(images):
#             fname = f'image{i}.png'
#             image.save(fname, "PNG")
#             image = cv2.imread(fname)
#             (H, W) = image.shape[:2]
#             ln = net.getLayerNames()
#             outLayers = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
#             print(f"Layer Names: {layerOutputs}")
#             blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#             net.setInput(blob)
#             start = time.time()
#             layerOutputs = net.forward(ln)
#             end = time.time()

#              # show timing information on YOLO 
#             print("[INFO] YOLO took {:.6f} seconds".format(end - start))

#             net.setInput(blob)
#             layerOutputs = net.forward(outLayers)
#             boxes = []
#             confidences = []
#             classIDs = []

#             for output in layerOutputs:
#                 for detection in output:
#                     scores = detection[5:]
#                     classID = np.argmax(scores)
#                     confidence = scores[classID]

#                     if confidence > 0.5:
#                         box = detection[0:4] * np.array([W, H, W, H])
#                         (centerX, centerY, width, height) = box.astype("int")
#                         x = int(centerX - (width / 2))
#                         y = int(centerY - (height / 2))
#                         boxes.append([x, y, int(width), int(height)])
#                         confidences.append(float(confidence))
#                         classIDs.append(classID)

#             idxs = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.3)

#             if len(idxs) > 0:
#                 for i in idxs.flatten():
#                     if LABELS[classIDs[i]] == "Equation":  # Check if class is 'Equation'
#                         x, y, w, h = boxes[i]
#                         cropped_image = image[y:y+h, x:x+w]
#                         equation_images.append(cropped_image)
#                         color = [int(c) for c in COLORS[classIDs[i]]]
#                         cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
#                         text = f"{LABELS[classIDs[i]]}: {confidences[i]:.4f}"
#                         cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#         imgresize = cv2.resize(image, (960, 520))
#         cv2.imshow("Image", imgresize)
#         cv2.waitKey(0)
#         # Process equations with LaTeX OCR
#         process_equations(equation_images)

#     except Exception as e:
#         messagebox.showinfo("Result", f"Error: {e}")
#     else:
#         messagebox.showinfo("Result", "Processing Completed!")

# # Function to process equations and generate audio
# def process_equations(equation_images):
#     extracted_texts = []
#     for img in equation_images:
#         try:
#             img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#             prediction = model(img_pil)
#             if isinstance(prediction, str):
#                 plain_text = LatexNodes2Text().latex_to_text(prediction)
#                 extracted_texts.append(plain_text)
#                 print(f"Extracted LaTeX: {prediction}")
#                 print(f"Plain Text: {plain_text}")
#             else:
#                 print("Invalid LaTeX prediction.")
#         except Exception as e:
#             print(f"Error processing equation: {e}")

#     if extracted_texts:
#         combined_text = " ".join(extracted_texts)
#         print("Final Combined Text:", combined_text)
#         generate_audio(combined_text)

# # Function to generate audio from text
# def generate_audio(text):
#     try:
#         tts = gTTS(text=text, lang='hi')
#         audio_path = "extracted_text_audio.mp3"
#         tts.save(audio_path)
#         print(f"Audio saved to {audio_path}")
#         display(Audio(audio_path, autoplay=True))
#     except Exception as e:
#         print(f"Error generating audio: {e}")

# # GUI setup
# master = Tk()
# Label(master, text="PDF to Equation Extractor").grid(row=0, sticky=W)
# b = Button(master, text="Start Processing", command=pdf2img_and_extract_equations)
# b.grid(row=2, column=1, columnspan=2, rowspan=2, padx=5, pady=5)
# mainloop()
