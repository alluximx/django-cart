import datetime
import models

CART_ID = 'CART-ID'


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class Cart:
    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        return cart

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else:  # ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity = item.quantity + int(quantity)
            item.save()

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:  # ItemAlreadyExists
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = int(quantity)
                item.save()

    def count(self):
        result = 0
        for item in self.cart.item_set.all():
            result += 1 * item.quantity
        return result
        
    def summary(self):
        result = 0
        for item in self.cart.item_set.all():
            result += item.total_price
        return result

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()
