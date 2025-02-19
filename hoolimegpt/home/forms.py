from django import forms
from .models import OasisInfo, Image, Mandatory_Documents

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = OasisInfo
        # fields = [
        #     'pat_info', 'name', 'mrn', 'pat_demo', 'cli_rec', 'bims', 'cams', 'phq', 'phy_ass', 'rom', 'spc_tre',
        #     'ser_req', 'cli_sum', 'med_sup', 'goal', 'GG0130A', 'GG0130B', 'GG0130C', 'GG0130E', 'GG0130F', 'GG0130G',
        #     'GG0130H', 'GG0170AB', 'GG0170C', 'GG0170D', 'GG0170E', 'GG170F', 'GG170I', 'GG170J', 'GG170K', 'GG170L',
        #     'GG170M', 'GG170N', 'GG170O', 'GG170P', 'GG170Q', 'GG170R', 'assisted_device', 'time_in', 'time_out', 
        #     'cli_name', 'visit_date']
        fields = [
            'name', 'mrn', 'pat_demo', 'cli_rec', 'bims', 'cams', 'phq', 'phy_ass', 'rom', 'spc_tre',
            'ser_req', 'cli_sum', 'med_sup', 'goal', 'GG0130A', 'GG0130B', 'GG0130C', 'GG0130E', 'GG0130F', 'GG0130G',
            'GG0130H', 'GG0170AB', 'GG0170C', 'GG0170D', 'GG0170E', 'GG170F', 'GG170I', 'GG170J', 'GG170K', 'GG170L',
            'GG170M', 'GG170N', 'GG170O', 'GG170P', 'GG170Q', 'GG170R', 'assisted_device', 'time_in', 'time_out', 
            'cli_name', 'visit_date']
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img', 'img_des']

class Mandatory_DocumnetsForm(forms.ModelForm):
    class Meta:
        model = Mandatory_Documents
        fields = ['concent_img', 'emg_img', 'med_list_img', 'add_doc_img1', 'add_doc_img2', 'misc_img']
