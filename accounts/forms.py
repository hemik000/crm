from django import forms
from .models import Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class OrdesForm(forms.ModelForm):
    # customer = forms.ModelChoiceField()

    class Meta:
        model = Order
        fields = [ 'product', 'status']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # print(args)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control'
    #         })

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method  = 'post'
    #     self.helper.add_input(Submit('submit', 'Create'))

    def __init__(self, *args, **kwargs):
        super(OrdesForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Place an Order',
                # 'customer',
                'product',
                'status'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


class UserReg(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserReg, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Sign Up'))
        self.helper.layout = Layout(
            Fieldset(
                'Sign Up',
                'username',
                'email',
                'password1',
                'password2'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

class UserLogin(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Sign Up'))
        self.helper.layout = Layout(
            Fieldset(
                'Login',
                'username',
                'password'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
