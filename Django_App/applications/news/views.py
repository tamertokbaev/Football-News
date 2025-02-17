from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template.context_processors import csrf
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from random import randint

from .models import *
from .forms import CustomRegistrationForm


# Данная функция используется для показа содержимого главной страницы
def index(request):
    news_list = News.objects.order_by('-count_of_views')[:3]
    another_list = News.objects.order_by('-count_of_views')[3:9]
    latest_news = News.objects.order_by('-publication_date')[:4]
    latest_comments = Comment.objects.order_by('-comment_date')[:4]
    return render(request, 'news/index.html', {'news_list': news_list, 'latest_news': latest_news,
                                               'another_list': another_list, 'latest_comments': latest_comments})


# Данная функция используется для показа определенной новости по ссылке в urls.py news/<int:news_id>
def one_by_one(request, news_id):
    try:
        context = {}
        a = News.objects.get(id=news_id)
        count = a.comment_set.count()
        a.count_of_views += 1
        a.save()
        if auth.get_user(request).is_authenticated:
            if UserFavourite.objects.filter(fav_news=a, user=auth.get_user(request)).exists():
                context.update({'favourite': _("Удалить из избранного")})
            else:
                context.update({'favourite': _("Добавить в избранное")})
    except:
        raise Http404("Статья не найдена!")
    latest_news = News.objects.order_by('-publication_date')[:4]
    comment_list = a.comment_set.all()
    latest_comments = Comment.objects.order_by('-comment_date')[:4]
    context.update({'news': a, 'comment_list': comment_list, 'count': count, 'latest_news': latest_news,
                    'latest_comments': latest_comments})
    return render(request, 'news/single-post.html', context)


# Данная функция используется для оставления комментария в новосте по ссылке news/<int:news_id>
def leave_comment(request, news_id):
    try:
        a = News.objects.get(id=news_id)
    except:
        raise Http404(_("Статья не найдена!"))
    a.comment_set.create(comment_author=auth.get_user(request), comment_text=request.POST['comment_text'])
    return HttpResponseRedirect(reverse('news:one_by_one', args=(news_id,)))


