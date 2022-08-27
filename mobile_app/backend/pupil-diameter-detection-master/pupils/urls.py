from django.urls import path
from . import views


urlpatterns =[
    # path('get-diameter', views.PupilDiameterApi.as_view(), name='calculate_diameter'),
    # path('test',views.PupilDiameterUpdatedApi.as_view(),name='updated')
    path('detect-diameter',views.PupilDiameterUpdatedApi.as_view(),name='updated_api')
]