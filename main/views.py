# menus / views.py
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# Model
from .models import Main
from .serializers import MainSerializer


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
      # json 형식이 아닐 때 예외 처리
      req_data = json.loads(json.dumps(request.data))
      # try:
      #   req_data = json.loads(request.body)
      # except json.JSONDecodeError as e:
      #   return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
      
      x_forwared_for = request.META.get('HTTP_X_FORWARDED_FOR')
      if x_forwared_for:
        ip = x_forwared_for.split(',')[0]
      else:
        ip = request.META.get('REMOTE_ADDR')

      urlPath = f"https://trace.cjlogistics.com/web/detail.jsp?slipno={req_data['slipno']}"
      # 680349049175
      try:
        result = main(urlPath) # 680..75 => {...}
      except:
        return Response({'error' : result['msg']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
      # DB
      try:
        customReqJson = {'ip': f'{ip}', 'url': urlPath}
        serializer = MainSerializer(data=customReqJson)
        if serializer.is_valid():
          serializer.save()
        return Response(result)
      except Exception as e:
        return Response({'error': f'DB erorr: {e}'})

def main(url):
    isFinished = False

    try:
      try:
        driver.get(url)
      except:
        return {'msg': 'invalid url & id, please check'}

      recent_state = driver.find_elements(By.CSS_SELECTOR, "table#detailContent tbody tr")[1]
      deliveryState = recent_state.find_elements(By.CSS_SELECTOR, "td[align='center']")[3]

      deliveryStateText = deliveryState.text
      if (deliveryStateText.__contains__("배송완료")):
        isFinished = True

      return {'isDelievered': f'{isFinished}', 'deliveryState': f'{deliveryStateText}'}
    except Exception as e:
      return {'msg': f'{e}'}