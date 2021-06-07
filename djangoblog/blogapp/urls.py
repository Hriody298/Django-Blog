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
    path('register', views.getRegister, name="register"),
    path('auth', views.getAuth, name="auth"),
    path('author_update<int:uid>', views.AuthorUpdate, name="author_update"),
    path('author_delte<int:uid>', views.AuthorDelete, name="author_delete"),
    path('add_author', views.AddAuthor, name="add_author"),
    path('category', views.getCategory, name="category"),
    path('create_category', views.CreateCategory, name="create_category"),
    path('delete_category<int:qid>', views.DeleteCategory, name="delete_category"),
    path('update_category<int:qid>', views.UpdateCategory, name="update_category")
]
