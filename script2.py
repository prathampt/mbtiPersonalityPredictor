import os
import pandas as pd
from icrawler.builtin import GoogleImageCrawler

# Define the output directory
output_dir = "MBTI_Images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define a list of emotions to search for
emotions = ["happy", "sad", "angry", "surprised", "neutral"]

# Function to download images using icrawler
def download_images(name, mbti_type, temp_dir, num_images_per_emotion=1):
    for emotion in emotions:
        crawler = GoogleImageCrawler(storage={'root_dir': temp_dir})
        filters = dict(
            size='medium',
            type='face'
        )
        crawler.crawl(keyword=f"{name} {emotion} clean portrait face forward", max_num=num_images_per_emotion, filters=filters)
        
        # Rename the downloaded images
        for filename in os.listdir(temp_dir):
            if filename.endswith((".jpeg", ".jpg", ".png")):
                ext = os.path.splitext(filename)[1]  # Get the file extension
                new_filename = f"{name.replace(' ', '_')}_{emotion}{ext}"
                os.rename(os.path.join(temp_dir, filename), os.path.join(output_dir, mbti_type, new_filename))

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