# Данная функция используется для регистрации нового пользователя при помощи кастомной форм CustomRegistrationForm в
# forms.py
def register_user(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            secret_code = randint(1000, 9999)
            head_of_message = 'Подтверждение регистрации на Football-News-Portal'
            content_of_message = """
                Здравствуйте, ваш электронный адрес был выбран для регистрации на Football News Portal 
                Ваш секретный код: {} 

                Если вы не регистрировались на Football-News-Portal, то пожалуйста просто проигнорируйте это письмо!
                С уважением, Тамерлан Токбаев!
                """.format(secret_code)
            send_mail(head_of_message, content_of_message, "Tamerlan's website",
                      recipient_list=[form.cleaned_data['email']]
                      , fail_silently=False)
            request.session.update({'form': {'username': form.cleaned_data['username'],
                                             'secret_code': secret_code}})
            # form.save()
            return HttpResponseRedirect('/accounts/confirming_registration')
        else:
            return render_to_response('register.html', {'form': form})
    args = {}
    args.update(csrf(request))
    args['form'] = CustomRegistrationForm()
    return render_to_response('register.html', args)


# Данная функция используется для показа всех новостей по дате публикации на новой странице
def archive(request):
    try:
        news_list = News.objects.order_by('publication_date')
        latest_comments = Comment.objects.order_by('-comment_date')[:4]
        latest_news = News.objects.order_by('-publication_date')[:4]
    except:
        raise Http404('Список новостей пуст')
    return render(request, 'news/catagories-post.html', {'news_list': news_list, 'latest_comments': latest_comments, 'latest_news': latest_news})


# Данная функция используется для поиска на главной странице по содержимому и заголовку новости
# Возможны результаты больше чем 1, отображается на отдельной странице search.html
def search(request):
    all_news = []
    try:
        if request.method == 'POST':
            search_str = request.POST['search']
            all_news = News.objects.filter(news_title__icontains=search_str).filter(
                news_content__icontains=search_str)
            latest_comments = Comment.objects.order_by('-comment_date')[:4]
            latest_news = News.objects.order_by('-publication_date')[:4]
            return render(request, 'news/search.html', {'all_news': all_news, 'latest_comments': latest_comments, 'latest_news': latest_news})
    except:
        return render(request, 'news/search.html', {})


# Подтверждение регистрации через электронную почту
def confirming_register(request):
    session = request.session
    if request.method == 'POST':
        if session['form']['secret_code'] == int(request.POST['code_by_user']):
            username = session['form']['username']
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/accounts/login')
        else:
            return render(request, 'news/confirm.html',
                          {'result': _('Секретный код был введен неверно! Регистрация отменена!')})
    return render(request, 'news/confirm.html', {})


def show_profile(request, slug):
    latest_news = News.objects.order_by('-publication_date')[:4]
    latest_comments = Comment.objects.order_by('-comment_date')[:4]
    return render(request, 'news/profile.html', {'latest_news': latest_news,
                    'latest_comments': latest_comments})


def edit_profile(request):
    try:
        if request.method == 'POST':
            first_name = str(request.POST['first_name'])
            last_name = str(request.POST['last_name'])
            birthday_date = request.POST['birth_date']
            user = auth.get_user(request)
            user.first_name = first_name.strip()
            user.last_name = last_name.strip()
            user.profile.birth_date = birthday_date
            user.save()
            latest_news = News.objects.order_by('-publication_date')[:4]
            latest_comments = Comment.objects.order_by('-comment_date')[:4]
            return render(request, 'news/profile.html', {'user': user,
                                                         'result': _('Ваш профиль был успешно изменен'),
                                                         'latest_news': latest_news,
                                                         'latest_comments': latest_comments})
    except:
        raise Http404(_('Упс... Что-то пошло не так...'))
    return render(request, 'news/profile.html', {})


def add_to_favourites(request, news_id):
    try:
        if auth.get_user(request).is_authenticated:
            if UserFavourite.objects.filter(fav_news=News.objects.get(id=news_id), user=auth.get_user(request)).exists():
                UserFavourite.objects.filter(fav_news=News.objects.get(id=news_id), user=auth.get_user(request)).delete()
            else:
                UserFavourite.objects.create(user=auth.get_user(request), fav_news=News.objects.get(id=news_id))
    except:
        raise Http404(_('Возможно ваша статья была удалена или навсегда перемещена!'))
    return HttpResponseRedirect(reverse('news:one_by_one', args=(news_id,)))


def show_favourites(request, slug):
    latest_news = News.objects.order_by('-publication_date')[:4]
    latest_comments = Comment.objects.order_by('-comment_date')[:4]
    context = {'latest_news': latest_news, 'latest_comments': latest_comments}
    try:
        user = auth.get_user(request)
        fav_list = UserFavourite.objects.filter(user=user)
        news_list = []
        for fav_news in fav_list:
            news_list.append(News.objects.get(id=fav_news.fav_news.id))
        if len(news_list) == 0:
            context.update({'error': _('Вы пока ничего не добавили в избранное!')})
        else:
            context.update({'news_list': news_list})
    except:
        context.update({'error': _('Войдите в систему чтобы получить доступ к избранным новостям!')})
    return render(request, 'news/show_favs.html', context)


def profile_avatar(request):
    try:
        if request.method == 'POST':
            user = request.user
            user.profile.avatar = request.FILES['avatar']
            user.save()
    except:
        raise Http404(_("Возникла ошибка! Возможно этот пользователь был удален!"))
    return HttpResponseRedirect(reverse('news:profile', args=(request.user.username,)))


def section_news(request, section):
    try:
        news_list = []
        if section == 'kazakh-premier-league':
            news_list = News.objects.order_by('publication_date').filter(news_tag='Казахстанская-премьер лига')
        elif section == 'uefa-champions-league':
            news_list = News.objects.order_by('publication_date').filter(news_tag='Лига чемпионов УЕФА')
        elif section == 'uefa-europe-league':
            news_list = News.objects.order_by('publication_date').filter(news_tag='Лига Европы УЕФА')
        elif section == 'national-team':
            news_list = News.objects.order_by('publication_date').filter(news_tag='Национальная сборная по футболу')
        elif section == 'another-tag':
            news_list = News.objects.order_by('publication_date').filter(news_tag='Другое')
        latest_comments = Comment.objects.order_by('-comment_date')[:4]
        latest_news = News.objects.order_by('-publication_date')[:4]
        return render(request, 'news/section_news.html', {'news_list': news_list, 'latest_comments': latest_comments, 'latest_news': latest_news})
    except:
        raise Http404(_('Список новостей пуст'))


def like(request, news_id):
    try:
        if request.user.is_authenticated:
            user = auth.get_user(request)
            news = News.objects.get(pk=news_id)
            if UserLiked.objects.filter(user=user, liked_post=news).exists():
                UserLiked.objects.filter(user=user, liked_post=news).delete()
                news.likes -= 1
                news.save()
                return HttpResponseRedirect(reverse('news:one_by_one', args=(news_id,)))
            else:
                UserLiked.objects.create(user=user, liked_post=News.objects.get(pk=news_id))
                news.likes += 1
                news.save()
                return HttpResponseRedirect(reverse('news:one_by_one', args=(news_id,)))
        else:
            return render(request, 'registration/login.html',
                          {'help_msg': _("Войдите на сайт чтобы получить возможность ставить лайк на пост")})
    except:
        raise Http404(_("Произошла ошибка в ходе выполнения действия!"))
