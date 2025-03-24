from rest_framework import generics, permissions, viewsets, status 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.db import IntegrityError

from .models import Admin, Book
from .serializers import AdminSerializer, BookSerializer

class AdminSignupView(generics.CreateAPIView):
    """API endpoint for admin signup"""
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': 'Admin with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def admin_login(request):
    """API endpoint for admin login and JWT token generation"""
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        admin = Admin.objects.get(email=email)
        if admin.check_password(password):
            refresh = RefreshToken.for_user(admin)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({'error': 'Invalid credentials'}, status=400)
    except Admin.DoesNotExist:
        return Response({'error': 'Admin not found'}, status=404)

class BookViewSet(viewsets.ModelViewSet):
    """API ViewSet for managing books (CRUD)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

def student_view(request):
    """Renders the list of books for students"""
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})
