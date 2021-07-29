from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import EmpModelsSerializer
from rest_framework.response import Response
from rest_framework import status

from .models import EmpModels
from django.core.exceptions import ObjectDoesNotExist

class EmployeeApi(viewsets.ViewSet):
    @action(methods=['get'], detail=False, permission_classes=[], authentication_classes=[], url_path="list")
    def get_list(self, request):
        try:
            objs = EmpModels.objects.all()
            list = EmpModelsSerializer(objs, many=True)
            return Response({"data": list.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"msg": "internal server error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg": "internal server error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True, permission_classes=[], authentication_classes=[], url_path="details")
    def get_list_individual(self, request, pk=None):
        try:
            obj = EmpModels.objects.get(pk=pk)
            serializer_obj = EmpModelsSerializer(obj)
            return Response({"data": serializer_obj.data},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"data": "object does not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "internal server error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg": "internal server error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=False, permission_classes=[], authentication_classes=[], url_path="create")
    def create_employee(self, request):
        try:
            data = request.data
            emp_name = data.get("emp_name")
            emp_designation = data.get("emp_designation")
            address = data.get("address")
            city = data.get("city")
            mobile = data.get("mobile")
            if emp_name:
                if emp_designation:
                    if address:
                        if city:
                            if mobile:
                                obj = EmpModels(emp_name=emp_name,
                                                emp_designation=emp_designation,
                                                address=address,
                                                city=city,
                                                mobile=mobile)
                                obj.save()
                                return Response({"msg": "data saved successfully"},
                                                status=status.HTTP_201_CREATED)
                            else:
                                return Response({"msg": "mobile is required"},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"msg": "city is required"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"msg": "address is required"},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"msg": "emp desigmnation is required"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"msg": "emp desigmnation is required"},
                                status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"data": "object does not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "internal server error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg": "internal server error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(methods=['post'], detail=True, permission_classes=[], authentication_classes=[], url_path="update")
    def update_employee(self, request, pk=None):
        try:
            data = request.data
            emp_name = data.get("emp_name")
            emp_designation = data.get("emp_designation")
            address = data.get("address")
            city = data.get("city")
            mobile = data.get("mobile")
            obj = EmpModels.objects.get(pk=pk)
            if emp_name:
                obj.emp_name = emp_name
            if emp_designation:
                obj.emp_designation = emp_designation
            if address:
                obj.address = address
            if city:
                obj.city = city
            if mobile:
                print("check point 1")
                obj.mobile = mobile
            obj.save()
            return Response({"msg": "profile update successfully"}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"data": "employee details does not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "internal server error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg": "internal server error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True, permission_classes=[], authentication_classes=[], url_path="delete")
    def delete_employee(self, request, pk=None):
        try:
            obj = EmpModels.objects.get(pk=pk)
            obj.delete()
            return Response({"msg": "profile delete successfully"}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"data": "employee details does not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "internal server error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg": "internal server error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



