from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views


class UserLoginView(auth_views.LoginView):
  template_name = 'pages/sign-in.html'
  form_class = LoginForm
  success_url = '/'

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/authz/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = {'form': form}
  return render(request, 'pages/sign-up.html', context)


class UserPasswordResetView(auth_views.PasswordResetView):
  template_name = 'accounts/password-reset.html'#'accounts/forgot-password.html'
  form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/recover-password.html'
  form_class = UserSetPasswordForm


class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm


def user_logout_view(request):
  logout(request)
  return redirect('login')
