from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Post


def homepage(request):
    """Show all posts and handle creating a new one, all on '/'."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect after a successful POST so refreshing the page
            # doesn't resubmit the form.
            return redirect("homepage")
    else:
        form = PostForm()

    posts = Post.objects.all()
    return render(request, "homepage/homepage.html", {"posts": posts, "form": form})
