from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Product, Vote
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html',{'products': products})

@login_required(login_url="/products/signup")
def details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/details.html', {'product': product})

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return(request, 'products/signup.html', {'error':'Username has already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                login(request, user)
                return redirect('home')
        else:
            return (request, 'products/signup.html', {'error': 'Passwords must match!'})

    return render(request, 'products/signup.html')

def create(request):
    if request.method == "POST":
        if request.POST['name'] and request.POST['link'] and request.POST['description']:
            product = Product()
            product.name = request.POST['name']
            product.image = request.FILES['image']
            product.description = request.POST['description']
            product.date = timezone.datetime.now()
            product.votes = 0
            product.creator = request.user
            product.link = request.POST['link']
            product.save()
            return redirect('/products/' + str(product.id))

        else:
            return render(request, 'products/create.html', {'error':'All fields are required!'})


    return render(request, 'products/create.html')


@login_required(login_url="/products/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        try:
            vote = Vote.objects.get(product=product, hunter=request.user)
        except Vote.DoesNotExist:
            vote = Vote()
            vote.product = product
            vote.hunter = request.user
            product.votes += 1
            product.save()
            vote.save()
        return redirect('/products/' + str(product.id))