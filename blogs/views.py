from django.shortcuts import render
from .models import Banner, Post, Comment, BlogCategory, Tags, FriendlyLink
from django.db.models import Q
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    banner_list = Banner.objects.all()
    repost_list = Post.objects.filter(is_recomment=True)

    for Repost in repost_list:
        Repost.content = Repost.content[:150] + '......'

    post_list = Post.objects.order_by('-pub_date')

    for post in post_list:
        post.content = post.content[:150] + '......'

    # 博客分类
    blogcategory_list = BlogCategory.objects.all()

    comment_list = Comment.objects.order_by('-pub_date').all()

    FriendlyLink_list = FriendlyLink.objects.all()

    new_comment_list = []
    for test in comment_list:
        if test.post.id not in new_comment_list:
            new_comment_list.append(test.post)

    try:
        page = request.GET.get('page', 1)
    except:
        page = 1

    p = Paginator(post_list, per_page=2, request=request)
    post_list = p.page(page)

    ctx = {
        'banner_list': banner_list,
        'repost_list': repost_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'comment_list': comment_list,
        'FriendlyLink_list': FriendlyLink_list,
        'new_comment_list': new_comment_list,
    }
    return render(request, 'index.html', ctx)


def base(request):
    return render(request, 'base.html')


def list(request):
    post_list = Post.objects.order_by('-pub_date').all()

    tgs_list = Tags.objects.all()

    comment_list = Comment.objects.order_by('-pub_date').all()

    new_comment_list = []
    for test in comment_list:
        if test.post.id not in new_comment_list:
            new_comment_list.append(test.post)

    content = {
        'post_list': post_list,
        'tgs_list': tgs_list,
        'new_comment_list': new_comment_list,
        'comment_list': comment_list,
    }
    return render(request, 'list.html', content)


class Search(View):
    def get(self, request):
        pass

    def post(self, request):
        kw = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=kw) | Q(content__icontains=kw))

        ctx = {
            'post_list': post_list
        }
        return render(request, 'list.html', ctx)


def blog_list(request, tid=-1):
    # tid=-1时候 代表的是  从列表过来
    tid = int(tid)
    post_list = None
    if tid != -1:
        post_list = Post.objects.filter(tags=tid)
    else:
        post_list = Post.objects.order_by('-pub_date')

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(post_list, per_page=10, request=request)
    post_list = p.page(page)

    # 取出所有标签
    tags = Tags.objects.all()
    tag_message_list = []

    for t in tags:
        count = len(t.post_set.all())
        tag_message_list.append({'name': t.name, 'id': t.id, 'count': count})

    ctx = {
        'post_list': post_list,
        'tag_message_list': tag_message_list
    }

    return render(request, 'list.html', ctx)


def show(request):
    return render(request, 'show.html')
