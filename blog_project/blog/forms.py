# -*- coding:utf-8 -*-
from django import forms
from .models import User


class LoginForm(forms.Form):
    """
    登录Form
    """
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "请输入6-20位字符的用户名"}), max_length=50,
                               min_length=6, error_messages={"required": "用户名不能为空"}, required=True, label="用户名")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入6-20位的密码"}), max_length=20,
                               min_length=6, error_messages={"required": "密码不能为空"}, required=True, label="密码")


class RegForm(forms.Form):
    """
    注册表单
    """
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "请输入6-20位字符的用户名"}), min_length=6,
                               max_length=50, error_messages={"required": "用户名不能为空"}, required=True, label="用户名")
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "请输入有效的邮箱"}),
                             error_messages={"required": "邮箱不能为空"}, label="密码", required=True)
    url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "请输入个人网页地址", }), required=False,
                         label="网页URL")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入6-20位的密码"}), min_length=6,
                               max_length=20, error_messages={"required": "密码不能为空"}, label="密码", required=True)
    password_again = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请再次输入6-20位的密码"}),
                                     min_length=6, max_length=20, error_messages={"required": "密码不能为空"},
                                     label="密码确认", required=True)

    def clean_password_again(self):
        password = self.cleaned_data["password"]
        password_again = self.cleaned_data["password_again"]
        if password != password_again:
            raise forms.ValidationError("两次输入的密码不一致")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email):
            raise forms.ValidationError("该邮箱已经注册")
        return email


class CommentForm(forms.Form):
    """
    评论表单
    """
    author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
                                                           "required": "required", "size": "25", "tabindex": "1"}),
                             min_length=6, max_length=50, error_messages={"required": "用户名不能为空"})
    email = forms.EmailField(widget=forms.TextInput(attrs={"id": "email", "type": "email", "class": "comment_input",
                                                           "required": "required", "size": "25", "tabindex": "2"}),
                             max_length=50, error_messages={"required": "邮箱不能为空"})
    url = forms.URLField(widget=forms.TextInput(attrs={"id": "url", "type": "url", "class": "comment_input",
                                                       "size": "25", "tabindex": "3"}), max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id": "comment", "class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),
                              error_messages={"required": "评论不能为空"})
    article = forms.CharField(widget=forms.HiddenInput())

    def clean_author(self):
        author = self.cleaned_data["author"]
        if not User.objects.filter(username=author):
            raise forms.ValidationError("用户名不存在，请注册！")
        return author

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email):
            raise forms.ValidationError("该用户名所对应的邮箱不正确，请重新输入！")
        return email
