#===========================
#blog/forms.py
#===========================
#--------------------------------------------------
#IMPORTS
from django import forms
from .models import Post, Comment

#####################################################
#Classes
#####################################################
#--------------------------------------------------
#Class: PostForm
#creates a form for each Post class in models.py
class PostForm(forms.ModelForm):

    #method: Meta
    #gives ability to edit author, title, text fields of Post class
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title':forms.TextInput(attrs={'class':TextInput()})
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

#--------------------------------------------------
#Class: CommentForm
#creates a form for each Comment class in models.py
class CommentForm(forms.ModelForm):

    #method: Meta
    #gives ability to edit author and text fields of Comment class
    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
