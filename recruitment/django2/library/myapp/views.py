from django.shortcuts import render
from django.http import HttpResponse
from .models import AddBook
from .forms import Add_Book_Form
import csv
import pickle
from datetime import datetime
import pandas as pd

file_types = ['txt', 'pdf']


def add_book_request(request):
    book_add_form = Add_Book_Form()
    if request.method == 'POST':
        book_add_form = Add_Book_Form(request.POST, request.FILES)
        if book_add_form.is_valid():
            book_pr = book_add_form.save(commit=False)
            book_pr.file_data = request.FILES['file_data']
            file_type = book_pr.file_data.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in file_types:
                return HttpResponse("Invalid file type")
            with open('books.csv', 'a') as file:
                db = csv.DictWriter(file, fieldnames=['title', 'author', 'publisher', 'genre', 'summary', 'ISBN', 'location', 'count'])
                db.writerow({'title': book_pr.name, "author": book_pr.author, 'publisher': book_pr.publisher, 'genre': book_pr.genre, 'summary': book_pr.summary, 'ISBN': book_pr.ISBN, 'location': book_pr.location})
            try:
                book_pr.save()
            except:
                pass
            return render(request, 'book_added.html', {"book_pr": book_pr})
    return render(request, 'add_book.html', {"book_add_form": book_add_form})




# import books

# file = open("database_l.pkl", "wb")
# data = {"shreyansh": "jain"}
# pickle.dump(data, file)
# file.close()

db = open("database.pkl", "rb")
data = pickle.load(db)
db.close()

dbl = open("database_l.pkl", 'rb')
datal = pickle.load(dbl)
dbl.close()

params = {"passed": ""}
params1 = {"passed": ""}
params2 = {"name": "", "status": ""}
student_params = {"name": "", "status": ""}
librarian_params = {"name": ""}
# book_params = {"name": "", "title": "", "author": "", "publisher": "", "genre": "", "summary": "", "ISBN": "", "location": "", "count": ""}

def student_login(request):
    return render(request, "student_login.html", params)


def index(request):
    return render(request, 'index.html')


def about(request):
    return HttpResponse("about Shreyansh")


def register(request):
    return render(request, 'registeration.html', params)


def registered(request):
    uname = request.GET.get('uname')
    upass = request.GET.get('upass')
    urpass = request.GET.get('urpass')
    if(upass == urpass):
        if(uname in data):
            params["passed"] = "That username is already taken"
            return render(request, "registeration.html", params)
        else:
            params["passed"] = ""
            data[uname] = upass
            db = open("database.pkl", "wb")
            pickle.dump(data, db)
            db.close()
            with open(f"student_logs/{uname}.csv", "w") as file:
                output = csv.DictWriter(file, fieldnames=["Title", "Date", "AcceptedOn", "ReturnedOn", "Status"])
                output.writeheader()
            return HttpResponse(f"Welcome {uname}")
    else:
        params["passed"] = "Passwords didn't match"
        return render(request, "registeration.html", params)


def librarian(request):
    return render(request, "Librarian_login.html", params1)


def librarian_registered(request):
    uname = request.GET.get('uname')
    upass = request.GET.get('upass')
    if(uname in datal):
        if(datal[uname] == upass):
            params1["passed"] = ""
            librarian_params["name"] = uname
            with open("library_request.csv", "r") as file:
                data = csv.DictReader(file)
                requested_books = []
                for line in data:
                    # print(line)
                    requested_books.append(line)
            librarian_params["request"] = requested_books
            # print(librarian_params)
            return render(request, "librarian_logged.html", librarian_params)
        else:
            params1["passed"] = "Incorrect Password"
            return render(request, "Librarian_login.html", params1)
    else:
        params1["passed"] = "No such librarian exist"
        return render(request, "Librarian_login.html", params1)


def student(request):
    uname = request.GET.get("uname")
    upass = request.GET.get("upass")
    if(uname in data):
        if(data[uname] == upass):
            student_params["status"] = ""
            student_params["name"] = uname
            pending = []
            issued = []
            with open(f"student_logs/{uname}.csv", "r") as file:
                output = csv.DictReader(file)
                for line in output:
                    if line["Status"] == "Pending":
                        pending.append(line)
                    else:
                        issued.append(line)
            student_params["pending"] = pending
            student_params["issued"] = issued
            return render(request, "student.html", student_params)
        else:
            params["passed"] = "Either Username or password is incorrect"
            return render(request, 'student_login.html', params)
    else:
        params["passed"] = "Either Username or password is incorrect"
        return render(request, 'student_login.html', params)


