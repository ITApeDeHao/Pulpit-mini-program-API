from django.urls import path
from user import views
urlpatterns = [
    path(r'login/password/',views.UserLogin.as_view()),
    path(r'login/phone/', views.PhoneLogin.as_view()),
    path(r'register/phoneCode/', views.PhoneRegister.as_view()),
    path(r'forget/passwordchange/',views.ForgetPassword.as_view()),
    path(r'change/',views.ChangePassWord.as_view()),
    path(r'changename/',views.ChangeUserName.as_view()),
    path(r'Attention/',views.Attention.as_view()),
    path(r'recommand/',views.Recommend.as_view()),
    path(r'personal/',views.Personal.as_view())
]
