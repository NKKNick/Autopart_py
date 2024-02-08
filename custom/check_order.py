from user_cart.models import Cart, CartDetail


def user_is_order(user):
    try:
        cart = Cart.objects.get(customer=user)
        have_Order = CartDetail.objects.filter(cart=cart)[0]     
        return True
    except :
        return False