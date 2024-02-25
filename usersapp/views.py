from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.
def login(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        if username == "" or password=="":
            messages.warning(req,"กรุณาป้อนข้อมูลให้ครบ")
            return redirect("/login")
        else:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(req,user)
                if user.has_perm('admin'):
                    return redirect('/dashboard')
                return redirect('/')
            else:
                messages.warning(req,"ไม่พบบัญชีผู้ใช้")
                return redirect('/login')
    return render(req,'login.html')
def register(req):
    if req.method == "POST":
        username = req.POST["username"]
        email = req.POST["email"]
        password = req.POST["password"]
        password2 = req.POST["password2"]
        if username=='' or email=='' or password=='' or password2=='':
            messages.warning(req,'กรุณาป้อนข้อมูลให้ครบ')
            return redirect("/register")
        elif password != password2:
            messages.warning(req,'รหัสผ่านไม่ตรงกัน')
            return redirect("/register")
        else:
            if User.objects.filter(username=username).exists():
                messages.warning(req,"ชื่อผู้ใช้นี้มีอยู่แล้ว")
                return redirect("/register")
            else:
                user=User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
                messages.success(req,'สร้างผู้ใช้เรียบร้อย')
                return redirect("/login")
    return render(req,'register.html')
def logout(req):
    auth.logout(req)
    return redirect("/")
