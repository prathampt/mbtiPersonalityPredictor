import os
import requests
from bs4 import BeautifulSoup
from icrawler.builtin import GoogleImageCrawler

# Define MBTI types
mbti_types = {
    1: "istj", 2: "estj", 3: "isfj", 4: "esfj",
    5: "esfp", 6: "isfp", 7: "estp", 8: "istp",
    9: "infj", 10: "enfj", 11: "infp", 12: "enfp",
    13: "intp", 14: "entp", 15: "intj", 16: "entj"
}

base_url = "https://www.personalityclub.com/blog/famous-{}/"

output_dir = "MBTI_Images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def scrape_celebrity_names(mbti_type):
    url = base_url.format(mbti_type)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    names = []
    for ul in soup.find_all('ul'):
        h4_tag = ul.find_previous_sibling('h4')
        if h4_tag and 'FICTIONAL CHARACTERS' in h4_tag.text:
                break
        for li in ul.find_all('li'):
            for span in li.find_all('span'):
                span.decompose()
            t = li.get_text(strip=True)
            names.append(t) if t else None
    return names

# Function to download images using icrawler
def download_images(name, mbti_type, temp_dir, num_images=1):
    crawler = GoogleImageCrawler(storage={'root_dir': temp_dir})
    filters = dict(
        size='medium',
        type='face'
    )
    crawler.crawl(keyword=f"{name} clean portrait face forward", max_num=num_images, filters=filters)
    
    # Rename the downloaded image
    for filename in os.listdir(temp_dir):
        if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):
            new_filename = f"{name.replace(' ', '_')}.jpeg"
            os.rename(os.path.join(temp_dir, filename), os.path.join(output_dir, mbti_type, new_filename))

# Scrape names and download images
for mbti in mbti_types.values():
    print(f"Processing MBTI type: {mbti}")
    names = scrape_celebrity_names(mbti)

    temp_dir = os.path.join(output_dir, mbti, "temp")

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if mbti == "estj":
        break
    
    for name in names:
        print(f"  Downloading images for {name}...")
        download_images(name, mbti, temp_dir)

    os.rmdir(temp_dir)

print("Data collection complete!")
