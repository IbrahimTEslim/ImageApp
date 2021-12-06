from . import views
from django.urls import path

urlpatterns = [
    path('image',views.add_image,name='image'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('get/<int:image_id>',views.show,name='show'),
    path('test',views.test,name='test'),
    path('getall',views.get_all,name='get_all'),
    path('delete/<int:image_id>',views.delete,name='delete'),
    path('delete',views.delete_all,name='delete_all'),
]