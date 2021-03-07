from django.urls import path
#for pass wrod rest
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('process_order/', views.processOrder, name="process_order"),

	#working with items
	path('update_item/<str:pk>', views.updateItem, name="update_item"),
	path('addpost/',views.addPost , name="addpost"),

	#usersLogic
	#usersLogic --> setting and loging in
	path('signin/', views.signin , name="sign_in"),
	path('login/' , views.loginPage, name="login"),
	path('logout/', views.logOutUser , name="logout") ,
	#useresLogic --> resting passwords
	path('rest_password/' ,
						auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html")
						, name="reset_password"),

	path('rest_password_sent/' ,
    					auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html") ,
        				name="password_reset_done"),

	path('rest/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html")
	, name="password_reset_confirm"),

	path('rest_password_complete/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_done.html")
					,name="password_reset_complete"),

	#assking for payment
	path('paytopost/', views.paytopost , name='paytopost'),
	path('paied/',views.pay , name="paied"),
]