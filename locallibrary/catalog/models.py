from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from datetime import date


class Genre(models.Model):
    """
    A model representing a book Genre.
    """

    name = models.CharField(max_length=200, help_text="A book genre (e.g. Science-Fiction).")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.capitalize()


class Language(models.Model):
    """
    A model representing a language in which a book is published.
    """

    LANGUAGES = (('AR', 'Arabic'),
                 ('ZH', 'Chinese (Mandarin)'),
                 ('EN', 'English'),
                 ('FR', 'French'),
                 ('DE', 'German'),
                 ('EL', 'Greek'),
                 ('IT', 'Italian'),
                 ('JA', 'Japanese'),
                 ('KO', 'Korean'),
                 ('LA', 'Latin'),
                 ('PT', 'Portuguese'),
                 ('RU', 'Russian'),
                 ('ES', 'Spanish'),
                 ('SW', 'Swahili'))

    name = models.CharField(max_length=2,
                            choices=LANGUAGES,
                            default='EN',
                            blank=True,
                            help_text="The language of the book.")

    class Meta:
        ordering = ['name']

    def __str__(self):
        for language in self.LANGUAGES:
            if language[0] == self.name:
                return language[1]


class Book(models.Model):
    """
    A model representing a book.
    """

    title = models.CharField(max_length=200, help_text="The book title.")

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    isbn = models.CharField('ISBN',
                            max_length=13,
                            help_text='13 Character '
                                      '<a href="https://www.isbn-international.org/content/what-isbn">'
                                      'ISBN number</a>')

    genres = models.ManyToManyField(Genre, blank=True)

    summary = models.TextField(max_length=1000, help_text="A brief summary of the book.")

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def display_genre(self) -> str:
        return ', '.join([genre.name for genre in self.genres.all()[:3]])

    display_genre.short_description = 'Genre'

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title.capitalize()

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    A model representing an instance of a given book, to handle copies and loans.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier for the book copy.")

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200, help_text="The legal notice of the book.")

    LOAN_STATUS = (('m', 'Maintenance'),
                   ('o', 'On loan'),
                   ('r', 'Reserved'),
                   ('a', 'Available'))

    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='m',
                              help_text="The book availability status.")

    due_back = models.DateField(null=True, blank=True, help_text="If on loan, the date by which it should be returned.")

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (
            ("can_mark_returned", "Set book as returned"),
        )

    def __str__(self):
        return f'{self.id} : {self.book.title} ({self.status})'

    def is_overdue(self):
        return date.today() > self.due_back if self.due_back else False


class Author(models.Model):
    """
    A model representing a book author.
    """

    first_name = models.CharField(max_length=100, help_text="The author first name")

    last_name = models.CharField(max_length=100, help_text="The author last name")

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'date_of_birth', 'date_of_death']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
