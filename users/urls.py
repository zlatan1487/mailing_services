from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, Profileview, block_user, unblock_user, generate_new_password
from users.views import UserListView
app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', Profileview.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
]
