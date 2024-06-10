from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from voters import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'elections', views.ElectionViewSet)
router.register(r'voting-records', views.VotingRecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/upload/', views.FileUploadView.as_view(), name='upload'),
    path('api/task/<str:task_id>/', views.TaskResultView.as_view(), name='task_status'),
    path('', views.home, name='home'),
]
