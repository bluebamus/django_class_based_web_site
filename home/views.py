from django.shortcuts import render, redirect, get_object_or_404
from user.models import Usert
from board.models import Board
from django.views import View

# Create your views here.


def home1(request):
    user_id = request.session.get("user")
    all_boards = Board.objects.all().order_by("-id")

    if user_id:
        try:
            usert = Usert.objects.get(pk=user_id)
        except Usert.DoesNotExist:
            del request.session["user"]
            return redirect("/login")
        return render(request, "index.html", {"boards": all_boards, "username": usert.username})

    return render(request, "index.html", {"boards": all_boards})
    # 이전 if로 세션 처리를 했던 내용들을 template의 home.html로 이동시킴, html에서 session 처리가 가능함!


class HomeView(View):
    model = Board
    template_name = "index.html"

    def get_object(self):
        return self.model.objects.all().order_by("-id")

    def get_template_name(self):
        return self.template_name

    def get_context_data(self, **kwargs):  # 폼에넘길 인자들 사전현태로 만들기
        kwargs["boards"] = self.get_object()
        user_id = self.request.session.get("user")
        if user_id:
            try:
                usert = Usert.objects.get(pk=user_id)
            except Usert.DoesNotExist:
                del self.request.session["user"]
                return redirect("/login")
            kwargs["username"] = usert.username

        print("kwargs :", kwargs)
        return kwargs

    def get(self, *args, **kwargs):  # get요청일때 실행되는 함수
        return render(self.request, self.get_template_name(), self.get_context_data())
