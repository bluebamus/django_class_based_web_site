from django.db import models


class Usert(models.Model):
    username = models.CharField(max_length=32, verbose_name="사용자명")
    useremail = models.EmailField(max_length=128, verbose_name="사용자이메일")
    password = models.CharField(max_length=64, verbose_name="비밀번호")
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "usert"
        verbose_name = "사용자 테이블"
        verbose_name_plural = "사용자 테이블"


# class user_profile(models.Model):
#     def __str__(self):
#         return self.username

#     class Meta:
#         db_table = "user_profile"
#         verbose_name = "패스트캠퍼스 사용자"
#         verbose_name_plural = "패스트캠퍼스 사용자들"


# class user_AbstractUser(models.Model):
#     def __str__(self):
#         return self.username

#     class Meta:
#         db_table = "user_abstractuser"
#         verbose_name = "패스트캠퍼스 사용자"
#         verbose_name_plural = "패스트캠퍼스 사용자들"


# class user_AbstractBaseUser(models.Model):
#     def __str__(self):
#         return self.username

#     class Meta:
#         db_table = "user_abstractbaseUser"
#         verbose_name = "패스트캠퍼스 사용자"
#         verbose_name_plural = "패스트캠퍼스 사용자들"
