from rest_framework.generics import ListAPIView
from backend.models import Product
from backend.views.products.serializers import ProductSerializer, QueryProductSerializer


class ProductList(ListAPIView):
    """get list of products"""

    serializer_class = ProductSerializer

    def get_queryset(self):
        # make base queryset
        product_objs = Product.objects.all()

        # work with sorting
        sort_params = {
            'min': self.request.query_params.get('min'),
            'max': self.request.query_params.get('max'),
            'sort': self.request.query_params.get('sort')
        }
        if QueryProductSerializer(data=sort_params).is_valid():
            if sort_params.get('min'):
                product_objs = product_objs.filter(price__gte=sort_params.get('min'))

            if sort_params.get('max'):
                product_objs = product_objs.filter(price__gte=sort_params.get('max'))

            if sort_params.get('sort') == 'min-max':
                product_objs = product_objs.order_by('price')
            elif sort_params.get('sort') == 'max-min':
                product_objs = product_objs.order_by('-price')

        return product_objs


