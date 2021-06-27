from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from user.models import Usert
from tag.models import Tag
from .models import Board, Comment
from .forms import BoardForm, BoardUpdateForm
from user.decorators import *

# Create your views here.


class BoardDetailView(DetailView):
    template_name = "board_detail.html"
    # queryset = Board.objects.all() # model의 선언 동작과 동일함
    # model = Board
    context_object_name = "board"

    # get_object와 model 선언시 동작에 대한 성능은 차후 평가가 필요하다
    # def get_object(self, queryset=None):
    #     return Board.objects.get(pk=self.kwargs.get("pk"))

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Board, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = {"board": self.kwargs.get("pk"), "is_deleted": False}
        context["comments"] = Comment.objects.filter(**args)
        return context


class BoardListView(ListView):
    model = Board
    paginate_by = 3
    paginate_orphans = 1
    ordering = "-id"
    template_name = "board_list.html"
    context_object_name = "boards"


@method_decorator(login_required, name="dispatch")
class BoardUpdateView(UpdateView):
    model = Board
    form_class = BoardUpdateForm
    template_name = "board_update.html"

    def form_valid(self, form):
        user_id = self.request.session.get("user")

        # 작성자 확인 custom user table을 사용했기에 별도 검사가 필요함
        if user_id != int(self.object.writer_id):
            err_msg = "글을 작성한 본인만 수정할 수 있습니다."
            return render(
                self.request, "board_detail.html", {"board": self.object, "err_msg": err_msg}
            )

        # photo 데이터를 삭제하는 경우
        self.object = form.save(commit=False)
        if form.cleaned_data["photo"] == None:
            self.object.photo = "default/no_img_lg.png"

        # DB에 실재로 저장함
        self.object.save()

        # tag 작업
        tags = form.cleaned_data["tags"].split(",")

        # for tag in tags:
        #     if not tag:
        #         continue

        #     # _tag, created = Tag.objects.get_or_create(name=tag)
        #     _tag, _data = Tag.objects.get_or_create(name=tag.strip())
        #     #  '_XXXX'는 protected를 의미함
        #     #  '_'는 사용하지 않는 변수를 의미함
        #     # Tag.objects.get_or_create(name=tag)는 가지고 있으면 가져오고 없으면 생성함
        #     # 이름과 작성자가 모두 똑같은 사람이 하고 싶다면 Tag.objects.get_or_create(name=tag, writer=writer)
        #     # 이름과 작성자가 다르면 새로 만듬
        #     # 이름만 확인하고 작성자가 없으면 기본값으로 생성
        #     # Tag.objects.get_or_create(name=tag, defaults={'wr'})
        #     self.object.tags.add(_tag)

        # stackoverflow의 code 참조

        for new_tag in tags:
            if not new_tag:
                continue

            _tag, _data = Tag.objects.get_or_create(name=new_tag.strip())
            self.object.tags.add(_tag)

        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self, *args, **kwargs):
    #     print("self : ", dir(self))
    #     return self.instance.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board_key"] = self.kwargs.get("pk")
        return context


@method_decorator(login_required, name="dispatch")
class BoardDeleteView(DeleteView):
    model = Board
    success_url = reverse_lazy("board:board_list")


class BoardWriteView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardUpdateForm  # createview should only use modelform class.
    template_name = "board_write.html"
    # context_object_name = 'form' # need get_object

    # def get_object(self):
    #     id_ = self.kwargs.get("pk")
    #     return get_object_or_404(Board, id=id_)

    def form_valid(self, form):

        # photo 데이터를 삭제하는 경우
        self.object = form.save(commit=False)
        if form.cleaned_data["photo"] == None:
            self.object.photo = "default/no_img_lg.png"

        self.object.writer = Usert.objects.get(pk=self.request.session.get("user"))

        # DB에 실재로 저장함
        self.object.save()

        # tag 작업
        tags = form.cleaned_data["tags"].split(",")

        # for tag in tags:
        #     if not tag:
        #         continue

        #     # _tag, created = Tag.objects.get_or_create(name=tag)
        #     _tag, _data = Tag.objects.get_or_create(name=tag.strip())
        #     #  '_XXXX'는 protected를 의미함
        #     #  '_'는 사용하지 않는 변수를 의미함
        #     # Tag.objects.get_or_create(name=tag)는 가지고 있으면 가져오고 없으면 생성함
        #     # 이름과 작성자가 모두 똑같은 사람이 하고 싶다면 Tag.objects.get_or_create(name=tag, writer=writer)
        #     # 이름과 작성자가 다르면 새로 만듬
        #     # 이름만 확인하고 작성자가 없으면 기본값으로 생성
        #     # Tag.objects.get_or_create(name=tag, defaults={'wr'})
        #     self.object.tags.add(_tag)

        # stackoverflow의 code 참조

        for new_tag in tags:
            if not new_tag:
                continue

            _tag, _data = Tag.objects.get_or_create(name=new_tag.strip())
            self.object.tags.add(_tag)

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
@method_decorator(require_POST, name="dispatch")
class CommentWriteView(View):
    def post(self, request, *args, **kwargs):
        errors = []

        post_id = request.POST.get("post_id", "").strip()
        content = request.POST.get("content", "").strip()

        if not content:
            errors.append("댓글을 입력해주세요.")

        if not errors:
            comment = Comment.objects.create(
                board=Board.objects.get(pk=post_id),
                user=Usert.objects.get(pk=request.session.get("user")),
                content=content,
                parent_comment=None,
            )

            return redirect(reverse("board:board_detail", kwargs={"pk": post_id}))

        return render(
            request, "blogs/post_detail.html", {"user": request.user, "cmt_errors": errors}
        )


# bug : 다른 사용자 로그인시 로그인 창으로 이동됨.
# 원래대로라면 내부 로직에서 글 작성자인지 여부를 검사하는 항목에서 걸러져야함
# 원인으로 django user를 사용하지 않고 custom user table을 사용했기 때문임 : 따로 구현하는 것이 맞음
class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        errors = []

        try:
            comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        except Board.DoesNotExist:
            raise Http404("게시 댓글을 찾을 수 없습니다")

        user_id = request.session.get("user")
        user = Usert.objects.get(pk=user_id)

        if user == comment.user:
            comment.delete()
        else:
            errors.append("글을 작성한 본인만 삭제할 수 있습니다.")

        comments = Comment.objects.filter(board=comment.board.id, is_deleted=False)
        return render(
            request,
            "board_detail.html",
            {"board": comment.board, "comments": comments, "err_msg": errors},
        )


@method_decorator(login_required, name="dispatch")
class LikesView(View):
    def get(self, request, *args, **kwargs):
        try:
            like_blog = get_object_or_404(Board, pk=self.kwargs.get("pk"))
        except Board.DoesNotExist:
            raise Http404("게시글을 찾을 수 없습니다")

        user_id = request.session.get("user")
        # item = like_blog.like.values_list("id")

        if like_blog.like.filter(id=user_id):
            like_blog.like.remove(user_id)
            like_blog.like_count -= 1
            like_blog.save()
        else:
            like_blog.like.add(user_id)
            like_blog.like_count += 1
            like_blog.save()

        return redirect("board:board_detail", pk=self.kwargs.get("pk"))
