from django.shortcuts import render
from rest_framework import generics

from .serializer import RegisterSerializer


class CustomerRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return render(request, template_name='customer/register.html')
