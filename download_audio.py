import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_mp3(url, save_path):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded to {save_path}")
    else:
        print("Failed to download")

def main():
    base_url = "https://dictionary.cambridge.org/"
    word_base_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
    audio_folder = "英式单词发音"
    
    while True:
        word = input("Enter an English word (or 'exit' to quit): ").strip()
        
        if word.lower() == 'exit':
            print("Exiting the program.")
            break
        
        word_url = urljoin(word_base_url, word)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(word_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            source_elements = soup.find_all('source', type="audio/mpeg")
            
            # 创建存放音频的文件夹
            if not os.path.exists(audio_folder):
                os.makedirs(audio_folder)
            
            for source_element in source_elements:
                src = source_element['src']
                if "/media/english-chinese-traditional/uk_pron/u/uk" in src:
                    mp3_url = urljoin(base_url, src)
                    mp3_filename = f"{word}.mp3"
                    mp3_save_path = os.path.join(audio_folder, mp3_filename)
                    
                    print("Saving mp3 to:", mp3_save_path)
                    print("Downloading mp3 from:", mp3_url)
                    download_mp3(mp3_url, mp3_save_path)
        else:
            print("Word not found on Cambridge Dictionary")

if __name__ == "__main__":
    main()
