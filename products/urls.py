from django.urls import path,include
from . import views
urlpatterns = [
    path('create',views.create,name='create'),
    path('<int:product_id>',views.detail,name='detail'),
    path('<int:product_id>/upvote',views.upvote,name='upvote'),
    path('myproducts',views.myproducts,name='myproducts'),
    path('myproducts/myproducts_details/<int:product_id>',views.myproducts_details,name='myproducts_details'),
    path('myproducts/myproducts_details/update/<int:product_id>',views.myproducts_update,name='myproducts_update'),
    path('myproducts/myproducts_details/update/<int:product_id>/updateconfirm',views.update_confirm,name='update_confirm'),
    path('myproducts/myproducts_details/delete/<int:product_id>',views.myproducts_delete,name='myproducts_delete'),
    path('myproducts/myproducts_details/delete/<int:product_id>/delete_confirm',views.delete_confirm,name='delete_confirm'),
]
