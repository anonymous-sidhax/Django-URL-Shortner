from django.urls import path, include
from .views import signup_view, login_view, logout_view


app_name = 'accounts'


urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('signup/', signup_view, name="signup")
]