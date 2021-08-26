import uuid
from django.db import models
from django.urls import reverse  # Используется для генерации URL-адресов путем изменения шаблонов URL-адресов


class Genre(models.Model):
    """
    Модель, представляющая жанр книги
    """

    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self):
        """
        Строка для предстваления объекта модели
        :return:
        """
        return self.name


class Book(models.Model):
    """
    Модель представления книги (но не конкретный экземпляр этой книги)
    """
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key используется потому что у книги может быть только один автор, а у автора - несколько книг
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Символов <a '
                                                             'href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    # ManyToManyField используется, потому что жанр может содержать много книг. Книги могут охватывать многие жанры.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''
        Возвращает URL-адресс для доступа к конкретному экземпляру книги
        '''
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    Модель, представляющая конкретный экземпляр книги (т. Е. Который можно взять из библиотеки).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор этой конкретной книги во всей библиотеке")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateTimeField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """
    Модель представления автора
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        '''
        Возвращает URL-адресс для доступа к конкретному экземпляру книги
        '''
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)


class Language(models.Model):
    """
    Модель представления языка
    """
    name = models.CharField(max_length=100, help_text='Введите язык на котором написана книга')


    def __str__(self):
        return self.name

