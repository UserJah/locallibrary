from django.shortcuts import render
from .models import *
from django.views import generic


def index(request):
    """
    Функция отображения для домашней страницы сайта
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count
    # Доступные книги со статусом 'a'
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию
    num_books_contains_word = BookInstance.objects.filter(book__title__icontains="test").count()

    # Отрисовка HTML шаблона с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors, 'num_books_contains_word': num_books_contains_word}
    )


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # ваше собственное имя переменной контекста в шаблоне
    # queryset = Book.objects.filter(title__icontains='test')[:5]  # Получение 5 книг, содержащих слово 'test' в заголовке
    template_name = 'books/my_arbitrary_template_name_list.html'  # Определение имени вашего шаблона и его расположения
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book

