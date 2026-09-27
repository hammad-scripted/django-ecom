# Cart-creating a session
class Cart:
    """ first it will create session and then it will create cart"""
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product,quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": quantity,
                "price": str(product.price),
            }
        else:
            self.cart[product_id]["quantity"] += quantity

        self.session.modified = True