def book(request):
    book_name = request.GET.get("book_name")
    book_name = book_name.lower()
    # print(book_name)
    with open("books.csv", 'r') as books_file:
        books_db = csv.DictReader(books_file)
        books_with_same_name = []
        books_with_same_name_params = {"name": ""}
        i = 0
        for line in books_db:
            if book_name in line["title"].lower():
                i += 1
                books_with_same_name.append(line['title'])
                # books_with_same_name += f"{i}. " + f"<h2 id=book{i}>{line['title']}</h2>" + "<br><br>"
        if i > 0:
            books_with_same_name_params["name"] = books_with_same_name
            return render(request, "book_select.html", books_with_same_name_params)
        else:
            student_params["status"] = "No such book found"
            return render(request, "student.html", student_params)


def book_selected(request):
    book_name = request.GET.get("book_select")
    books_file = open("books.csv", 'r')
    books_db = csv.DictReader(books_file)
    for line in books_db:
        if(line["title"] == book_name):
            book_details = line
            books_file.close()
            book_details["name"] = student_params["name"]
            return render(request, "book_page.html", book_details)


def requested(request):
    data = request.GET.get("data")
    data = data.split("+")
    book_name = data[1]
    student_name = data[0]
    datenow = datetime.now()
    request_csv = {"Name": student_name, "Title": book_name, "Date": datenow}
    # print(request_csv)
    with open("library_request.csv", "r") as file:
        output = csv.DictReader(file)
        for lines in output:
            if lines["Name"] == student_name and lines["Title"] == book_name:
                return HttpResponse("You have already requested this book and it is still to be approved")
    with open("library_request.csv", "a") as file:
        output = csv.DictWriter(file, fieldnames=["Name", "Title", "Date"])
        output.writerow(request_csv)
    with open(f"student_logs/{student_name}.csv", "a") as file:
        output = csv.DictWriter(file, fieldnames=["Title", "Date", "AcceptedOn", "ReturnedOn", "Status"])
        output.writerow({"Title": book_name, "Date": datenow, "AcceptedOn": "", "ReturnedOn": "", "Status": "Pending"})
    return HttpResponse("Your file is requested")


def request_accepted(request):
    accepted = request.GET.getlist('check')
    print("Hello")
    # print(accepted)
    read = open("library_request.csv", "r")
    read_file = csv.DictReader(read)
    print(read_file)
    print(line for line in read_file)
    to_write = []
    for line in read_file:
        for approved in accepted:
            approved = approved.split("+")
            if not (approved[0] == line["Name"] and approved[1] == line["Title"]):
                to_write.append(line)
                print(line)
            else:
                with open("logs.csv", "a") as file:
                    file_db = csv.DictWriter(file, fieldnames=["Librarian", "Student", "Book", "Status"])
                    file_db.writerow({"Librarian": librarian_params["name"], "Student": line["Name"], "Book": line["Title"], "Status": f"Issued on {line['Date']}"})
                output = pd.read_csv(f"student_logs/{line['Name']}.csv")
                for i in range(len(output.axes[0])):
                    if output.loc[i, "Title"] == line["Title"]:
                        output.loc[i, "AcceptedOn"] = datetime.now()
                        output.loc[i, "Status"] = "Issued"
                        output.to_csv(f"student_logs/{line['Name']}.csv", index=False)
                print("Its a break")
                break
    read.close()
    write = open("library_request.csv", "w")
    write_file = csv.DictWriter(write, fieldnames=["Name", "Title", "Date"])
    write_file.writeheader()
    for line in to_write:
        write_file.writerow(line)
    write.close()
    with open("library_request.csv", "r") as file:
        data = csv.DictReader(file)
        requested_books = []
        for line in data:
            print(line)
            requested_books.append(line)
    librarian_params["request"] = requested_books
    return render(request, "librarian_logged.html", librarian_params)


def book_show(request):
    title = request.GET.get("title")
    book_details = pd.read_csv("books.csv")
    for i in range(len(book_details.axes[0])):
        if book_details.loc[i, "title"] == title:
            book_params = {"title": book_details.loc[i, "title"], "author": book_details.loc[i, "author"], "publisher": book_details.loc[i, "publisher"], "genre": book_details.loc[i, "genre"], "summary": book_details.loc[i, "summary"], "ISBN": book_details.loc[i, "ISBN"], "location": book_details.loc[i, "location"]}
    print(title)
    with open(f"media/{title}.txt", "r") as file:
        book_params["content"] = file.readlines()
    return render(request, "book_show.html", book_params)


# def librarian_add_book(request):
#     return render(request, "librarian_add_request_html", librarian_params)


def book_added(request):
    title = request.GET.get("title")
    author = request.GET.get('author')
    publisher = request.GET.get('publisher')
    ISBN = request.GET.get("ISBN")
    genre = request.GET.get('genre')
    # content = request.