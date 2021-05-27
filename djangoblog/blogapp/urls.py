from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('author/<name>', views.getauthor, name="author"),
    path('article/<int:id>', views.getsingle, name="single-post"),
    path('topic/<name>', views.getTopic, name="topic"),
    path('login', views.getLogin, name="login"),
    path('logout', views.getLogout, name="logout"),
    path('create_post', views.createpost, name="create_post"),
    path('profile', views.getProfile,name="profile"),
    path('update/<int:pid>', views.getUpdate, name="update"),
    path('delete/<int:pid>', views.getDelete, name="delete"),
    path('register', views.getRegister, name="register")
]
