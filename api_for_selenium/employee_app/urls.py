from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'employee_api', views.EmployeeApi, basename="employee_api")


urlpatterns = router.urls