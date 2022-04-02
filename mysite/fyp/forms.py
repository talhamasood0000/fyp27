from django import forms
from django.contrib.auth import get_user_model
from .models import Video, VideoOutput
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User=get_user_model()


class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ['videofile']

class VideoOutputForm(forms.ModelForm):
    class Meta:
        model= VideoOutput
        fields= ['total_detected_card','detected_time']

class UserAdminCreationForm(forms.ModelForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Password Conformation', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('email','username','phonenumber')
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 is not None and password1 != password2:
            raise forms.ValidationError("Passwords dont match")
        return password2

    def save(self,commit=True): 
        user=super(UserAdminCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user    

class UserAdminChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=User
        fields=('email','username','phonenumber','password','is_active','is_admin')

        def clean_password(self):
            return self.initial['password']

class RegisterForm(forms.ModelForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Password Conformation', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('email','username','phonenumber')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class':'form-control','name':'email','placeholder':'Email','type':'email'})
        self.fields['username'].widget.attrs.update({'class':'form-control','name':'name','placeholder':'Name','type':'text'})
        self.fields['phonenumber'].widget.attrs.update({'class':'form-control','name':'phonenumber','placeholder':'Phone Number'})
        self.fields['password1'].widget.attrs.update({'class':'form-control','name':'password','placeholder':'Password','type':'password'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','name':'password','placeholder':'Password Conformation','type':'password'})

    
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 is not None and password1 != password2:
            raise forms.ValidationError("Passwords dont match")
        return password2

    def save(self,commit=True): 
        user=super(RegisterForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user  

class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.TextInput(
        attrs={'type':'email','class':'form-control','name':'email','placeholder':'Email'}))
    password=forms.CharField(widget=forms.TextInput(
        attrs={'type':'password','class':'form-control','name':'password','placeholder':'Password'}))
