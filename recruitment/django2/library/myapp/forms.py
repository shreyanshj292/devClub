from django import forms
from .models import AddBook
from django import forms

class Add_Book_Form(forms.ModelForm):
	class Meta:
		model = AddBook
		fields = [
			'name',
			'author',
			'publisher',
			'genre',
			'ISBN',
			'summary',
			'location',
			'count',
			'file_data'
		]


# class Register_Student_Form(forms.ModelForm):
# 	class Meta:
# 		model = RegisterStudent
# 		fields = [
# 			'name',
# 			'email',
# 			'password',
# 			're_password'
# 		]
#
#
# class Login_Student(forms.ModelForm):
# 	class Meta:
# 		model = LoginStudent
# 		fields = [
# 			'username',
# 			'password'
# 		]
#
#
# class Login_Librarian(forms.ModelForm):
# 	class Meta:
# 		model = LoginLibrarian
# 		fields = [
# 			'username',
# 			'password'
# 		]