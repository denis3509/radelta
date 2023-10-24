from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from delivery import views

urlpatterns = [
    path('api/delivery/package-type-list/', views.PackageTypeList.as_view()),
    path('api/delivery/package/', views.Package.as_view()),
    path('api/delivery/package-async/', views.PackageAsync.as_view()),
    path('api/delivery/package/<int:pk>/', views.Package.as_view()),
    path('api/delivery/package-list/', views.PackageList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
