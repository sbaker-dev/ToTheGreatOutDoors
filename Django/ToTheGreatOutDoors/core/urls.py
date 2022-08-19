from django.urls import path
from . import views

urlpatterns = [

    # Core Pages
    path('', views.home, name="home"),
    path('select_location/', views.select_location, name="select_location"),
    path('county/<str:pk>/<str:place_type>', views.county, name='county'),

    # User authentication / account settings
    path('login/', views.login_page, name='login'),
    path('register_user/', views.register_user, name='registerUser'),
    path('logout/', views.logout_user, name="logOut"),

]
