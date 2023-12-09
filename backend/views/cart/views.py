from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from backend.models import CartModel, Product, Category, CategoryForProduct
from backend.views.cart.serializers import AddProductSerializer
from backend.views.cart.utils import UtilCart


class CartView(APIView):
    """"""

    permission_classes = [IsAuthenticated]
    db_worker = UtilCart
    serializer = AddProductSerializer

    def __post_and_put(self, request: Request):
        """method for post/put requests"""

        # control data(body) from request
        serializer = self.serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # add products for user and return it
        util = self.db_worker(request)
        return Response(data=util.add_product_cart(request.data))

    def get(self, request: Request):
        util = self.db_worker(request)
        return Response(data=util.get_products_by_user())

    def post(self, request: Request):
        return self.__post_and_put(request)

    def put(self, request: Request):
        return self.__post_and_put(request)

    def delete(self, request: Request):

        # control data(body) from request
        serializer = self.serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        util = self.db_worker(request)
        return Response(data=util.delete_product_cart(request.data))
