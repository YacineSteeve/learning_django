from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

"""
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookInstance)
"""

admin.site.register(Genre)
admin.site.register(Language)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    fields = ('id', 'status', 'due_back', 'borrower')


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ('title', 'language', 'isbn')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'language', 'display_genre')

    list_filter = ('author', 'language')

    inlines = [BookInstanceInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    list_filter = ('last_name',)

    fields = ('first_name',
              'last_name',
              ('date_of_birth', 'date_of_death'))

    inlines = [BookInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    list_filter = ('due_back', 'status')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
