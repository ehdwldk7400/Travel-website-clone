from django.urls import path
from .views      import SignUp, SignIn, ProfileView

urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/signin', SignIn.as_view()),
    path('/profile', ProfileView.as_view()),
]