from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "account"
urlpatterns = [
    path('signup/', views.SignupAPIView.as_view()),
    path("login/", views.CustomTokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path('<int:pk>/', views.MyPageAPIView.as_view()),
    path("steamlogin/", views.SteamLoginAPIView.as_view()),
    path("steam-callback/", views.SteamCallbackAPIView.as_view()),
    path("logout/", views.LogoutAPIView.as_view()),
    path('verify-email/<str:uidb64>/<str:token>/', views.EmailVerifyAPIView.as_view(), name='verify-email'),
    # Steam ID 회원가입
    path("steamsignup/", views.SteamSignupAPIView.as_view()),
    # Steam ID 로그인
    path("steamidlogin/", views.SteamIDLoginAPIView.as_view()),
    # Steam ID 연동
    path("steamlink/", views.SteamLinkAPIView.as_view()),
    # Steam 라이브러리 불러오기
    path("steamlibrary/", views.GetSteamLibraryAPIView.as_view()),
    # ID 찾기
    path("find-id/", views.FindIDAPIView.as_view()),
    # 비밀번호 찾기
    path("find-password/", views.FindPasswordAPIView.as_view()),
    # 인증번호 인증
    path("verify-token/", views.VerifyTokenAPIView.as_view()),
    # 비밀번호 재설정
    path("change-password/", views.ChangePasswordAPIView.as_view()),
]