from decimal import Decimal

from myapp.models import Product


class Cart:
    """A small session-backed cart that only stores serializable values."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not isinstance(cart, dict):
            cart = {}
        self.cart = cart

    def add(self, product, quantity=1):
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")

        product_id = str(product.pk)
        try:
            current_quantity = int(self.cart.get(product_id, {}).get("quantity", 0))
        except (AttributeError, TypeError, ValueError):
            current_quantity = 0
        new_quantity = current_quantity + quantity
        if new_quantity > product.stock:
            raise ValueError("There are not enough items in stock.")

        self.cart[product_id] = {
            "quantity": new_quantity,
            "price": str(product.price),
        }
        self.session["cart"] = self.cart
        self.session.modified = True

    def set_quantity(self, product, quantity):
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if quantity > product.stock:
            raise ValueError("There are not enough items in stock.")
        if str(product.pk) not in self.cart:
            raise ValueError("This item is not in your cart.")

        self.cart[str(product.pk)] = {
            "quantity": quantity,
            "price": str(product.price),
        }
        self.session.modified = True

    def remove(self, product_id):
        self.cart.pop(str(product_id), None)
        self.session.modified = True

    def __len__(self):
        total = 0
        for item in self.cart.values():
            try:
                total += max(0, int(item.get("quantity", 0)))
            except (AttributeError, TypeError, ValueError):
                continue
        return total

    def __iter__(self):
        product_ids = []
        for product_id in self.cart:
            try:
                product_ids.append(int(product_id))
            except (TypeError, ValueError):
                continue

        products = Product.objects.in_bulk(product_ids)
        for product_id, saved_item in self.cart.items():
            try:
                product = products.get(int(product_id))
                quantity = int(saved_item.get("quantity", 0))
            except (AttributeError, TypeError, ValueError):
                continue
            if product is None or quantity < 1:
                continue

            price = product.price
            yield {
                "product": product,
                "quantity": quantity,
                "price": price,
                "total_price": price * quantity,
                "available": product.active and product.stock >= quantity,
            }

    def get_total_price(self):
        return sum((item["total_price"] for item in self), Decimal("0.00"))
