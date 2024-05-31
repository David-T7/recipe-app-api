from user import views

from django.urls import path

app_name = 'user'
urlpatterns =[
path('create/' , view=views.CreateUserView.as_view() , name='create'
)
]