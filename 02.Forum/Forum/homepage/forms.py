from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # author is set from request.user in the view, not typed by hand.
        fields = ["name", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # post and author are set in the view, not typed by hand.
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write a comment..."}
            ),
        }
