import requests
import json
import numpy as np
import pytesseract
import cv2
from PIL import Image
from time import sleep

from bs4 import BeautifulSoup,SoupStrainer
from io import BytesIO

#code start here
number='KA51ED9789'
app_url = 'https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml'
captcha_image_url = 'https://vahan.nic.in/nrservices/cap_img.jsp'
r = requests.get(url=app_url)
cookies = r.cookies
soup = BeautifulSoup(r.text, 'html.parser')
#MARK: ViewState contains token which needs to be passed in POST Request
# ViewState is a hidden element. Open debugger to inspect element
viewstate = soup.select('input[name="javax.faces.ViewState"]')[0]['value']

#MARK: Get Request to get Captcha Image from URL
## Captcha Image Changes each time the URL is fired
iresponse = requests.get(captcha_image_url)
img = Image.open(BytesIO(iresponse.content))
img.save("downloadedpng.png")

def enhance():
	img = cv2.imread('downloadedpng.png', 0)
	kernel = np.ones((2,2), np.uint8)
	img_erosion = cv2.erode(img, kernel, iterations=1)
	img_dilation = cv2.dilate(img, kernel, iterations=1)
	erosion_again = cv2.erode(img_dilation, kernel, iterations=1)
	final = cv2.GaussianBlur(erosion_again, (1, 1), 0)
	return final
#location of pytesseract exe for windows
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

enhancedImage = enhance()
captchaString=pytesseract.image_to_string(enhancedImage)
print("captcha is "+captchaString)

# MARK: Identifying Submit Button which will be responsible to make POST Request
button = soup.find("button",{"type": "submit"})


encodedViewState = viewstate.replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")

# MARK: Data, which needs to be passed in POST Request | Verify this manually in debugger
data = {
	'javax.faces.partial.ajax':'true',
	'javax.faces.source': button['id'],
	'javax.faces.partial.execute':'@all',
	'javax.faces.partial.render': 'rcDetailsPanel resultPanel userMessages capatcha txt_ALPHA_NUMERIC',
	button['id']:button['id'],
	'masterLayout':'masterLayout',
	'regn_no1_exact': number,
	'txt_ALPHA_NUMERIC': captchaString,
	'javax.faces.ViewState': viewstate,
	'j_idt32':''
}

# MARK: Request Headers which may or may not needed to be passed in POST Request
# Verify in debugger
headers = {
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Accept': 'application/xml, text/xml, */*; q=0.01',
	'Accept-Language': 'en-us',
	'Accept-Encoding': 'gzip, deflate, br',
	'Host': 'vahan.nic.in',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
	'Cookie': 'JSESSIONID=%s; SERVERID_7081=vahanapi_7081; SERVERID_7082=nrservice_7082' % cookies['JSESSIONID'],
	'X-Requested-With':'XMLHttpRequest',
	'Faces-Request':'partial/ajax',
	'Origin':'https://vahan.nic.in',
	'Referer':'https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml',
    'Connection':'keep-alive'
    # 'User-Agent': 'python-requests/0.8.0',
    # 'Access-Control-Allow-Origin':'*',
}
# MARK: Added delay to simulate time required to fill in captcha
sleep(2.0)
#MARK: Send POST Request
postResponse = requests.post(url=app_url, data=data, headers=headers, cookies=cookies)

rsoup = BeautifulSoup(postResponse.text, 'html.parser')
print("Mark: postResponse soup => ")
print(rsoup.prettify())

#MARK: Following code finds tr which means <table> element from html vehicle details response
# the required response is appended in <table> only. Verify it in debugger
table = SoupStrainer('tr')
tsoup = BeautifulSoup(rsoup.get_text(), 'html.parser', parse_only=table)

print("Table Soup => ")
print(tsoup.prettify())
