from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm, UsernameField
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import LowProfile
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To

class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject, message, from_email, recipient_list, html_message=None):
        """
        Override the send_mail method to use SendGrid and send the email with the custom template.
        """
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        for email in recipient_list:
            # Prepare dynamic data for the template
            user = self.get_users(email)[0]
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.SITE_URL}/accounts/reset/{uid}/{token}/"  # Customize the reset URL

            dynamic_template_data = {
                "username": user.username,
                "reset_link": reset_link
            }

            # Use SendGrid's dynamic template
            mail = Mail(
                from_email=Email("noreply@app-mucho.com"),
                to_emails=To(email),
                subject=subject,
            )
            mail.template_id = "d-f8e5bcaea66e45e58dba4eb8f0d9a1ee"#settings.SENDGRID_PASSWORD_RESET_TEMPLATE_ID  # Your SendGrid template ID
            mail.dynamic_template_data = dynamic_template_data

            try:
                response = sg.send(mail)
                print(f"Email sent! Status code: {response.status_code}")
            except Exception as e:
                print(f"Error sending email: {e}")        



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                           widget=forms.EmailInput(attrs={
                               'class': 'form-control'
                           }
                           )
                           )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control phone-mask', }),
        label="Telefone"
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label="Primeiro Nome"
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label="Último Nome",
    )
    
    role_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label="Role",
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label=("Senha"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=("Confirmação Senha"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = LowProfile  # User
        fields = ["username", "first_name", "last_name", "role_name", "email", "phone_number", "password1",
                  "password2"]
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_methd = 'post'
        self.helper.add_layout(Submit('submit', 'Register'))
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
            # user.profile.save()
            # Profile.objects.create(user=user, phone_number=self.cleaned_data["phone_number"])
        return user

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class UserPasswordResetForm(PasswordResetForm):
  email = forms.EmailField(widget=forms.EmailInput(attrs={
    'class': 'form-control',
    'placeholder': 'Email'
  }))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
