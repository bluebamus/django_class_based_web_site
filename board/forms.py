# from django.forms import TextInput, ModelForm, Textarea
from django import forms
from .models import Board


class BoardForm(forms.Form):
    title = forms.CharField(
        error_messages={"required": "Please enter the title."}, max_length=128, label="title"
    )
    contents = forms.CharField(
        error_messages={"required": "Please enter your content."},
        widget=forms.Textarea,
        label="content",
    )
    tags = forms.CharField(required=False, label="tag")
    photo = forms.ImageField(required=False, label="photo")


class BoardUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                
        super(BoardUpdateForm, self).__init__(*args, **kwargs)        
        #self.fields['tags'].initial = [value[1]  for value in self.instance.tags.all().values_list()]
        self.fields['tags'] = forms.CharField()                
        self.fields['tags'].required = False 
        #self.fields['photo'].required = False        

    # def is_valid(self):        
    #     valid = super(BoardUpdateForm, self).is_valid()
    #     if not valid:            
    #         return valid
    #     else:            
    #         return valid
        
    class Meta:
        model = Board
        fields = ["title", "contents", "tags","photo"]
        # fields = "__all__"
        labels = {
            "title": ("title"),
            "contents": ("contents"),
            "tags": ("tag"),
            "photo": ("photo"),
        }
        widgets = {
            "contents": forms.Textarea(attrs={"cols": 80, "rows": 20}),            
        }
        help_texts = {}
        error_messages = {
            "title": {
                "required": ("Please enter the title."),
            },
            "contents": {
                "required": ("Please enter your content."),
            },
        }
    
