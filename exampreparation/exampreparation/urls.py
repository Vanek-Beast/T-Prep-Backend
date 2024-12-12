"""
URL configuration for exampreparation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from preparation.views import *

from exampreparation import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/<int:user_id>/subjects/', SubjectListView.as_view(), name='subject-list'),
    path('api/v1/users/<int:user_id>/subjects/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('api/v1/users/subjects/<int:subject_id>/segments/', SegmentListView.as_view(), name='segment-list'),
    path('api/v1/users/<int:user_id>/subjects/delete/<int:subject_id>/', SubjectDeleteView.as_view(), name='subject-delete'),
    path('api/v1/users/register/', UserCreateView.as_view(), name='user-create'),
    path('api/v1/users/auth/<str:user_name>/<str:user_password>/', UserAuthView.as_view(), name='user-auth'),
    path('api/v1/users/logout/', UserLogoutView.as_view(), name='user-auth'),
    path('api/v1/users/segments/update-status/<int:segment_id>/', SegmentUpdateStatusView.as_view(), name='segment-update'),
    path('api/v1/users/segments/<int:segment_id>/change-answer/', QuestionUpdateView.as_view(), name='change-question'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
