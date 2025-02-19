from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group, Permission

class OasisInfo(models.Model):
    # pat_info = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=100)
    mrn = models.CharField(max_length=100)
    # pat_demo = models.CharField(max_length=2000, null=True, blank=True)
    pat_demo = models.TextField(null=True, blank=True)
    cli_rec = models.TextField(null=True, blank=True)
    bims = models.TextField(null=True, blank=True)
    cams = models.TextField(null=True, blank=True)
    phq = models.TextField(null=True, blank=True)
    phy_ass = models.TextField(null=True, blank=True)
    rom = models.TextField(null=True, blank=True)
    spc_tre = models.TextField(null=True, blank=True)
    ser_req = models.TextField(null=True, blank=True)
    cli_sum = models.TextField(null=True, blank=True)
    med_sup = models.TextField(null=True, blank=True)
    goal = models.TextField(null=True, blank=True)

    GG0130A = models.TextField(null=True, blank=True)
    GG0130B = models.TextField(null=True, blank=True)
    GG0130C = models.TextField(null=True, blank=True)
    GG0130E = models.TextField(null=True, blank=True)
    GG0130F = models.TextField(null=True, blank=True)
    GG0130G = models.TextField(null=True, blank=True)
    GG0130H = models.TextField(null=True, blank=True)
    GG0170AB = models.TextField(null=True, blank=True)
    GG0170C = models.TextField(null=True, blank=True)
    GG0170D = models.TextField(null=True, blank=True)
    GG0170E = models.TextField(null=True, blank=True)
    GG170F = models.TextField(null=True, blank=True)
    GG170I = models.TextField(null=True, blank=True)
    GG170J = models.TextField(null=True, blank=True)
    GG170K = models.TextField(null=True, blank=True)
    GG170L = models.TextField(null=True, blank=True)
    GG170M = models.TextField(null=True, blank=True)
    GG170N = models.TextField(null=True, blank=True)
    GG170O = models.TextField(null=True, blank=True)
    GG170P = models.TextField(null=True, blank=True)
    GG170Q = models.TextField(null=True, blank=True)
    GG170R = models.TextField(null=True, blank=True)
    assisted_device = models.TextField(null=True, blank=True)

    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    cli_name = models.CharField(max_length=100, null=True, blank=True)
    visit_date = models.CharField(max_length=100, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.completed = self.check_completed()
        super().save(*args, **kwargs)

    def check_completed(self):
        for field in self._meta.get_fields():
            if isinstance(field, models.Field) and field.name not in ['id', 'created_date', 'modified_date', 'completed']:
                value = getattr(self, field.name)
                if value in [None, '', []]:  
                    return False
        return True

    def __str__(self):
        return self.name
    

# class Image(models.Model):
#     oasis_info = models.ForeignKey(OasisInfo, related_name='images', on_delete=models.CASCADE, null = True, blank = True)
#     img = models.ImageField(upload_to='images/')
#     img_des = models.TextField(null=True, blank=True)

#     created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
#     def __str__(self):
#         return self.oasis_info.name

def image_upload_path(instance, filename):
    today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = filename.split('.')[-1]
    new_filename = f"image_{today_str}.{ext}"
    return f"images/{new_filename}"

class Image(models.Model):
    oasis_info = models.ForeignKey(OasisInfo, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to=image_upload_path)
    img_des = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.oasis_info.name
    
class Mandatory_Documents(models.Model):
    oasis_info = models.ForeignKey(OasisInfo, related_name='mandatory_documents', on_delete=models.CASCADE, null = True, blank = True)
    concent_img = models.ImageField(upload_to='documents/', null=True, blank=True)
    emg_img = models.ImageField(upload_to='documents/', null=True, blank=True)
    med_list_img = models.ImageField(upload_to='documents/', null=True, blank=True)
    add_doc_img1 = models.ImageField(upload_to='documents/', null=True, blank=True)
    add_doc_img2 = models.ImageField(upload_to='documents/', null=True, blank=True)
    misc_img = models.ImageField(upload_to='documents/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.oasis_info.name


