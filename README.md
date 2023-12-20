# Autopart_py

class orders(models.Model):
  order_id = models.CharField(max_length=100,blank=True)
  customer = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
  def __str__(self) -> str:
    return f"{self.customer.username}"

class orderDetail(models.Model):
  product = models.ForeignKey(product,on_delete=models.CASCADE)
  order = models.ForeignKey(orders,on_delete=models.CASCADE)
  amount = models.IntegerField()

  def __str__(self) -> str:
    return f"{self.product.product_name} : {self.amount}"


@login_required(login_url="login")
def cart(req):
    count = 0
    total = 0
    try:
        cart = orders.objects.get(order_id=create_cart(req),customer=req.user)
        cartDetail = orderDetail.objects.filter(order=cart)
        for i in cartDetail:
            count += i.amount
            total += i.product.price * i.amount
    except:
        cart= None
        cartDetail=None
    print(cartDetail)
    return render(req,"cart.html",{'count':count,'total':total,'cartDetail':cartDetail})

def create_cart(req):
    cart = req.session.session_key
    if not cart:
        cart.req.session.create()
    return cart

@login_required(login_url="login")
def add_cart(req,id):
    product = Product.objects.get(pk=id)
    try:  #กรณีมี order อยู่แล้ว
        order = orders.objects.get(order_id=create_cart(req))
    except orders.DoesNotExist: #กรณีไม่มี order
        order = orders.objects.create(
            order_id= create_cart(req),
            customer= req.user
        )
        order.save()
    try: #ถ้าสั่งซำ้ จะเพิ่มสินค้าตัวนั้น
        orderdetail = orderDetail.objects.get(product=product,order=order)
        if orderdetail.amount < orderdetail.product.stock:
            orderdetail.amount += 1
            orderdetail.save()
            return redirect(home)
    except orderDetail.DoesNotExist: #ถ้าไม่เคยสั่งจะ set ค่า amount เป็น 1
        orderdetail = orderDetail.objects.create(
            product=product,
            order = order,
            amount = 1,
        )
        orderdetail.save()
        return redirect(home)
    print(orderdetail)
    return render(req,"cart.html")

@login_required
def delete_cart(req,id):
    product = Product.objects.get(pk=id)
    order = orders.objects.get(order_id=create_cart(req),customer=req.user)
    cartDetail=orderDetail.objects.get(product=product,order=order)
    cartDetail.delete()
    return redirect("/cart")


urls.py
    path('cart',views.cart,name='cart'),
    path('cart/add/<int:id>',views.add_cart,name='addcart'),
    path('cart/delete/<int:id>',views.delete_cart,name='delete_cart'),
