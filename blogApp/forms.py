from unicodedata import category
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from blogApp.models import UserProfile, Category, Post

class UserRegistration(UserCreationForm):
    email = forms.EmailField(max_length=250,help_text="The email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name')
    

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")
       

class UpdateProfileMeta(forms.ModelForm):
    dob = forms.DateField(help_text="The Birthday field is required.")
    contact = forms.CharField(max_length=250,help_text="The Contact field is required.")
    address = forms.CharField(help_text="The Contact field is required.")

    class Meta:
        model = UserProfile
        fields = ('dob', 'contact', 'address')

class UpdateProfileAvatar(forms.ModelForm):
    avatar = forms.ImageField(help_text="The Avatar field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = UserProfile
        fields = ('avatar',)
    
    def __init__(self,*args, **kwargs):
        self.user = kwargs['instance']
        kwargs['instance'] = self.user.profile
        super(UpdateProfileAvatar,self).__init__(*args, **kwargs)

    def clean_current_password(self):
        if not self.user.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError("Password is Incorrect")

class AddAvatar(forms.ModelForm):
    avatar = forms.ImageField(help_text="The Avatar field is required.")
    class Meta:
        model = UserProfile
        fields = ('avatar',)
   

class SaveCategory(forms.ModelForm):
    name = forms.CharField(max_length=250,help_text = "Category Name Field is required.")
    description = forms.Textarea()
    status = forms.ChoiceField(help_text = "Category Name Field is required.", choices = (('1','Active'), ('2','Inctive')))

    class Meta:
        model = Category
        fields = ('name', 'description','status',)
    def clean_name(self):
        name = self.cleaned_data['name']
        id = self.instance.id if not self.instance == None else ''
        try:
            if id.isnumeric() and id != '':
                category = Category.objects.exclude(id= id).get(name= name)
            else:
                category = Category.objects.get(name= name)
        except Exception as e:
            if name == '':
                raise forms.ValidationError(f"Category field is required.")
            else:
                return name
        raise forms.ValidationError(f"{name} Category already exists.")

class SavePost(forms.ModelForm):
    category = forms.IntegerField()
    author = forms.IntegerField()
    title = forms.Textarea()
    blog_post = forms.Textarea()
    status = forms.ChoiceField(help_text = "Status Field is required.", choices = (('1','Published'), ('2','Unpublished')))

    def __init__(self, *args, **kwargs):
        super(SavePost, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('category', 'author','title','blog_post','status','banner')

        
    def clean_category(self):
        catId = self.cleaned_data['category']
        # raise forms.ValidationError(f"Invalid Category Value.")
        try:
            category = Category.objects.get(id = catId)
            return category
        except:
            raise forms.ValidationError(f"Invalid Category Value.")
            
    def clean_author(self):
        userId = self.cleaned_data['author']
        try:
            author = User.objects.get(id = userId)
            return author
        except:
            raise forms.ValidationError(f"Invalid User Value.")

