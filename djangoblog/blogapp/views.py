from os import name
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from .models import author,category,article,comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import createForm,RegistrationForm,GetAuthor,GetComment,UpdateAuthor,CategoryForm
from django.contrib import messages


# Create your views here.
def index(request):
    post = article.objects.all()
    search = request.GET.get('search')
    if search:
        post = post.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    paginator = Paginator(post, 8)
    page_number = request.GET.get('page')
    total_article = paginator.get_page(page_number)
    context = {
        "post": total_article
    }
    return render(request, "index.html",context)


def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, name=post_author.id)
    post = article.objects.filter(article_author=auth.id)
    context={
        "auth": auth,
        "post": post
    }
    return render(request, "profile.html",context)


def getsingle(request, id):
    user = get_object_or_404(User, id=request.user.id)
    post = get_object_or_404(article, pk=id)
    first = article.objects.first()
    last = article.objects.last()
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    show_comment = comment.objects.filter(post=id)
    form = GetComment(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.name = user
        instance.post = post
        instance.save()
    context = {
        "first": first,
        "last": last,
        "post": post,
        "related": related,
        "form": form,
        "show_comment": show_comment

    }
    return render(request, "single.html",context)


def getTopic(request, name):
    cat = get_object_or_404(category, name=name)
    post = article.objects.filter(category=cat.id)
    context = {
        "post": post,
        "cat": cat
    }
    return render(request, "category.html", context)


def getLogin(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            user = request.POST.get("user")
            password = request.POST.get("password")
            auth = authenticate(request, password=password, username=user)
            if auth is not None:
                login(request, auth)
                return redirect("index")
            else:
                messages.add_message(request, messages.ERROR, 'Username or password error.')
                return redirect("login")

    return render(request, "login.html")


def getLogout(request):
    logout(request)
    return redirect("index")


def createpost(request):
    if request.user.is_authenticated:
        user = get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=user
            instance.save()
            messages.success(request, 'New post created.')
            return redirect('profile')
        return render(request, "create_post.html", {"form": form})
    else:
        return redirect("login")


def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile=author.objects.filter(name=user.id)
        if author_profile:
            author_user=get_object_or_404(author, name=request.user.id)
            post = article.objects.filter(article_author=author_user.id)
            return render(request, "logged_profile.html", {"post": post, "user": author_user})
        else:
            form = GetAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                messages.success(request, 'Author created successfully')
                return redirect("profile")
            return render(request, "create_author.html", {"form": form})
    else:
        return redirect("login")



def getUpdate(request,pid):
    if request.user.is_authenticated:
        user = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=pid)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=user
            instance.save()
            messages.success(request, 'Post details updated.')
            return redirect('profile')
        return render(request, "create_post.html", {"form": form})
    else:
        return redirect("login")


def getDelete(request,pid):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=pid)
        post.delete()
        messages.warning(request, 'Post has been deleted.')
        return redirect('profile')
    else:
        return redirect("login")


def getRegister(request):
    form=RegistrationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration successfully done.')
        return redirect('profile')
    context={
        "form": form
    }
    return render(request, 'register.html', context)


def getAuth(request):
    if request.user.is_staff:
        auth = author.objects.all()
        user = get_object_or_404(author, id=request.user.id)
        context={
            "auth": auth,
            "user": user,
        }
        return render(request, 'get_auth.html', context)


def AuthorUpdate(request,uid):
    auth_user = get_object_or_404(author, id=uid)
    form = UpdateAuthor(request.POST or None, request.FILES or None, instance=auth_user)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Author successfully updated')
        return redirect('auth')
    return render(request, 'author_update.html', {"form": form})


def AuthorDelete(request,uid):
    if request.user.is_staff:
        auth_user = get_object_or_404(author, id=uid)
        auth_user.delete()
        messages.success(request, 'Author successfully deleted.')
        return redirect('auth')


def AddAuthor(request):
    form = UpdateAuthor(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Author created successfully')
        return redirect('auth')
    return render(request, 'create_author.html',{"form": form})


def getCategory(request):
    categories = category.objects.all()
    return render(request, 'get_category.html', {"cat": categories})


def CreateCategory(request):
    if request.user.is_staff:
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'New category added.')
            return redirect('category')
        return render(request, 'create_category.html',{"form": form})
    else:
        messages.warning(request, 'login as an staff.')
        return redirect('login')
 


def DeleteCategory(request,qid):
    delete_cat = get_object_or_404(category, id=qid)
    delete_cat.delete()
    messages.success(request, 'Category successfully deleted.')
    return redirect('category')


def UpdateCategory(request,qid):
    cat = get_object_or_404(category, id=qid)
    form = CategoryForm(request.FILES or None, instance=cat)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Category successfully updated')
        return redirect('category')
    return render(request,'update_category.html',{"form": form})
