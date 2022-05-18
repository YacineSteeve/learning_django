from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import Book, BookInstance, Author, Genre
from .forms import RenewBookForm
import datetime
from uuid import UUID


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


@login_required()
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request: HttpRequest, pk: UUID) -> HttpResponse:
    """
    View function for renewing a specific BookInstance by librarian.
    :param request: A HttpRequest
    :param pk: A valid book instance uuid
    :return: A HttpResponse (redirection or template to populate).
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


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


class LoanedBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {
        'date_of_birth': datetime.date.today() - datetime.timedelta(weeks=2600),
    }
    permission_required = 'can_mark_returned'


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'can_mark_returned'


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'can_mark_returned'


class BookCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'genres', 'summary', 'language']


class BookUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'genres', 'summary', 'language']


class BookDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = Book
    success_url = reverse_lazy('books')
