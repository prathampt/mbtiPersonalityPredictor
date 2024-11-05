import cv2
import dlib
import numpy as np
from skimage import io
from skimage import filters
import os
import hashlib

# Set the path to the directory containing the images
image_dir = '/path/to/images'

# Set the path to the output directory for the cropped faces
output_dir = '/path/to/output'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the face detector
face_detector = dlib.get_frontal_face_detector()

# Load the face landmark predictor
landmark_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Function to crop the face from an image
def crop_face(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect the faces in the image
    faces = face_detector(gray, 1)

    # Loop through the detected faces
    for face in faces:
        # Get the face landmarks
        landmarks = landmark_predictor(gray, face)

        # Calculate the face bounding box
        x1 = landmarks.part(0).x
        y1 = landmarks.part(0).y
        x2 = landmarks.part(16).x
        y2 = landmarks.part(16).y

        # Crop the face from the image
        face_image = image[y1:y2, x1:x2]

        # Save the cropped face to the output directory
        face_hash = hashlib.md5(image_path.encode()).hexdigest()
        face_path = os.path.join(output_dir, f'{face_hash}.jpg')
        cv2.imwrite(face_path, face_image)

# Loop through the images in the directory
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(image_dir, filename)
        crop_face(image_path)

print('Face cropping complete!')