from django.db import models


# Choices for a book reading progress
ReadTypes = [('Finished', 'Finished'), ('In Progress', 'In Progress'), ('To Be Read', 'To Be Read')]


# Creates the Bookshelf model
class Bookshelf(models.Model):
    shelf_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)

    # Defines the model Manager for Accounts
    Bookshelves = models.Manager()

    def __str__(self):
        return f"{self.user_name}'s {self.shelf_name}"


# Creates the Book model
class Book(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=70)
    read = models.CharField(max_length=20, choices=ReadTypes)
    notes = models.CharField(max_length=300)
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.SET_NULL, null=True, blank=True)

    # Defines the model Manager for Book
    Books = models.Manager()
