from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

def home(request):
    products = Product.objects.all().order_by("-pub_date")

    query = request.GET.get("q")
    if query:
        products= products.filter(Q(title__icontains=query)|
                            Q(body__icontains=query)|
                            Q(hunter__username__icontains=query)).distinct()
    paginator = Paginator(products, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    list = paginator.get_page(page)

    return render(request,'products/home.html',{'product':list})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()       #making object of model Product
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))



        else:
            return render(request,'products/create.html',{'error':'All fields are required'})
    else:
        return render(request,'products/create.html')

@login_required(login_url="/accounts/signup")
def detail(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    return render(request,'products/detail.html',{'product':product})

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method =='POST':
        product = get_object_or_404(Product,pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))

@login_required(login_url="/accounts/signup")
def myproducts(request):
    User = request.user

    myproducts = Product.objects.filter(hunter=User).order_by("-pub_date")


    query = request.GET.get("q")
    if query:
        myproducts= myproducts.filter(Q(title__icontains=query)|
                            Q(body__icontains=query)|
                            Q(hunter__username__icontains=query)).distinct()
    paginator = Paginator(myproducts, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    list = paginator.get_page(page)


    return render(request,'products/myproducts.html',{'myproducts':list})

@login_required(login_url="/accounts/signup")
def myproducts_details(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    return render(request,'products/myproducts_detail.html',{'product':product})

@login_required(login_url="/accounts/signup")
def myproducts_update(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    print(product.image)
    return render(request,'products/myproducts_update.html',{'product':product})

@login_required(login_url="/accounts/signup")
def update_confirm(request,product_id):
    if request.method=='POST':
            product = get_object_or_404(Product,pk=product_id)
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            try:
                product.icon = request.FILES['icon']
            except:
                pass
            try:
                product.image = request.FILES['image']
            except:
                pass

            product.save()
            product = get_object_or_404(Product,pk=product_id)
    return render(request,'products/myproducts_detail.html',{'product':product})

@login_required(login_url="/accounts/signup")
def myproducts_delete(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    return render(request,'products/delete_product.html',{'product':product})

@login_required(login_url="/accounts/signup")
def delete_confirm(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    product.delete()
    products = Product.objects.all()
    return render(request,'products/home.html',{'product':products,'error':'Deleted the Product Successfully'})
