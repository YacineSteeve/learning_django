from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Book, BookInstance, Author, Genre


def index(request: HttpRequest) -> HttpResponse:
    """
    A view function for displaying the number of instances of some objects
    :param request: A HttpRequest.
    :return: A HttpResponse, to publish the context built with the request, on the base of a given template.
    """

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    requested_word = 'u'
    matching_genres = set(genre.name for genre in Genre.objects.filter(name__contains=requested_word))
    matching_books = ({'title': book.title,
                       'author': book.author}
                      for book in Book.objects.filter(title__contains=requested_word)
                      )

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'requested_word': requested_word,
        'matching_genres': matching_genres,
        'matching_books': matching_books
    }

    return render(request, 'index.html', context)
