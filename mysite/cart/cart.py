# Cart-creating a session
class Cart:
    """first it will create session and then it will create cart"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": quantity,
                "price": str(product.price),
            }
        else:
            self.cart[product_id]["quantity"] += quantity

        self.session.modified = True

    def __len__(self):
        return sum(int(item["quantity"] for item in self.cart.values()))

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = float(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item