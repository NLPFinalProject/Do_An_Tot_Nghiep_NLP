from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


# Create your models here.
from django import forms
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.normalize_email(username),
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    """def create_superuser(self, username,password,name,EmailOrganization, DateOfBirth,phone ):
        
        Creates and saves a superuser with the given email, date of
        birth and password.
        
        user = self.create_user(
            username=username,
            password=password,
            DateOfBirth=DateOfBirth,
            name=name,
            EmailOrganization=EmailOrganization,
            phone=phone
        )
        user.is_admin = True
        user.save(using=self._db)
        return user"""
    def create_superuser(self, username,password ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password,
           
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    username = models.CharField(max_length=30, blank=False, default='',unique=True)
    password = models.CharField(max_length=150, blank=False, default='')
    name = models.CharField(max_length=30,null=True, blank=True, default='')
    EmailOrganization = models.CharField(max_length=30,null=True,blank=True, default='')
    DateOfBirth = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=False,blank=False)
    is_admin = models.BooleanField(default=False,blank=False)
    phone = models.CharField(max_length=15,null=True,blank=True,  default='')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    objects = UserManager()
#bỏ primary key, xóa bảng trong database trên máy rồi migrations lại sẽ tự sinh id(pk)
class User(models.Model):
    username = models.CharField(max_length=30, blank=False, default='')
    password = models.CharField(max_length=100, blank=False, default='')
    name = models.CharField(max_length=30, blank=False, default='')
    EmailOrganization = models.CharField(max_length=30,blank=True, default='')
    DateOfBirth = models.DateTimeField(blank=True)
    active = models.BooleanField(default=False,blank=False)
    phone = models.CharField(max_length=15,blank=True,  default='')

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        db_table='user'
    
"""class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DataDocument(models.Model):
    DataDocumentName = models.CharField(max_length=200)
    DataDocumentType = models.CharField(max_length=10)
    DataDocumentAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    DataDocumentFile = models.FileField(upload_to='DocumentFile/')
    def __str__(self):
        return self.DataDocumentName
    def AuthorName(self):
        return self.DataDocumentAuthor
    def DocumentType(self):
        return self.DataDocumentType

#model dùng để tạo form post
#lock command lại trước khi makemigrations
# #class này k đưa vào database
# class DataDocumentFile(models.Model):
#     DataDocumentFile = models.FileField(upload_to='DocumentFile/')

# nội dung file được tách thành các câu

class DataDocumentContent(models.Model):
    DataDocumentNo = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
    DataDocumentSentence = models.CharField(max_length=200)
    DataDocumentSentenceLength = models.IntegerField(default=0)
    def __str__(self):
        return self.DataDocumentSentence
    def DocName(self):
        return self.DataDocumentNo
    class Meta:
        indexes = [
            models.Index(fields=['DataDocumentNo','DataDocumentSentence'], name='DataDocumentNo1_idx'),
            models.Index(fields=['DataDocumentSentence'], name='DataDocumentSentence1_idx'),
        ]
        
"""
