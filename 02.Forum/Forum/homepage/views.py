from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Post


def homepage(request):
    """Show all posts to everyone; only logged-in users get the create form.

    Editing a post and commenting on it both happen on that post's own
    detail page (see post_detail/post_edit below) -- this page only links
    out to them.
    """
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


def post_detail(request, pk):
    """A single post: full content, an Edit link for its author, the
    comment thread, and a comment form open to anyone (logged in or not).
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    can_edit = request.user.is_authenticated and request.user == post.author
    comment_form = CommentForm()

    return render(
        request,
        "homepage/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "can_edit": can_edit,
            "comment_form": comment_form,
        },
    )


@login_required
def post_edit(request, pk):
    """Edit a post. Only that post's author may access this, logged in or
    not -- login_required covers the "logged in" half, the explicit check
    below covers "is actually the author"."""
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("Only the author can edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "homepage/post_edit.html", {"form": form, "post": post})


def add_comment(request, pk):
    """Add a comment to a post. Open to everyone: logged-in users are
    recorded as the comment's author (shown by username), logged-out
    visitors' comments are stored with no author (shown as 'Anonymous')."""
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()

    return redirect("post_detail", pk=post.pk)


@login_required
def delete_comment(request, pk, comment_id):
    """Delete a comment. Allowed for the comment's own author, or for the
    post's author (moderating comments on their own post)."""
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(post.comments, pk=comment_id)

    if request.user != comment.author and request.user != post.author:
        return HttpResponseForbidden("You can't delete this comment.")

    if request.method == "POST":
        comment.delete()

    return redirect("post_detail", pk=post.pk)
