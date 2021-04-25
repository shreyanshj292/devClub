from django.urls import path
from . import views
from library import settings
from django.conf.urls.static import static

urlpatterns = [
   path('add_book_request/', views.add_book_request, name='add_book_request'),
   path('', views.index, name="index"),
   path('about/', views.about, name="about"),
   path('register/', views.register, name='register'),
   path('registered/', views.registered, name='registered'),
   path('librarian/', views.librarian, name='librarian'),
   path('student/', views.student, name='student'),
   path('student_login/', views.student_login, name="student_login"),
   path('book/', views.book, name='book'),
   path('book_selected/', views.book_selected, name="book_selected"),
   path('requested/', views.requested, name="requested"),
   path('librarian_registered/', views.librarian_registered, name="librarian_registered"),
   path('request_accepted/', views.request_accepted, name="request_accepted"),
   path('book_show/', views.book_show, name="book_show"),
   path('librarian_add_book/', views.add_book_request, name='librarian_add_book'),
   path('book_added/', views.book_added, name='book_added')
]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)