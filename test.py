import requests
from bs4 import BeautifulSoup
import os
import time

# 웹사이트 기본 URL. 여기에 크롤링하려는 사이트의 URL을 입력하세요.
base_url = 'https://~~.com/np/categories/~~'
headers = {
    # 사용자 에이전트 정보를 설정합니다. 필요시 자신의 브라우저 정보를 입력하세요.
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    # 언어 설정. 여기에 자신이 사용하는 언어 정보를 넣으세요.
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3'
}

# 이미지가 저장될 폴더명. 원하는 폴더명을 입력하세요.
folder_name = '~~_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

page_num = 1

while True:
    # 페이지 번호를 URL에 추가합니다. 웹사이트 구조에 맞게 URL을 수정하세요.
    url = f'{base_url}?page={page_num}'
    print(f"Sending request to the website: {url}")
    
    # 웹사이트에 요청을 보내는 부분입니다.
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage or no more pages. Status code: {response.status_code}")
        break

    print("Parsing the HTML...")
    soup = BeautifulSoup(response.text, 'html.parser')

    print("Finding image tags...")
    images = soup.find_all('img')
    print(f"Found {len(images)} images on page {page_num}.")

    for i, img in enumerate(images):
        img_url = img.get('src')
        data_src = img.get('data-src')
        onerror = img.get('onerror')

        # 이미지 URL에서 필요한 정보를 추출하여 다운로드하는 부분입니다.
        if img_url and img_url.startswith('//thumbnail') and '~~cdn.com' in img_url:
            img_url = 'https:' + img_url 

            print(f"Downloading image {i+1} from {img_url}")
            img_data = requests.get(img_url).content
            with open(f'{folder_name}/image_page{page_num}_{i+1}.jpg', 'wb') as handler:
                handler.write(img_data)
            print(f"Image {i+1} on page {page_num} downloaded")
            time.sleep(1)

        elif data_src and data_src.startswith('//thumbnail') and '~~cdn.com' in data_src:
            img_url = 'https:' + data_src

            print(f"Downloading image {i+1} from {img_url}")
            img_data = requests.get(img_url).content
            with open(f'{folder_name}/image_page{page_num}_{i+1}.jpg', 'wb') as handler:
                handler.write(img_data)
            print(f"Image {i+1} on page {page_num} downloaded")
            time.sleep(1)

    page_num += 1

print("모든 이미지 다운로드 완료")
