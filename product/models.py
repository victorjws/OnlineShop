from django.db import models

from customer.models import Customer


class Category(models.Model):
    name = models.CharField(verbose_name='카테고리', max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'


class Product(models.Model):
    name = models.CharField(verbose_name='상품명', max_length=256)
    price = models.IntegerField(verbose_name='상품가격')
    picture = models.ImageField(verbose_name='상품이미지', upload_to='product_img/',
                                default='product_img/no-image-icon.png')
    description = models.TextField(verbose_name='상품설명')
    stock = models.IntegerField(verbose_name='재고')
    register_date = models.DateTimeField(verbose_name='등록날짜',
                                         auto_now_add=True)
    is_discount = models.BooleanField(verbose_name='할인여부', default=False)
    discount_price = models.IntegerField(verbose_name='할인가격', blank=True,
                                         null=True)
    categories = models.ManyToManyField(
        verbose_name='카테고리',
        to=Category,
        related_name='%(app_label)s_%(class)s_related')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = '상품'
        verbose_name_plural = '상품'


class Review(models.Model):
    product = models.ForeignKey(verbose_name='상품', to=Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(verbose_name='고객', to=Customer,
                                 on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name='별점')
    contents = models.TextField(verbose_name='내용')

    def __str__(self):
        return '고객: ' + str(self.customer) + ' 상품: ' + str(
            self.product) + ' 별점: ' + str(
            self.rating) + ' 내용: ' + str(self.contents)

    class Meta:
        db_table = 'review'
        verbose_name = '상품평'
        verbose_name_plural = '상품평'