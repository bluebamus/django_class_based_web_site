from django.db import models
import os
from imagekit.models import ImageSpecField  # 썸네일 함수
from imagekit.processors import ResizeToFill  # 사이즈조절
from uuid import uuid4
from django.utils import timezone
from django.urls import reverse
from helpers.models import BaseModel
from user.models import Usert

# Create your models here.


def date_upload_to(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime("%Y/%m/%d")
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return "/".join(
        [
            ymd_path,
            uuid_name + extension,
        ]
    )


# def upload_to_func(instance, filename):
#     prefix = timezone.now().strftime("%Y/%m/%d")
#     file_name = uuid4().hex
#     extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
#     return "/".join(
#         [prefix, file_name, extension,]
#     )


class Board(models.Model):
    title = models.CharField(max_length=128, verbose_name="제목")
    contents = models.TextField(verbose_name="내용")
    # TextField는 길이에 제한이 없음
    writer = models.ForeignKey(Usert, on_delete=models.CASCADE, verbose_name="글쓴이")
    # models import 해서 사용하는 방법
    tags = models.ManyToManyField("tag.Tag", verbose_name="태그", blank=True)
    # app의 class명을 명시적으로 입력해서 사용하는 방법

    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")
    photo = models.ImageField(upload_to=date_upload_to, verbose_name="이미지")
    # photo = models.ImageField(upload_to=date_upload_to, blank=True, null=True, default='default/no_img_lg.png', verbose_name="이미지")

    photo_thumbnail = ImageSpecField(
        source="photo",  # 원본 IageField이름
        processors=[ResizeToFill(500, 325)],  # 사이즈 조정
        format="JPEG",  # 최종 저장 포맷
        options={"quality": 60},  # 저장 옵션
    )

    like = models.ManyToManyField(Usert, related_name="likes", blank=True)
    like_count = models.PositiveIntegerField(default=0)
    # 0 또는 양수만 받음

    def delete(self, *args, **kwargs):
        if self.photo != "default/no_img_lg.png":
            self.photo.delete()
        super().delete(*args, **kwargs)

    # def delete(self, *args, **kargs):
    #     if self.upload_files:
    #         os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
    #     super(Notice, self).delete(*args, **kargs)

    def get_absolute_url(self):
        return reverse("board:board_detail", kwargs={"pk": self.pk})
        # reverse 사용 방법 예시
        # return reverse('board:board_detail', args=[self.pk])
        # return reverse('board:board_detail')
        # return reverse('board:board_detail', args=[self.pk])
        # return reverse('board:board_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return "%s - %s - %s" % (
            self.id,
            self.title,
            self.writer,
        )

    class Meta:
        db_table = "board"
        verbose_name = "Board"
        verbose_name_plural = "Board"


class Comment(BaseModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(Usert, on_delete=models.CASCADE)
    content = models.TextField()
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    # 대댓글 기능은 fbv에서는 구현안함, cvb project에서 구현

    def __str__(self):
        return "%s - %s - %s" % (
            self.id,
            self.board,
            self.user,
        )
