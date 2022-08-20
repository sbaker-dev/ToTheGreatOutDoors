from django.urls import path
from . import views

urlpatterns = [

    # Core Pages
    path('', views.home, name="home"),
    path('select_location/', views.select_location, name="select_location"),
    path('county/<str:pk>/<str:place_type>', views.county, name='county'),
    path('place/<str:place_name>/<str:place_location>/', views.place, name='place'),
    path('search/', views.search_location, name="search_location"),
    path('contact', views.contact, name='contact'),

    # User authentication / interaction / account settings
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='registerUser'),
    path('logout/', views.logout_user, name="logOut"),
    path('delete-message<str:pk>', views.delete_message, name="deleteMessage"),
    path('account_page/', views.account_page, name='accountPage')

]
