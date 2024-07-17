from django.db import models
from django.contrib.auth.models import User

class ObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status_code=1)

class Base(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="%(app_label)s_%(class)s_creator_name",null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="%(app_label)s_%(class)s_editor_name",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status_code = models.BooleanField(default=1)
    objects = ObjectManager()

    class Meta:
        abstract = True

# Create your models here.
class ReportMedia(Base):
    files = models.FileField(upload_to= 'reports')
    type = models.CharField(max_length=200)
    placement = models.CharField(max_length=200)


    def __str__(self):
        return self.type


class ReportContent(Base):
    content = models.CharField(max_length=1000)
    type = models.CharField(max_length=200)
    placement = models.CharField(max_length=200)

class ContentStyling(Base):
    font_name = models.CharField(max_length = 100,blank=True,null=True)
    font_size = models.IntegerField(default=10)
    font_style = models.CharField(max_length = 100,blank=True,null=True)
    def __str__(self):
        return self.font_name

class ReportTemplate(Base):
    media = models.ManyToManyField(ReportMedia,blank=True)
    content_style = models.ForeignKey(ContentStyling,on_delete=models.CASCADE,null=True,blank=True)
    content = models.ManyToManyField(ReportContent,blank=True)
    template_name = models.CharField(max_length = 100,blank=True,null=True)
    def __str__(self):
        return self.template_name


class ReportFilters(Base):
    display_name = models.CharField(max_length=100)
    db_name = models.CharField(max_length=100)
    query_string = models.CharField(max_length=500,null=True,blank=True)
    replacable_variable = models.CharField(max_length=100, null=True,blank=True)
    is_id = models.IntegerField(default=0)

    def __str__(self):
        return self.display_name


class ReportManagement(Base):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500, null=True, blank=True)
    query = models.TextField(max_length=10000)
    report_type = models.CharField(default="Query", max_length=25)
    user = models.ManyToManyField(User, blank=True, related_name="reports_user")
    columns_to_skip = models.IntegerField(default=0)
    filters_list = models.ManyToManyField(ReportFilters, blank=True)


    def __str__(self):
        return self.name
    
