from django import forms
from .models import Usert
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={"required": "아이디를 입력해주세요."}, max_length=32, label="사용자 이름"
    )
    password = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."}, widget=forms.PasswordInput, label="비밀번호"
    )
    # 비밀번호 형태로 폼 필드 속성을 정의함

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                usert = Usert.objects.get(username=username)
            except Usert.DoesNotExist:
                self.add_error("username", "아이디가 없습니다")
                # 예외 발생시 에러 문구 정의
                return

            if not check_password(password, usert.password):
                self.add_error("password", "비밀번호를 틀렸습니다")
            else:
                self.user_id = usert.id
                self.user_name = usert.username
