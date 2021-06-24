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


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get("username", None)
        useremail = request.POST.get("useremail", None)
        password = request.POST.get("password", None)
        re_password = request.POST.get("re-password", None)

        res_data = {}

        if not (username and useremail and password and re_password):
            res_data["error"] = "모든 값을 입력해야합니다."
        elif password != re_password:
            res_data["error"] = "비밀번호가 다릅니다."
        else:
            if not (Usert.objects.filter(username=username)):
                usert = Usert(
                    username=username, useremail=useremail, password=make_password(password)
                )
                usert.save()

                # 가입과 동시에 로그인 상태로 만들어주는
                request.session["user"] = usert.id
                context = {"username": username}
                return render(request, "index.html", context)
            else:
                res_data["error"] = "아이디가 이미 가입되어 있습니다."

        return render(request, "register.html", res_data)
