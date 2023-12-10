from django.contrib.auth.models import User
from rest_framework.request import Request
from backend.models import CartModel, CategoryForProduct, Category, Product, OrderModel, ProductsInOrderModel


class UtilProduct:
    def __init__(self, request: Request):
        self.request = request

    @staticmethod
    def get_category_product(product: Product):
        values = CategoryForProduct.objects.filter(product=product).values_list('category_id', flat=True)

        return {
            'id': product.id,
            'about': product.about,
            'price': product.price,
            'category': [i.name for i in Category.objects.filter(id__in=values)]
        }

    def get_products_by_user(self):
        """get all products by user"""

        products = CartModel.objects.filter(user=self.request.user)
        return [UtilProduct.get_category_product(i.product) for i in products]


class UtilCart(UtilProduct):
    def __init__(self, request: Request):
        super().__init__(request)

    def add_product_cart(self, id_product: list) -> list:
        """"""

        for i in id_product:
            try:
                product = Product.objects.get(id=i)
                CartModel.objects.create(product=product, user=self.request.user)
            except (ValueError, Product.DoesNotExist):
                pass

        return super().get_products_by_user()

    def delete_product_cart(self, id_product: list) -> list:
        """"""

        for i in id_product:
            try:
                product = Product.objects.get(id=i)

                delete_obj = CartModel.objects.get(product=product, user=self.request.user)
                delete_obj.delete()
            except (ValueError, Product.DoesNotExist):
                pass

        return super().get_products_by_user()


class CartUtils:
    """"""

    def __init__(self, request: Request):
        self.query_set = CartModel.objects.filter(user=request.user)
        self.user = request.user

    def cart_is_empty(self) -> bool:
        return False if len(self.query_set) else True

    def make_ordering(self) -> dict:
        ordering = OrderModel.objects.create(user=self.user)

        for i in self.query_set:
            ProductsInOrderModel.objects.create(order=ordering, product=i.product)

        returned_data = {
            'ordering_id': ordering.id,
            'products': [UtilProduct.get_category_product(i.product) for i in self.query_set]
        }

        # delete all objects from cart of user
        for i in self.query_set:
            i.delete()

        return returned_data
