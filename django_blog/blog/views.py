from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from .models import Post, Comment, Tag
from django.db.models import Q
from .models import Post, Tag




class UserLoginView(LoginView):
    template_name = "blog/login.html"

class UserLogoutView(LogoutView):
    template_name = "blog/logout.html"

class RegisterView(View):
    template_name = "blog/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect("profile")
        return render(request, self.template_name, {"form": form})

@login_required
def profile_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "blog/profile.html", {"u_form": u_form, "p_form": p_form})


# Public: list all posts
class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"       # context: object_list or post_list
    context_object_name = "posts"
    queryset = Post.objects.select_related("author").order_by("-published_date")

# Public: view a single post
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return (Post.objects
                .select_related("author")
                .prefetch_related("tags", "comments__author"))

# Authenticated: create a post (author = current user)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("posts-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self._apply_tags(form)
        return response

    def _apply_tags(self, form):
        tags_list = form.cleaned_data.get("tags_input", [])
        tag_objs = []
        for name in tags_list:
            obj, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(obj)
        # set many-to-many after the post is saved
        self.object.tags.set(tag_objs)

# Only author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("posts-list")

    def test_func(self):
        return self.get_object().author_id == self.request.user.id

    def form_valid(self, form):
        response = super().form_valid(form)
        self._apply_tags(form)
        return response

    def _apply_tags(self, form):
        tags_list = form.cleaned_data.get("tags_input", [])
        tag_objs = []
        for name in tags_list:
            obj, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(obj)
        self.object.tags.set(tag_objs)
# Only author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("posts-list")

    def test_func(self):
        return self.get_object().author_id == self.request.user.id


class PostByTagListView(ListView):
    """
    List posts that contain a given tag (by slug).
    """
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return (Post.objects.filter(tags=self.tag).select_related("author")
                .prefetch_related("tags")
                .order_by("-published_date"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag"] = self.tag
        return ctx


class SearchView(ListView):
    """
    Search posts by title, content, or tag name using ?q=...
    """
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        base = Post.objects.select_related("author").prefetch_related("tags").order_by("-published_date")
        if not q:
            return base.none()
        return base.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "").strip()
        return ctx



class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a comment for a given post.
    The form is shown on post_detail; this view just handles POST submission.
    """
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"  # rarely used; we submit from post_detail

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post_obj
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("posts-detail", kwargs={"pk": self.post_obj.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing comment (only by the comment's author).
    """
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        return self.get_object().author_id == self.request.user.id

    def get_success_url(self):
        return reverse("posts-detail", kwargs={"pk": self.get_object().post_id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an existing comment (only by the comment's author).
    """
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        return self.get_object().author_id == self.request.user.id

    def get_success_url(self):
        return reverse("posts-detail", kwargs={"pk": self.get_object().post_id})
