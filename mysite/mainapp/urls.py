from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from mainapp import views


urlpatterns = [


   path('feed/', views.FeedPage.as_view(), name='feedpage'),
   path('articles/<int:article_id>', views.ArticlePage.as_view(), name='articlepage'),
   path('articles/<int:article_id>/delete', views.ArticlePage.delete, name='articledelete'),
   path('articles/<int:article_id>/edit', views.ArticleEdit.as_view(), name='articleedit'),


   path('<str:username>/mainpage/', views.UserPage.as_view(), name='userpage'),

   path('login/', views.Login.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path("register/", views.Login.register, name="register"),

   path('mainpage/admin/', views.AdminPage.as_view(), name='adminpage'),
   path('adminuserdelete/<str:username>', views.AdminPage.delete, name='adminuserdelete'),
   path('adminuserunblock/<str:username>', views.AdminPage.unblock, name='adminuserunblock'),
   path('adminuserblock/<str:username>', views.AdminPage.block, name='adminuserblock'),
]
