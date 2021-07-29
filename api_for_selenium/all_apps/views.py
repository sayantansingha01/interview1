from django.shortcuts import render
from rest_framework.views import APIView
from django.http import FileResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED,
                                   )
from django.http import HttpResponse

from all_apps.serializers import UserDataSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from all_apps.models import OthersField
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
import time

from selenium.webdriver.common.keys import Keys
opts=webdriver.ChromeOptions()
opts.headless=True


class SignUpView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        return Response({'data': 'method not allowed'}, status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = UserDataSerializer(data=request.data)
        if data.is_valid():
            try:
                validated_data = data.validated_data
                email = validated_data.get("email")
                username = validated_data.get("username")
                password = validated_data.get("password")
                address = validated_data.get("address")
                phone_number = validated_data.get("phone_number")
                user = User.objects.create_user(username, email)
                user.save()
                user.set_password(password)
                user.save()
                obj = OthersField(user=user, address=address, phone_number=phone_number)
                obj.save()
                return Response({'data': "profile saved successfully"},
                                status=HTTP_201_CREATED)

            except Exception:
                return Response({"msg":"Internal server error"},
                                status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data.errors, status=HTTP_400_BAD_REQUEST)
        return Response({
                        "msg":"Internal server error"},
                        status=HTTP_400_BAD_REQUEST)


class Proile(APIView):
    """
    Authorization:  Bearer <Token>

    """
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user = request.user
            obj = OthersField.objects.filter(user=user).first()
            if obj:
                return Response({'email': request.user.email,
                                 'username': request.user.username,
                                 'address': obj.address,
                                 'phone_number': obj.phone_number
                                 }, status=HTTP_200_OK)
            else:
                return Response({'email': request.user.email,
                                 'username': request.user.username,
                                 'address': "",
                                 'phone_number': ""
                                 }, status=HTTP_200_OK)
        except Exception:
            return Response({"msg": "internal server error"}, status=HTTP_400_BAD_REQUEST)
        return Response({"msg": "internal server error"}, status=HTTP_400_BAD_REQUEST)


class SeleniumView(APIView):
    """
        {
      "name": " ",
      "id": " ",
      "address": " ",
      "city": " ",
      "state": " ",
      "country": "Afghanistan",
      "sdn": "SDN"
    }

    """

    def post(self, request):
        try:
            name = request.data.get("name")
            id = request.data.get("id")
            address = request.data.get("address")
            city = request.data.get("city")
            state = request.data.get("state")
            country = request.data.get("country")
            sdn = request.data.get("sdn")
            if all([name, id, address, city, state, country, sdn]):
                result = self.auto(name, id, address, city, state, country, sdn)
                print(result)
                return Response({"result": result},
                                status=HTTP_200_OK)
            else:
                return Response({"msg": "Please fill data properly"}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"msg": str(e)},
                            status=HTTP_400_BAD_REQUEST)

        return Response({"msg": "internal server error"},
                        status=HTTP_400_BAD_REQUEST)

    def auto(self, name, id, address, city, state, country, sdn):
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
        driver.get("https://sanctionssearch.ofac.treas.gov/")
        driver.set_window_size(1920, 1000)
        driver.find_element(By.ID, "ctl00_MainContent_txtLastName").send_keys(name)
        driver.find_element(By.ID, "ctl00_MainContent_txtID").send_keys(id)
        driver.find_element(By.ID, "ctl00_MainContent_txtAddress").send_keys(address)
        driver.find_element(By.ID, "ctl00_MainContent_txtCity").send_keys(city)
        driver.find_element(By.ID, "ctl00_MainContent_txtState").send_keys(state)
        sel = Select(driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddlCountry']"))
        sel.select_by_visible_text(country)
        sel1 = Select(driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddlList']"))
        sel1.select_by_visible_text(sdn)
        driver.find_element(By.ID, "ctl00_MainContent_btnSearch").click()
        table_id = driver.find_element(By.ID, "gvSearchResults")
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        result = []
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")[0]
            sub = dict()
            sub["0"] = col.text
            sub["1"] = (row.find_elements(By.TAG_NAME, "td")[1]).text
            sub["2"] = (row.find_elements(By.TAG_NAME, "td")[2]).text
            sub["3"] = (row.find_elements(By.TAG_NAME, "td")[3]).text
            result.append(sub)
        return result


class FileShowView(View):

    def get(self, request):
        try:
            opts = webdriver.ChromeOptions()
            opts.headless = True
            preference = {"download.default_directory": r"F:\new_test", "safebrowsing.enable": "false"}

            opts.add_experimental_option("prefs", {
                'download.prompt_for_download': False,
                'download.default_directory': r"F:\new_test\api_for_selenium",
                'download.directory_upgrade': True,
                'plugins.always_open_pdf_externally': True,
            })

            driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
            driver.get("https://www.treasury.gov/ofac/downloads/mbs/mbslist.pdf")
            path = r'mbslist.pdf'
            return FileResponse(open(path, 'rb'), content_type='application/pdf')
        except Exception as e:
            print(e)
            return HttpResponse("<h1>404 not found</h1>")

