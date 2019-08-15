from django.db import models


class Cart(models.Model):
    customer = models.ForeignKey(verbose_name='고객', to='customer.Customer',
                                 on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name='상품', to='product.Product',
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='주문수량')

    def __str__(self):
        return '고객: ' + str(self.customer) + ' ' + '상품: ' + str(
            self.product) + ' ' + '주문수량: ' + str(self.quantity)

    class Meta:
        db_table = 'cart'
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니'


class Order(models.Model):
    customer = models.ForeignKey(verbose_name='고객', to='customer.Customer',
                                 on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name='상품', to='product.Product',
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='주문수량')
    order_date = models.DateTimeField(verbose_name='주문시간', auto_now_add=True)

    def __str__(self):
        return '고객: ' + str(self.customer) + ' ' + '상품: ' + str(
            self.product) + ' ' + '주문수량: ' + str(
            self.quantity) + ' ' + '주문시간: ' + str(self.order_date)

    class Meta:
        db_table = 'order'
        verbose_name = '주문'
        verbose_name_plural = '주문'
