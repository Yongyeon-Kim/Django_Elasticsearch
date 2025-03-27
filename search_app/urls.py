from django.contrib import admin
from django.urls import path
from search_app import views  # 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search, name='home'),  # 루트 경로도 검색 뷰에 연결
    path('search/', views.search, name='search'),
]