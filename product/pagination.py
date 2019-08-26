from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class ProductPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'limit_count'
    max_page_size = 50

    def get_paginated_response(self, data):
        context = self.get_html_context()

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', context['next_url']),
            ('previous', context['previous_url']),
            ('page_links', context['page_links']),
            ('results', data)
        ]))
