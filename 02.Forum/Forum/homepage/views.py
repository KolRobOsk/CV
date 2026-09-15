from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Post


def homepage(request):
    """Show all posts to everyone; only logged-in users get the create form."""
    form = None

    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                # Redirect after a successful POST so refreshing the page
                # doesn't resubmit the form.
                return redirect("homepage")
        else:
            form = PostForm()
    elif request.method == "POST":
        # The create form is only rendered for logged-in users, so a POST
        # from someone logged out shouldn't normally happen -- reject it.
        return HttpResponseForbidden("You must be logged in to post.")

    posts = Post.objects.all()
    return render(request, "homepage/homepage.html", {"posts": posts, "form": form})
