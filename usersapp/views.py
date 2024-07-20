from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from custom.check_order import user_is_worker
from usersapp.forms import ProfileForm
from usersapp.models import UserProfile
# Create your views here.
def login(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        if username == "" or password=="":
            messages.warning(req,"กรุณากรอกข้อมูลให้ครบ")
            return redirect("/login")
        else:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(req,user)
                if user.is_superuser:
                    return redirect('/dashboard')
                elif user.is_staff:
                    return redirect('/calendar')
                return redirect('/')
            else:
                messages.warning(req,"ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                return redirect('/login')
    return render(req,'login.html')



def register(req):
    if req.method == "POST":
        username = req.POST["username"]
        email = req.POST["email"]
        password = req.POST["password"]
        password2 = req.POST["password2"]
        if username=='' or email=='' or password=='' or password2=='':
            messages.warning(req,'กรุณากรอกข้อมูลให้ครบ')
            return redirect("/register")
        elif password != password2:
            messages.warning(req,'รหัสผ่านไม่ตรงกัน')
            return redirect("/register")
        else:
            if User.objects.filter(username=username).exists():
                messages.warning(req,"ชื่อผู้ใช้นี้มีอยู่แล้ว")
                return redirect("/register")
            elif User.objects.filter(email=email).exists():
                messages.warning(req,"อีเมลนี้ถูกใช้แล้ว")
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

@login_required(login_url="/login")
def user_profile(req):
    user_obj = User.objects.get(pk=req.user.id)
    try:
        if req.method == "POST":
            profile = UserProfile.objects.get(user=req.user.id)
            form = ProfileForm(req.POST,req.FILES,instance=profile)
            if form.is_valid():
                form.instance.owner = req.user
                form.save()
                return redirect('/')
        else:
            profile = UserProfile.objects.get(user=req.user.id)
            form = ProfileForm(instance=profile)
        return render(req,'user_profile.html',{'profile':profile,'form':form})
    except:
        if req.method == "POST":
            profile = UserProfile.objects.create(
                image= req.FILES['image'],
                firstname = req.POST['firstname'],
                lastname = req.POST['lastname'],
                address = req.POST['address'],
                phone = req.POST['phone'],
                user = user_obj
            )
            profile.save()
            return redirect('/')
        return render(req,"create_profile.html")


