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


class RegisterForm(forms.Form):
    username = forms.CharField(
        error_messages={"required": "사용하실 ID를 입력해 주세요."}, max_length=32, label="사용자명"
    )
    useremail = forms.EmailField(
        error_messages={"required": "이메일을 입력해주세요."}, max_length=64, label="이메일"
    )
    password = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."}, widget=forms.PasswordInput, label="비밀번호"
    )
    re_password = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."}, widget=forms.PasswordInput, label="비밀번호 확인"
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        useremail = cleaned_data.get("useremail")
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if not (username and useremail and password and re_password):
            self.add_error("username", "모든 값을 입력해야합니다.")
            self.add_error("useremail", "모든 값을 입력해야합니다.")
            self.add_error("password", "모든 값을 입력해야합니다.")
            self.add_error("re_password", "모든 값을 입력해야합니다.")
        elif (password and re_password) and (password != re_password):
            self.add_error("password", "비밀번호가 서로 다릅니다.")
            self.add_error("re_password", "비밀번호가 서로 다릅니다.")
        else:
            try:
                Usert.objects.get(username=username)
                self.add_error("username", "아이디가 이미 가입되어 있습니다.")
            except Usert.DoesNotExist:
                pass
