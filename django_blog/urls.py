"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from blog.views import CategoryViewSet, PostViewSet
from user_info.views import RegisterViewSet

# 接口注册
router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"register", RegisterViewSet, basename="register")

# 接口文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="API_title",
        default_version="v1",
        description="API_description",
        terms_of_service="",
        contact=openapi.Contact(email="xiaocao@qq.com"),
        license=openapi.License(name="GPLv3 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include((router.urls, 'api'), namespace="v1")),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 配置接口文档url
    re_path(
        r"swagger(?P<format>\.json|\.yaml)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
]
