import requests
import urllib3
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, BookshelfForm
from .models import Book, Bookshelf


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# This function will render the Home page when requested
def home(request):
    form = BookForm(data=request.POST or None)   # Retrieve AddBook form
    # Checks if request method is POST
    if request.method == 'POST':
        pk = request.POST['bookshelf']      # If the form is submitted, retrieve which bookshelf the user wants to view
        return balance(request, pk)       # Call bookshelf function to render that bookshelf's list of books
    content = {'form': form}    # Pass content to the template in a dictionary
    # Adds content of form to page
    return render(request, 'home.html', content)


# This function will render the Create Bookshelf page when requested
def create_shelf(request):
    form = BookshelfForm(data=request.POST or None)     # Retrieve the Bookshelf form
    # Checks if request method is POST
    if request.method == 'POST':
        if form.is_valid():     # Check to see if the submitted form is valid and if so, saves the form
            form.save()     # Saves new bookshelf
            return redirect('home')     # Returns user back to the homepage
    content = {'form': form}        # Saves content to the template as a dictionary
    # Adds content of form to page
    return render(request, 'bookshelf.html', content)


#This function will render the Add Book page when requested
def add_book(request):
    form = BookForm(data=request.POST or None)      # Retrieve the Book form
    # Checks if request method is POST
    if request.method == 'POST':
        if form.is_valid():     # Check to see if the submitted form is valid and if so, saves the form
            pk = request.POST['bookshelf']      # Retrieve which bookshelf the book addition was for
            book = form.save(commit=False)
            book.bookshelf_id = pk
            book.save()     # Saves the added book form
            return balance(request, pk)     # Renders current bookshelf with list of books
    # Pass content to the template in a dictionary
    content = {'form': form}
    # Adds content of form to page
    return render(request, 'add_book.html', content)


def balance(request, pk):
    bookshelf = get_object_or_404(Bookshelf, pk=pk)     # Retrieve the requested bookshelf using its primary key
    books = Book.Books.filter(bookshelf_id=pk)     # Retrieve all of that bookshelf's books
    # Pass bookshelf, books in bookshelf to template
    content = {'bookshelf': bookshelf, 'books': books}
    return render(request, 'balance.html', content)


def delete_shelf(request, pk):
    bookshelf = get_object_or_404(Bookshelf, pk=pk)
    if request.method == 'POST':
        bookshelf.delete()
        return redirect('home')


def rename_shelf(request, pk):
    bookshelf = get_object_or_404(Bookshelf, pk=pk)
    form = BookshelfForm(data=request.POST or None, instance=bookshelf)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('balance', pk=pk)

    context = {'form': form, 'bookshelf': bookshelf}
    return render(request, 'rename_shelf.html', context)


def remove_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    shelf_id = book.bookshelf_id

    if request.method == 'POST':
        book.delete()

    return redirect('balance', pk=shelf_id)


def toggle_read_status(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        selected_status = request.POST.get('read_status')

        valid_statuses = ['Finished', 'In Progress', 'To Be Read']

        if selected_status in valid_statuses:
            book.read = selected_status
            book.save()

    return redirect('balance', pk=book.bookshelf_id)


def search(request):
    query = request.GET.get("q", "").strip()        #Get search term from URL parameters
    books_list = []

    if query:
        api_url = "https://gutendex.com/books/"
        params = {"topic": query}

        try:
            response = requests.get(api_url, params=params, timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()

            raw_books = data.get("results", [])

            for book in raw_books[:10]:
                author_names = []
                for author in book.get("authors", []):
                    if isinstance(author, dict) and author.get("name"):
                        author_names.append(author.get("name"))

                # Combine authors or fallback to default string
                authors_str = ", ".join(author_names) if author_names else "Unknown Author"

                books_list.append({
                    "title": book.get("title", "Unknown Title"),
                    "authors": authors_str,
                    "downloads": book.get("download_count", 0),
                    "id": book.get("id"),
                })
        except requests.exceptions.RequestException as e:
            print(f"API Connection Error: {e}")
            books_list = None

    context = {
        "query": query,
        "books": books_list,
    }
    return render(request, 'search.html', context)


def book_detail(request, book_id):
    api_url = f"https://gutendex.com/books/{book_id}/"
    book_data = None
    clean_formats = {}  # Dictionary to hold safe keys for the template
    book_summaries = []

    try:
        response = requests.get(api_url, timeout=10, verify=False)
        response.raise_for_status()
        book_data = response.json()

        # Extract formats safely using standard string dictionary lookups
        formats = book_data.get("formats", {})
        clean_formats = {
            "html": formats.get("text/html"),
            "epub": formats.get("application/epub+zip"),
            "text": formats.get("text/plain; charset=utf-8")
            or formats.get("text/plain"),
        }

        book_summaries = book_data.get("summaries", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching book details: {e}")

    context = {
        "book": book_data,
        "formats": clean_formats,  # Pass the safe dictionary keys to the template
        "summaries": book_summaries,
    }
    return render(request, "book_detail.html", context)
