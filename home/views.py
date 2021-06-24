from django.shortcuts import render, redirect
from user.models import Usert
from board.models import Board
from django.views import View

# Create your views here.
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

        return kwargs

    def get(self, *args, **kwargs):  # get요청일때 실행되는 함수
        return render(self.request, self.get_template_name(), self.get_context_data())
