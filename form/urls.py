from django.urls import path
from . import views

app_name = 'form'

urlpatterns = [
    path("" , views.main_dashbord , name = 'index'),
    path("/myform/" , views.my_form , name = 'myform'),
    path("create-form/", views.create_form , name = 'create-form'),
    path("delete-form/<str:form>/" , views.delete_form , name = 'delete-form'),
    path("<str:form>/" , views.form_details , name = 'form_details'),
    
    path("view-form/<uuid:form>/", views.view_form , name = 'view-form'),
    path("submit-form'/<str:form>/", views.submit_form , name = 'submit-form'),
    path("<str:form>/<str:submission>/submissions/", views.view_all_submission , name='all_submission'),
]