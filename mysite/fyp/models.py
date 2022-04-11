from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.template.defaultfilters import slugify

class VideoOutput(models.Model):
    video=models.ForeignKey('Video', on_delete=models.CASCADE)
    total_detected_card=models.IntegerField(default=0)
    detected_time=models.CharField(max_length=100,default='')
    detected_image=models.ImageField(upload_to='upload_test_images/',default='',null=True,blank=True)


class Video(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True, unique=True)
    videofile= models.FileField(upload_to='upload_test_videos/', null=True, unique=True)
    result=models.BooleanField(default=False)

    def _get_unique_slug(self):
        slug = slugify(self.videofile.name)
        unique_slug = slug
        num = 1
        while Video.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    def create_user(self, email,username,phonenumber,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not phonenumber:
            raise ValueError('Users must have an phonenumber')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phonenumber=phonenumber, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email,username,phonenumber,password):
        user = self.create_user(
            email,
            username=username, 
            password=password,
            phonenumber=phonenumber,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True  
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name='email',max_length=60,unique=True)
    username=models.CharField(max_length=30,unique=True)
    phonenumber=models.CharField(max_length=30,unique=True)
    date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    hide_email=models.BooleanField(default=True)

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','phonenumber']

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
         
