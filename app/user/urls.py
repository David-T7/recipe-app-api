from user import views

from django.urls import path

app_name = 'user'
urlpatterns =[
path('create/' , view=views.CreateUserView.as_view() , name='create') ,
path('token/' , view=views.CreateTokenView.as_view() , name='token'),
path('me/' , view=views.ManageUserView.as_view() , name='me'),

]