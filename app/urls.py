from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login") ,
    path("logout/", views.logout_view, name="logout"),
    path("post/", views.post_recipe, name="post"), 
    path("main/", views.get_all_recipes, name="main"),  
    path('recipe/<int:recipe_id>/', views.recipe_profile, name='recipe'),
    path('update-recipe/<int:recipieid>/', views.updaterecipiepost, name='updaterecipiepost'),
    path('delete/<int:recipieid>/', views.deleterecipe, name='delete'),
    path('search/', views.search_recipes, name='search'),
]
