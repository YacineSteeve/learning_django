from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
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
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    requested_word = 'u'
    matching_genres = set(genre.name for genre in Genre.objects.filter(name__contains=requested_word))
    matching_books = Book.objects.filter(title__contains=requested_word)

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'requested_word': requested_word,
        'matching_genres': matching_genres,
        'matching_books': matching_books
    }

    return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').filter(borrower=self.request.user).order_by('due_back')
