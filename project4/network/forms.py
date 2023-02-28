from django import forms


class PostForm(forms.Form):
    tweet = forms.CharField(label="New Post", max_length=280,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'autofocus': True}))
