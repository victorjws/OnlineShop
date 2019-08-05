from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from customer.models import Customer


@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status=status)


class CustomerLoginView(BaseView):
    def get(self, request):
        return render(request, template_name='customer/login.html')

    def post(self, request):
        email = request.data['email']
        if not email:
            return self.resposne(message='아이디를 입력해주세요', status=400)
        password = request.data['password']
        if not password:
            return self.response(message='패스워드를 입력해주세요.', status=400)
        customer = authenticate(request, email=email, password=password)
        if customer is None:
            return self.response(message='입력 정보를 확인해주세요.', status=400)
        login(request, customer)
        return self.response()


class CustomerLogoutView(BaseView):
    def get(self, request):
        logout(request)
        return self.response()


class CustomerRegisterView(BaseView):
    def get(self, request):
        return render(request, template_name='customer/register.html')

    def post(self, request):
        # email = request.data['email']
        email = request.POST.get('email')
        if not email:
            return self.resposne(message='아이디를 입력해주세요', status=400)
        # password = request.data['password']
        password = request.POST.get('password')
        if not password:
            return self.response(message='패스워드를 입력해주세요.', status=400)
        try:
            validate_email(email)
        except ValidationError:
            return self.response(message='올바른 이메일을 입력해주세요.', status=400)
        try:
            customer = Customer.objects.create_user(email, password)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.', status=400)
        return self.response({'user.email': customer.email})
