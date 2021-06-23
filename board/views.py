from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import Http404
from user.models import Usert
from tag.models import Tag
from .models import Board, Comment
from .forms import BoardForm, BoardUpdateForm
from user.decorators import *

# Create your views here.


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
        comments = Comment.objects.filter(board=pk, is_deleted=False)
    except (Board.DoesNotExist, Comment.DoesNotExist):
        raise Http404("게시글을 찾을 수 없습니다")

    return render(request, "board_detail.html", {"board": board, "comments": comments})


@login_required
def board_update(request, pk):
    try:
        # board = Board.objects.get(pk=pk)
        board = get_object_or_404(Board, pk=pk)
    except Board.DoesNotExist:
        raise Http404("게시글을 찾을 수 없습니다")

    user_id = request.session.get("user")
    usert = Usert.objects.get(pk=user_id)

    if usert != board.writer:
        err_msg = "글을 작성한 본인만 수정할 수 있습니다."
        return render(request, "board_detail.html", {"board": board, "err_msg": err_msg})

    if request.method == "POST":
        form = BoardUpdateForm(request.POST or None, request.FILES or None, instance=board)
        if form.is_valid():
            user_id = request.session.get("user")
            usert = Usert.objects.get(pk=user_id)
            tags = form.cleaned_data["tags"].split(",")

            board.title = form.cleaned_data["title"]
            board.contents = form.cleaned_data["contents"]
            board.writer = usert
            if form.cleaned_data["photo"] == None:
                board.photo = "default/no_img_lg.png"
            elif form.cleaned_data["photo"] != board.photo:
                board.photo = form.cleaned_data["photo"]
            else:
                pass
            board.save()
            # 보드 생성 이후 pk가 만들어지고 나서 만들어야 에러 발생이 안됨
            for tag in tags:
                if not tag:
                    continue

                # _tag, created = Tag.objects.get_or_create(name=tag)
                _tag, _data = Tag.objects.get_or_create(name=tag.strip())
                #  '_XXXX'는 protected를 의미함
                #  '_'는 사용하지 않는 변수를 의미함
                # Tag.objects.get_or_create(name=tag)는 가지고 있으면 가져오고 없으면 생성함
                # 이름과 작성자가 모두 똑같은 사람이 하고 싶다면 Tag.objects.get_or_create(name=tag, writer=writer)
                # 이름과 작성자가 다르면 새로 만듬
                # 이름만 확인하고 작성자가 없으면 기본값으로 생성
                # Tag.objects.get_or_create(name=tag, defaults={'wr'})
                board.tags.add(_tag)
            return redirect("board_detail", pk=pk)
        else:
            print(form.errors)
    form = BoardUpdateForm(instance=board)
    # ModelForm에서는 initial이 아닌 instance로 객체를 전달해야한다.
    """form = BoardUpdateForm(
        initial={
            "title": board.title,
            "contents": board.contents,
            "tags": [tag.name for tag in board.tags.all()],
            "photo": board.photo,
        }
    )"""
    return render(request, "board_update.html", {"form": form, "board": board})


@login_required
def board_delete(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404("게시글을 찾을 수 없습니다")

    if not request.session.get("user"):

        err_msg = "로그인을 한 사용자만 글을 삭제할 수 있습니다."
        return render(request, "board_detail.html", {"board": board, "err_msg": err_msg})

    user_id = request.session.get("user")
    usert = Usert.objects.get(pk=user_id)

    if usert == board.writer:
        Board.objects.get(pk=pk).delete()
    else:
        err_msg = "글을 작성한 본인만 삭제할 수 있습니다."
        return render(request, "board_detail.html", {"board": board, "err_msg": err_msg})
    return redirect("/board/list/")


@login_required
def board_write(request):
    if not request.session.get("user"):
        return redirect("/login/")

    if request.method == "POST":
        form = BoardForm(request.POST, request.FILES or None)
        if form.is_valid():
            user_id = request.session.get("user")
            usert = Usert.objects.get(pk=user_id)
            tags = form.cleaned_data["tags"].split(",")

            board = Board()
            board.title = form.cleaned_data["title"]
            board.contents = form.cleaned_data["contents"]
            board.writer = usert
            board.photo = form.cleaned_data["photo"]
            if board.photo == None:
                board.photo = "default/no_img_lg.png"
            board.save()

            # 보드 생성 이후 pk가 만들어지고 나서 만들어야 에러 발생이 안됨
            for tag in tags:
                if not tag:
                    continue

                # _tag, created = Tag.objects.get_or_create(name=tag)
                _tag, _ = Tag.objects.get_or_create(name=tag.strip())
                #  '_XXXX'는 protected를 의미함
                #  '_'는 사용하지 않는 변수를 의미함
                # Tag.objects.get_or_create(name=tag)는 가지고 있으면 가져오고 없으면 생성함
                # 이름과 작성자가 모두 똑같은 사람이 하고 싶다면 Tag.objects.get_or_create(name=tag, writer=writer)
                # 이름과 작성자가 다르면 새로 만듬
                # 이름만 확인하고 작성자가 없으면 기본값으로 생성
                # Tag.objects.get_or_create(name=tag, defaults={'wr'})
                board.tags.add(_tag)

            return redirect("/board/list/")
    else:
        form = BoardForm()

    return render(request, "board_write.html", {"form": form})


def board_list(request):
    all_boards = Board.objects.all().order_by("-id")
    # -id 역순, 최신순으로 가져오겠다는 옵션
    page = int(request.GET.get("p", 1))
    paginator = Paginator(all_boards, 3)

    boards = paginator.get_page(page)
    return render(request, "board_list.html", {"boards": boards})


@login_required
def likes(request, pk):
    try:
        like_blog = get_object_or_404(Board, pk=pk)
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

    return redirect("board_detail", pk=pk)


@login_required
def comment_write(request):
    errors = []
    if request.method == "POST":
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

            return redirect(reverse("board_detail", kwargs={"pk": post_id}))

    return render(request, "blogs/post_detail.html", {"user": request.user, "cmt_errors": errors})
    # return render(request, "board_detail.html", {"board": board, "err_msg": err_msg})


@login_required
def comment_delete(request, pk):
    errors = []
    try:
        comment = Comment.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404("게시 댓글을 찾을 수 없습니다")

    user_id = request.session.get("user")
    user = Usert.objects.get(pk=user_id)

    if user == comment.user:
        # Comment.objects.get(pk=pk).delete()
        comment.delete()
    else:
        errors.append("글을 작성한 본인만 삭제할 수 있습니다.")

    comments = Comment.objects.filter(board=comment.board.id, is_deleted=False)
    return render(
        request,
        "board_detail.html",
        {"board": comment.board, "comments": comments, "err_msg": errors},
    )
