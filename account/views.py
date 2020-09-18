from django.shortcuts import render
from django.contrib.auth.views import LoginView as  AuthLoginView
from django.contrib.auth.views import PasswordChangeView as  AuthPwdChangeView
from .forms import LoginForm,PwdChangeForm,UserRegistrationForm
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

class LoginView(AuthLoginView):
	authentication_form = LoginForm
	extra_context = {'page':'login'}
	#redirect_field_name = 'redirect_to'

class PasswordChangeView(AuthPwdChangeView):
	form_class = PwdChangeForm

@login_required
def dashboard(request):
	return render(request,'account/dashboard.html',{'page':'dashboard'})

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(data=request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_user = form.save(commit=False)
			new_user.set_password(cd['password'])
			new_user.save()
			return render(request,'account/register_done.html',{'new_user':new_user})
	else:
		form = UserRegistrationForm()
	return render(request,'account/register.html',{'form':form})