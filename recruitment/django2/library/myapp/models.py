from django.db import models


class AddBook(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=75)
    genre = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=20)
    summary = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    count = models.IntegerField()
    file_data = models.FileField()

    def __str__(self):
        return self.name


# class RegisterStudent(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     password = models.CharField(max_length=75)
#     re_password = models.CharField(max_length=75)
#
#
# class LoginStudent(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=75)
#
#
# class LoginLibrarian(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=75)
#
#

