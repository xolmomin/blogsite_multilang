from . import views
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout',views.logoutuser,name='logout'),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-avatar',views.update_avatar,name='update-avatar'),
    path('category_mgt',views.category_mgt,name='category-mgt'),
    path('manage_category',views.manage_category,name='manage-category'),
    path(r'manage_category/<int:pk>',views.manage_category,name='edit-category'),
    path('save_category',views.save_category,name='save-category'),
    path('delete_category',views.delete_category,name='delete-category'),
    path('post_mgt',views.post_mgt,name='post-mgt'),
    path('manage_post',views.manage_post,name='manage-post'),
    path(r'manage_post/<int:pk>',views.manage_post,name='edit-post'),
    path('save_post',views.save_post,name='save-post'),
    path('delete_post',views.delete_post,name='delete-post'),
    path(r'view_post/<int:pk>',views.view_post,name='view-post'),
    path(r'<int:pk>',views.post_by_category,name='category-post'),
    path('categories',views.categories,name='category-page'),
]
