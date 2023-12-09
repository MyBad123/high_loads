from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnList
from backend.models import Product, CategoryForProduct, Category
from backend.views.products.serializers import QueryProductSerializer, ProductSerializer


class ProductUtil:
    __products: ReturnList

    def __init__(self, request: Request):
        self.request = request

    def __get_queryset(self):
        # make base queryset
        product_objs = Product.objects.all()

        # work with sorting
        sort_params = {
            'min': self.request.data.get('min'),
            'max': self.request.data.get('max'),
            'sort': self.request.data.get('sort')
        }
        if QueryProductSerializer(data=sort_params).is_valid():
            if sort_params.get('min'):
                product_objs = product_objs.filter(price__gte=sort_params.get('min'))

            if sort_params.get('max'):
                product_objs = product_objs.filter(price__lte=sort_params.get('max'))

            if sort_params.get('sort') == 'min-max':
                product_objs = product_objs.order_by('product__price')
            elif sort_params.get('sort') == 'max-min':
                product_objs = product_objs.order_by('-product__price')

        return product_objs

    def __make_request_data(self):
        """make data for return in request"""

        data = {}
        for i in self.__products:
            data.update({i['id']: {
                'id': i['id'],
                'name': i['name'],
                'about': i['about'],
                'price': i['price'],
                'category': []
            }})

        for i in CategoryForProduct.objects.filter(product__id__in=data.keys()):
            data[i.product.id]['category'].append(i.category.name)

        return [data[i] for i in data.keys()]

    def get_products(self):
        self.__products = ProductSerializer(self.__get_queryset(), many=True).data
        return self.__make_request_data()

    def get_single_product(self, product_id: int) -> dict | None:

        # control product with this id
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

        # get category for this product
        category = CategoryForProduct.objects.filter(product=product)

        return {
            "id": product.id,
            "name": product.name,
            "about": product.about,
            "price": product.price,
            "category": [i.category.name for i in category]
        }


class CategoryUtils:

    @staticmethod
    def get_tree():
        # make requests
        category = Category.objects.all()
        products = CategoryForProduct.objects.all()

        data = {}
        for i in category:
            data.update({i.name: []})

        for i in products:
            data[i.category.name].append({
                'product_name': i.product.name,
                'product_id': i.product.id
            })

        return data
