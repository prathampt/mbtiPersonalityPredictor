import os
import pandas as pd
from icrawler.builtin import GoogleImageCrawler
import contextlib
import logging

# The output directory
output_dir = "MBTI_Images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of emotions to search for
emotions = ["happy", "sad", "angry", "surprised", "neutral"]

# Function to download images using icrawler
def download_images(name, mbti_type, temp_dir, num_images_per_emotion=1):
    for emotion in emotions:
        crawler = GoogleImageCrawler(storage={'root_dir': temp_dir})
        filters = dict(
            size='medium',
            type='face'
        )
        
        with open(os.devnull, 'w') as fnull:
            with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                crawler.crawl(keyword=f"{name} {emotion} clean portrait face frontfacing", max_num=num_images_per_emotion, filters=filters)
        
        # Rename the downloaded images
        for filename in os.listdir(temp_dir):
            if filename.endswith((".jpeg", ".jpg", ".png")):
                ext = os.path.splitext(filename)[1]  # Get the file extension
                new_filename = f"{name.replace(' ', '_')}_{emotion}{ext}"
                os.rename(os.path.join(temp_dir, filename), os.path.join(output_dir, mbti_type, new_filename))

# Configure logging to suppress messages from icrawler
logging.getLogger('icrawler').setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Read the CSV file
csv_file_path = './data/raw_mbtiSmall.csv'  # Update this path if necessary
data = pd.read_csv(csv_file_path)

# Create the necessary directories and download images
for index, row in data.iterrows():
    name = row['name']
    mbti_type = row['mbti']
    
    print(f"Processing: {name} ({mbti_type})")
    
    mbti_dir = os.path.join(output_dir, mbti_type)
    if not os.path.exists(mbti_dir):
        os.makedirs(mbti_dir)
    
    temp_dir = os.path.join(mbti_dir, "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    download_images(name, mbti_type, temp_dir)
    
    # Remove the temporary directory after processing
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

print("Data collection complete!")
