from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views import View
from django.views.generic.edit import FormView
from .models import Usert
from .forms import RegisterForm, LoginForm


# Create your views here.
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get("user"):
            del request.session["user"]

        return redirect("/")


# forms.py 사용 방법
# django의 기본 user model을 사용하지 않고 사용자가 생성한 테이블을 사용
class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        self.request.session["user"] = form.user_id

        return super().form_valid(form)


# def login(request):
#     print("request.method : ", request.method)
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             request.session["user"] = form.user_id
#             # context = {"username": form.user_name}
#             # return render(request, "index.html", context)
#             return redirect("/")
#     else:
#         form = LoginForm()

#     return render(request, "login.html", {"form": form})


# forms.py 사용 없이, 하드 코딩 하는 방법
class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        usert = Usert(
            username=form.data.get("username"),
            useremail=form.data.get("useremail"),
            password=make_password(form.data.get("password")),
        )
        usert.save()

        self.request.session["user"] = usert.id

        return super().form_valid(form)
