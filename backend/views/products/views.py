from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from backend.models import Product, CategoryForProduct
from backend.views.products.serializers import QueryProductSerializer, QuerySerializer, ProductWithCategorySerializer


class ProductList(APIView):
    """get list of products"""

    serializer_data: ReturnList
    serializer_class = ProductWithCategorySerializer

    def make_request_data(self):
        """make data for return in request"""

        data = {}

        # control unique
        for i in self.serializer_data:
            if data.get(i['product']['id']):
                data[i['product']['id']]['category'].append(i['category']['name'])
            else:
                data.update({i['product']['id']: {
                    'id': i['product']['id'],
                    'name': i['product']['name'],
                    'about': i['product']['about'],
                    'price': i['product']['price'],
                    'category': [i['category']['name']]
                }})

        # make normal struct for data
        return_data = []
        for i in data.keys():
            return_data.append(data[i])

        return return_data

    def get_queryset(self):
        # make base queryset
        product_objs = CategoryForProduct.objects.all()

        # work with sorting
        sort_params = {
            'min': self.request.query_params.get('min'),
            'max': self.request.query_params.get('max'),
            'sort': self.request.query_params.get('sort')
        }
        if QueryProductSerializer(data=sort_params).is_valid():
            if sort_params.get('min'):
                product_objs = product_objs.filter(product__price__gte=sort_params.get('min'))

            if sort_params.get('max'):
                product_objs = product_objs.filter(product__price__lte=sort_params.get('max'))

            if sort_params.get('sort') == 'min-max':
                product_objs = product_objs.order_by('product__price')
            elif sort_params.get('sort') == 'max-min':
                product_objs = product_objs.order_by('-product__price')

        return product_objs

    def post(self, request: Request):
        """api method for getting products"""

        serializer = self.serializer_class(self.get_queryset(), many=True)
        self.serializer_data = serializer.data

        return Response(data=self.make_request_data())


class ProductSingleView(APIView):
    """view for single product"""

    id_product: int
    product: Product

    def get_product_pk(self):
        try:
            return Product.objects.get(id=self.id_product)
        except Product.DoesNotExist:
            raise None

    def get(self, request: Request):
        """api method for getting object"""

        # control user's data
        self.id_product = request.query_params.get('id')
        if QuerySerializer(data={'pk': self.id_product}).is_valid():

            # control product obj with this id
            self.product = self.get_product_pk()
            if self.product:
                return Response(data=ProductSerializer(self.product).data)

        return Response(status=status.HTTP_404_NOT_FOUND)
