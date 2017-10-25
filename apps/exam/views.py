from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def blank(request):
    response = "connected"
    return HttpResponse(response)

def index(request):
    return render(request, 'exam/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/main')
        else:
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hashed_password)
            messages.error(request, "Successfully Registered")
            return redirect('/main')

def login(request):
    if request.method == 'POST':
        if not 'login_status' in request.session:
            request.session['login_status'] = False
        login_data = User.objects.filter(email=request.POST['email'])
        if len(request.POST['email']) < 1:
            messages.error(request, "enter email")
            return redirect('/main')
        if len(request.POST['password']) < 1:
            messages.error(request, "enter password")
            return redirect('/main')
        inputted_password = request.POST['password']
        stored_password = User.objects.filter(email=request.POST['email']).first().password
        if login_data and bcrypt.checkpw(inputted_password.encode(), stored_password.encode()):
            request.session['login_status'] = {'id':login_data.first().id, 'name':login_data.first().name, 'email':login_data.first().email}
            print request.session['login_status']
            return redirect('/quotes')
        else:
            messages.error(request, "Email and password does not match")
            return redirect('/main')

def logout(request):
    request.session['login_status'] = False
    return redirect('/main')


def create(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        temp = Quote.objects.create(author=request.POST['author'], intext=request.POST['intext'], posted_by=this_user)
        temp.favored_by.add(this_user)
    return redirect('/quotes')

def add_to_favorite(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        this_quote = Quote.objects.get(id=request.POST['quote_id'])
        this_quote.favored_by.add(this_user)
    return redirect('/quotes')

def remove_from_favorite(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        this_quote = Quote.objects.get(id=request.POST['quote_id'])
        this_quote.favored_by.remove(this_user)
    return redirect('/quotes')

def users(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quotes_all = Quote.objects.all()
    context = {
        'quote': quote,
        'quotes_all': quotes_all

    }
    return render(request, 'exam/users.html', context)

def quotes(request):
    quotes_all = Quote.objects.all()
    context = {
        'quotes_all': quotes_all
    }
    return render(request, 'exam/quotes.html', context)