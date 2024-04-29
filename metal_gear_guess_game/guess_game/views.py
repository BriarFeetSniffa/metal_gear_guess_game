from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .db.db_main import db_info
from random import randint
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .models import Characters
import redis


class Bio:
    def __init__(self):
        self.all_data = db_info()
        self.res_dic = {
            'all_chars': Characters.objects.all(),
            'name': '...',
            'sex': '...',
            'quote': '...',
            'nicknames': '...',
            'orgs': '...',
            "occupation": '...',
            'nationality': '...',
            'games': '...',
        }

    def make_bio(self, point):
        chars = self.all_data
        for i in chars:
            if point in i:
                self.res_dic['name'] = i[1]
                self.res_dic['sex'] = i[2]
                if i[3] != '':
                    self.res_dic['quote'] = i[3]
                if i[4] != '':
                    self.res_dic['nicknames'] = i[4]
                if i[5] != '':
                    self.res_dic['orgs'] = i[5]
                if i[6] != '':
                    self.res_dic['occupation'] = i[6]
                if i[7] != '':
                    self.res_dic['nationality'] = i[7]
                if i[8] != '':
                    self.res_dic['games'] = i[8]

        return self.res_dic


def start_of_guess(request):
    bio = Bio()

    char_list = [i[1] for i in db_info()]

    inp = request.POST.get('Guess')
    redis_client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    if not redis_client.get('guess'):
        rand_pk = randint(1, 26)
        redis_client.set(name='guess', value=bio.make_bio(rand_pk)['name'])
        redis_client.expire('guess', 300)

    if inp == str(redis_client.get('guess')):
        return render(request, 'win_in_guess.html', context=bio.make_bio(inp))

    if inp in char_list and inp != str(redis_client.get('guess')):
        return render(request, 'lose_in_guess.html', context=bio.make_bio(inp))

    print(str(redis_client.get('guess')))
    return render(request, 'start_of_guess.html', context=bio.make_bio(str(redis_client.get('guess'))))


def lose_in_guess(request):
    return render(request, 'guess_game/lose_in_guess.html')


def win_in_guess(request):
    return render(request, 'guess_game/win_in_guess.html')


def register_page(request):
    form = CreateUserForm
    context = {'form': form}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('guess_game:login')

    return render(request, 'guess_game/register.html', context=context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'guess_game/login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('guess_game:login')
