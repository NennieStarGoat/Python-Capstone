from django.urls import path
from . import views


urlpatterns = [
    # Sets the url path to home page home.html
    path('', views.home, name='home'),
    # Sets the url path to search page search.html
    path('search/', views.search, name='search'),
    # Sets the url path to create a bookshelf page create.html
    path('bookshelf/', views.create_shelf, name='create'),
    # Sets the url path to view current bookshelf page balance.html
    path('<int:pk>/balance/', views.balance, name='balance'),
    # Sets the url path to add a new book page add_book.html
    path('add_book/', views.add_book, name='book'),
    # Sets the url path to delete a bookshelf page delete.html
    path('bookshelf/<int:pk>/delete', views.delete_shelf, name='delete_shelf'),
    # Sets the url path to go to the details page of a specific book detail.html
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    # Sets the url path to renaming a bookshelf page rename_shelf.html
    path("shelf/<int:pk>/rename/", views.rename_shelf, name="rename_shelf"),
    # Sets the url path to removing a book from a shelf page remove_book.html
    path("book/<int:book_id>/remove/", views.remove_book, name="remove_book"),
    # Sets the url path to change the status of a book on a bookshelf page toggle_read.html
    path("book/<int:book_id>/toggle-read/", views.toggle_read_status, name="toggle_read_status",),
]