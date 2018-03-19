from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import View
#from .forms import UserForm

'''class UserFormView(View):
    form_class = UserForm
    template_name = 'home/registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #clean (normalised) data - means formatted properly
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns user object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # print their username - request.user.username (thenewboston ep 36 2.33)
                    return redirect('home:index')

        return render(request, self.template_name, {'form': form})
        #return render(request, 'home/home.html')'''





def index(request):
    return render(request, 'home/home.html')

    #return HttpResponse(arg)
    '''response = HttpResponse(alarm, content_type='text/plain')
    response_a = do_something(response)
    return response_a'''

'''def post(request):
    form = HomeForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['post']
        args = {'form': form, 'text': text}
        return render(request, 'home/home.html', args)'''

def post(request):
    print(request.POST)
    print('hi')
    #return render(request, 'results/home.html')

def search(request, text):
    print(request.POST)
    return render(request, 'results/home.html')
