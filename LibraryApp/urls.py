from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('login/', views.user_login, name='login'),
    path('login1/', views.login1, name='login1'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_categorydb/', views.add_categorydb, name='add_categorydb'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_registerdb/', views.user_registerdb, name='user_registerdb'),
    path('apd/', views.apd, name='apd'),
    path('user_approve/<int:k>/', views.approve, name='approve'),
    path('user_disapprove/<int:k>/', views.disapprove, name='disapprove'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('add_books', views.add_books, name='add_books'),
    path('add_booksdb', views.add_booksdb, name='add_booksdb'),
    path('book_details', views.book_details, name='book_details'),
    path('edit_book/<int:pk>',views.edit_book,name="edit_book"),
    path('delete_book/<int:pk>',views.delete_book,name="delete_book"),
    path('user_details/', views.user_details, name='user_details'),
    path('delete_user/<int:k>/', views.delete_user, name='delete_user'),
    path('search/', views.search, name='search'),
    path('rent/<int:book_id>/', views.rent_book, name='rent_book'),
    path('cart/<int:book_id>', views.add_to_cart, name='cart'),
    path('return/<int:book_id>/', views.return_book, name='return_book'),
    path('pay_fine/<int:book_id>/', views.pay_fine, name='pay_fine'),
    path('rentalhistory/', views.user_rental_history, name='user_rental_history'), 
    path('admin_rentalhistory/', views.admin_rentalhistory, name='admin_rentalhistory'),
    path('booklist/<int:category_id>/', views.booklist, name='booklist'),  # Updated from 'prolist'
    path('book_list/', views.book_list, name='book_list'),  # Updated from 'pro_list'
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),  # Updated from 'cart'
    path('view_cart/', views.view_cart, name='view_cart'),  # Updated from 'cartde'
    path('increase_quantity/<int:book_id>/', views.increase_quantity, name='increase_quantity'),  # Updated from 'increase'
    path('decrease_quantity/<int:book_id>/', views.decrease_quantity, name='decrease_quantity'),  # Updated from 'decrease'
    path('remove_item/<int:book_id>/', views.remove_item, name='remove_item'),  # Updated from 'remove'
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_db/', views.checkout_db, name='checkout_db'),
    path('user_purchasehistory/', views.user_purchase_history, name='user_purchase_history'), 
    path('admin_purchase_history/', views.admin_purchase_history, name='admin_purchase_history'),
    path('report-issue/<int:book_id>/', views.report_issue, name='report_issue'),
    path('admin_damage_report/', views.admin_damage_report, name='admin_damage_report'),
    path('re_pas/', views.re_pas, name='re_pas'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_profile/', views.view_profile, name='view_profile'),
]
