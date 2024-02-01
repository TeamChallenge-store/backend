from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer

class ProductListView(APIView):
    """"Вивід списку продуктів"""
    def get(self, request):

        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)

        products = Product.objects.all()

        if min_price is not None:
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            products = products.filter(price__lte=max_price)

        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    """"Вивід детального списку продуктів"""
    
    def get(self, request, id):
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)











class CartView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def post(self, request, *args, **kwargs):
        # Отримати назву товару з запиту
        product_name = request.data.get('name')

        # Перевірити, чи існує товар з такою назвою
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        # Додати товар до корзини (в даному випадку, просто вивести інформацію про товар)
        response_data = {
            'message': 'Product added to the cart',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
            }
        }

        return Response(response_data)

    def delete(self, request, *args, **kwargs):
        # Отримати ідентифікатор товару з запиту для видалення
        product_id = request.data.get('product_id')

        # Перевірити, чи існує товар з таким ідентифікатором
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        # Видалити товар з корзини
        product.delete()

        return Response({'message': 'Product removed from the cart'})
