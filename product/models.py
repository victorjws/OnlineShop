from django.db import models


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

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = '상품'
        verbose_name_plural = '상품'
