from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomerManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('이메일이 필요')
        email = self.normalize_email(email)
        customer = self.model(email=email, **extra_fields)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer


class Customer(AbstractBaseUser):
    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True)
    # password = models.CharField(verbose_name='비밀번호', max_length=128)
    # level = models.CharField(verbose_name='등급', max_length=8,
    #                          choices=(('admin', 'admin'), ('user', 'user')))
    register_date = models.DateTimeField(verbose_name='등록날짜',
                                         auto_now_add=True)
    shipping_address = models.TextField(verbose_name='배송주소')

    objects = CustomerManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return "<%d %s>" % (self.pk, self.email)

    class Meta:
        db_table = 'customer'
        verbose_name = '고객'
        verbose_name_plural = '고객'
