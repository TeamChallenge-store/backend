from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


GET_PRODUCTS_URL = reverse('product-list')
GET_BRAND_URL = reverse('brands-list')


class TestProducts(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_all_products_list(self):
        response = self.client.get(GET_PRODUCTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_product_by_id(self):
        response = self.client.get(GET_PRODUCTS_URL, kwargs={'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_product_by_rating(self):
        response = self.client.get(GET_PRODUCTS_URL, {'sort': 'rate'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_filter_by_price_asc(self):
        response = self.client.get(GET_PRODUCTS_URL, {'sort': 'price_up'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_filter_by_price_desc(self):
        response = self.client.get(GET_PRODUCTS_URL, {'sort': 'price_down'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_text_search(self):
        response = self.client.get(GET_PRODUCTS_URL, {'search': 'your_search_query'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)


class TestBrands(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_all_brand_list(self):
        response = self.client.get(GET_BRAND_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_brand_by_id(self):
        response = self.client.get(GET_BRAND_URL, kwargs={'id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)