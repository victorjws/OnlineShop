from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from customer.models import Customer
from customer.serializer import TokenSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@method_decorator(csrf_exempt, name='dispatch')
# class BaseView(View):
class BaseView(APIView):
    @staticmethod
    def response(data={}, message='', status=status.HTTP_200_OK):
        result = {
            'data': data,
            'message': message,
        }
        return Response(data=result, status=status)


# class CustomerLoginView(BaseView):
#     def get(self, request):
#         return render(request, template_name='customer/login.html')
#
#     def post(self, request):
#         email = request.data['email']
#         print(email)
#         if not email:
#             return self.response(message='아이디를 입력해주세요',
#                                  status=status.HTTP_400_BAD_REQUEST)
#         password = request.data['password']
#         print(password)
#         if not password:
#             return self.response(message='패스워드를 입력해주세요.',
#                                  status=status.HTTP_400_BAD_REQUEST)
#         customer = authenticate(request, email=email, password=password)
#         if customer is None:
#             return self.response(message='입력 정보를 확인해주세요.',
#                                  status=status.HTTP_400_BAD_REQUEST)
#         login(request, customer)
#         return self.response()


# class LoginView(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = TokenSerializer
#     queryset = Customer.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         email = request.data['email']
#         password = request.data['password']
#         customer = authenticate(request, email=email, password=password)
#         if customer is not None:
#             login(request, customer)
#             serializer = TokenSerializer(data={
#                 "token": jwt_encode_handler(
#                     jwt_payload_handler(customer)
#                 )
#             })
#             serializer.is_valid()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

# class LoginView(JSONWebTokenAPIView):
#
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)


# class CustomerLogoutView(BaseView):
#     def get(self, request):
#         logout(request)
#         return self.response()


class CustomerRegisterView(BaseView):
    def get(self, request):
        return render(request, template_name='customer/register.html')

    def post(self, request):
        email = request.data['email']
        if not email:
            return self.resposne(message='아이디를 입력해주세요',
                                 status=status.HTTP_400_BAD_REQUEST)
        nickname = request.data['nickname']
        if not nickname:
            return self.response(message='닉네임을 입력해주세요',
                                 status=status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        if not password:
            return self.response(message='패스워드를 입력해주세요.',
                                 status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except ValidationError:
            return self.response(message='올바른 이메일을 입력해주세요.',
                                 status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.create_user(email, password)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.',
                                 status=status.HTTP_400_BAD_REQUEST)
        return self.response({'user.email': customer.email})
