from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


def post_list(request):
    post_list = Post.published.all()
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post/list.html', {'posts': posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'post/detail.html', {'post': post})


def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # subject = f"{cd['name']} recommends you read " f"{post.title}"
            subject = 'Test subject'
            message = 'Test message'
            sender = 'ridmovies@yandex.ru'
            recipient = [cd['to']]
            send_mail(
                subject,
                message,
                sender,
                recipient,
                fail_silently=False,
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'post/share.html', {'post': post, 'form': form, 'sent': sent})


# def post_share(request, post_id):
#     # Retrieve post by id
#     post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
#     sent = False
#
#     if request.method == 'POST':
#         # Form was submitted
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             # Form fields passed validation
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = f"{cd['name']} recommends you read " \
#                       f"{post.title}"
#             message = f"Read {post.title} at {post_url}\n\n" \
#                       f"{cd['name']}\'s comments: {cd['comments']}"
#             send_mail(subject, message, 'ridmovies@yandex.ru',
#                       [cd['to']])
#             sent = True
#
#     else:
#         form = EmailPostForm()
#     return render(request, 'post/share.html', {'post': post, 'form': form, 'sent': sent})