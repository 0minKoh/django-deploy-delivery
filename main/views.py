# menus / views.py
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from pyvirtualdisplay import Display
import time

# ssh -i /Users/sohyunwoo/.ssh/delievery_deploy.pem ubuntu@ec2-43-201-149-60.ap-northeast-2.compute.amazonaws.com
# Create your views here.
chrome_options = Options()
chrome_options.add_argument('--headless')  # headless 모드 설정
# display = Display(visible=0, size=(1024, 768))
# display.start()
driver = webdriver.Chrome(options=chrome_options)

@api_view(['GET'])
def index(request):
    return render(request, 'main/index.html')

@api_view(['POST'])
def getUrlAndShowState(request):
    if request.method == 'POST':
      data = json.loads(request.body)
      try:
        result = main(data['url'])
        return Response(result)
      except:
        return Response(result)

def main(url):
    isFinished = False

    try: 
      driver.get(url)

      recent_state = driver.find_elements(By.CSS_SELECTOR, "table#detailContent tbody tr")[1]
      deliveryState = recent_state.find_elements(By.CSS_SELECTOR, "td[align='center']")[3]

      deliveryStateText = deliveryState.text
      if (deliveryStateText.__contains__("배송완료")):
        isFinished = True

      return {'isDelievered': f'{isFinished}', 'deliveryState': f'{deliveryStateText}'}
    except Exception as e:
      return {'msg': f'{e}'}