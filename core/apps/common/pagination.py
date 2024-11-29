from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
        """Custom pagination class for product list."""
        page_size = 12
        page_size_query_param = 'page_size'
        max_page_size = 100

        def get_paginated_response(self, data):
            response = super().get_paginated_response(data)
            response.data['page_size'] = self.page_size

            total_pages = self.page.paginator.num_pages
            response.data['total_pages'] = total_pages

            response.data = OrderedDict([
                ('count', response.data['count']),
                ('page_size', response.data['page_size']),
                ('total_pages', response.data['total_pages']),
                ('next', response.data['next']),
                ('previous', response.data['previous']),
                ('results', response.data['results']),
            ])
            return response
