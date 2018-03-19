from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from signup.models import Profile, Product

from .forms import SignUpForm
from results.modules import update_id

def check_logged_in(request):
    if request.user.is_authenticated():
        return redirect('myaccount/')
    else:
        return redirect('signup/')

def myaccount(request):
    if request.user.is_authenticated():
        basket = []
        if request.method == 'POST':
            product_index = int(request.GET.get('q'))
            #product_to_add = request.user.profile.temp_result_dict['results'][product_index]
            product_to_add = request.session['temp_results'][product_index]
            product_id = update_id.main(product_to_add[5], product_to_add[0])
            p = Product(website=product_to_add[0], name=product_to_add[1], brand=product_to_add[2], price=product_to_add[3], img=product_to_add[4], link=product_to_add[5], web_id=product_id)
            p.save()
            request.user.profile.productm2m.add(p)
        
        product_objs = request.user.profile.productm2m.all()
        itera = 0
        index_list = []
        for obj in product_objs:
            list_ = obj.getBasket()
            list_.append(itera)
            basket.append(list_)
            #index_list.append(itera)
            itera += 1
           #print('basket: ', basket)
        
        return render(request, 'signup/myaccount.html', {'basket':basket})
    else:
        if request.method == 'POST':
            return render(request, 'signup/please_signin.html')
        else:
            return render(request, 'signup/home.html')

def remove(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            product_index = int(request.GET.get('q'))
            product_objs = request.user.profile.productm2m.all()
            request.user.profile.productm2m.remove(product_objs[product_index])
            return redirect('../myaccount')



    
def logout():
    if request.user.is_authenticated():
            logout(request)
            return redirect('../../home')
    else:
         return render('signup/myaccount.html')
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #bio = form.cleaned_data.get('email')
            login(request, user)
            return redirect('../thanks/')
    else:
        form = SignUpForm()
    return render(request, 'signup/home.html', {'form': form})

def thanks(request):
    return render(request, 'signup/thanks.html')

'''def signin(request):
    return render(request, 'signup/signin.html')'''
