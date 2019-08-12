from rest_framework import pagination


class ProductPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
