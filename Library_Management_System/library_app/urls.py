from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminSignupView, admin_login, BookViewSet, student_view

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('admin/signup/', AdminSignupView.as_view(), name='admin_signup'),
    path('admin/login/', admin_login, name='admin_login'),
    path('student/books/', student_view, name='student_books'),
    path('', include(router.urls)),
]

