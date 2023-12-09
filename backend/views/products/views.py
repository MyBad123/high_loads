from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from backend.views.products.serializers import QuerySerializer
from backend.views.products.utils import ProductUtil, CategoryUtils


class ProductList(APIView):
    """get list of products"""

    util = ProductUtil

    def post(self, request: Request):
        """api method for getting products"""

        return Response(data=self.util(request).get_products())


class ProductSingleView(APIView):
    """view for single product"""

    util = ProductUtil

    def get(self, request: Request):
        """api method for getting object"""

        # control user's data
        if QuerySerializer(data={'pk': request.query_params.get('id')}).is_valid():

            # control product obj with this id
            util_product = self.util(request).get_single_product(request.query_params.get('id'))
            if util_product:
                return Response(data=util_product)

        return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryTreeView(APIView):
    """make tree with category and it's products"""

    util = CategoryUtils

    def get(self, request: Request):
        return Response(data=self.util.get_tree())
