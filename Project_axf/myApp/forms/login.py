from django import forms


# 创建登录页表单
class LoginForm(forms.Form):
    username = forms.CharField(max_length=11, min_length=6, required=True, label=u"账号",
                               error_messages={
                                   "required": u"用户账号不能为空",
                                   "invalid": u"格式错误",
                                   "min_length": u"账号不能少于6位",
                                   "max_length": u"账号不能大于12位",
                               },
                               widget=forms.TextInput(attrs={"class": "c"}))
    password = forms.CharField(max_length=16, min_length=6, label=u"密码", widget=forms.PasswordInput)
