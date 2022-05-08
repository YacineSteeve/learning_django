from django.db import models
from django.urls import reverse
import uuid


class Genre(models.Model):
    """
    A model representing a book Genre.
    """

    name = models.CharField(max_length=200, help_text="A book genre (e.g. Science-Fiction).")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


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
        return self.name


class Book(models.Model):
    """
    A model representing a book.
    """

    title = models.CharField(max_length=200, help_text="The book title.")

    genres = models.ManyToManyField(Genre, help_text="The book genre.")

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    isbn = models.CharField('ISBN',
                            max_length=13,
                            help_text='13 Character '
                                      '<a href="https://www.isbn-international.org/content/what-isbn">'
                                      'ISBN number</a>')

    summary = models.TextField(max_length=1000, help_text="A brief summary of the book.")

    languages = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title.capitalize()

    def get_absolute_url(self):
        return reverse('book-details', args=[str(self.id)])


class BookInstance(models.Model):
    """
    A model representing an instance of a given book, to handle copies and loans.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier for the book copy.")

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200, help_text="The legal notice of the book.")

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (('m', 'Maintenance'),
                   ('o', 'On loan'),
                   ('r', 'Reserved'),
                   ('a', 'Available'))

    loan = models.CharField(max_length=1,
                            choices=LOAN_STATUS,
                            blank=True,
                            default='m',
                            help_text="The book availability status.")

    class Meta:
        ordering = ['-due_back']

    def __str__(self):
        return f'{self.id} : {self.book.title} ({self.loan})'


class Author(models.Model):
    """
    A model representing a book author.
    """

    first_name = models.CharField(max_length=100, help_text="The author first name")

    last_name = models.CharField(max_length=100, help_text="The author last name")

    date_of_birth = models.DateField('Born on', null=True, blank=True)

    date_of_death = models.DateField('Died on', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'date_of_death']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('author-details', args=[str(self.id)])
