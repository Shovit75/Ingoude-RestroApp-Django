from . import views
from django.urls import path

urlpatterns=[
    path("", views.index, name="index"),
    path("food/<int:food_id>", views.food, name="food"),
    path("category/<int:category_id>", views.category, name="category"),
    path("webuserlogin", views.webuserlogin, name="webuserlogin"),
    path("webuserregister", views.webuserregister, name="webuserregister"),
    path("webuserlogout", views.webuserlogout, name="webuserlogout"),
    path("cart", views.cart, name="cart"),
    path("addtocart/<int:item_slug>/<str:item_name>/<str:item_price>/", views.addtocart, name="addtocart"),
    path("clearcart", views.clearcart, name="clearcart"),
    path("deleteitem/<int:item_id>", views.deleteitem, name="deleteitem"),
    path("checkout", views.checkout, name="checkout"),
    path("sessions", views.sessions, name="sessions"),
    path("completetransaction", views.completetransaction, name="completetransaction"),
]
