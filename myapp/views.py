from .models import barcodes, account, reviews
from django.shortcuts import render, redirect
from .forms import RegistrationForm, AuthForm, ReviewAddForm, ReviewsSearch
from datetime import datetime
import hashlib
import time, calendar
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json

key = "KfsndjkfmFJSANJ"#Создаем свой ключ для хеширования auth_key

def logout(request):
    response = HttpResponse("Cookie обнулен.")
    response.delete_cookie('login')
    response.delete_cookie('auth_key')
    return response

def reviews(request):
    return render(request, 'reviews.html')
    
def authorized(request):
    return render(request, 'authorized.html')

def index(request):
    set_cookie(request)
    return render(request, 'index.html')

def registration(request):
    return render(request, 'registration.html')

def registrationnext(request):
    return render(request, 'registrationNext.html')

def login(request):
    return render(request, 'login.html')

def about(request):
    filter_params = {'barcode': '4607174577206'}
    queryset = barcodes.objects.filter(**filter_params)
    return render(request, 'about.html', {'barcodes': queryset})

def set_cookie(request):
    response = HttpResponse("Cookie set!")
    response.set_cookie('my_cookie', 'cookie_value')
    return response


def review_search(request):
    if request.method == 'POST':
        form = ReviewsSearch(request.POST)
        if form.is_valid():
            count = reviews.objects.filter(product_barcode=form.cleaned_data['barcode']).count()
            if(count > 0):
                result = reviews.objects.filter(product_barcode=form.cleaned_data['barcode'])
                serialized_data = serializers.serialize('json', result)
                return render(request, 'reviews.html', {'data': serialized_data})
            else:
                return HttpResponse('Ошибка: не найдены никакие отзывы о товаре!')
        else:
            return HttpResponse('Ошибка: форма недействительна!')
    else:
        return HttpResponse('Ошибка: нет параметров POST!')

def auth_validation(request):
    if(request.COOKIES['login'].is_valid and request.COOKIES['auth_key'].is_valid):
        result = account.objects.filter(login=request.COOKIES['login'])
        login = request.COOKIES['login']
        auth_key = request.COOKIES['auth_key']
        client_ip = request.META.get('REMOTE_ADDR')#Достаем IP адрес пользователя. Будет защитой от использования auth_key на другом компьютере
        password = result.password
        current_GMT = time.gmtime()
        current_timestamp = calendar.timegm(current_GMT)#получаем текущий таймстамп для записи в ауткей (будет служить сроком годности)
        auth_key = "".join([key, login, password, client_ip])#Генерим строку из всех составляющих
        auth_key = sha1_hash(auth_key) #хешируем аут кей
        arr = request.COOKIES['auth_key'].split("_")
        if(arr[0] == auth_key and current_timestamp < arr[0]):
            return True
        else:
            return False
    else:
        return False
    
def review_add(request):
    if(request.COOKIES['login'].is_valid and request.COOKIES['auth_key'].is_valid):
        if(auth_validation(request) == True):#Если аут кей действителен, и срок его годности не вышел, то выполняем запрос
            form = ReviewAddForm(request.POST)
            if form.is_valid():
                current_GMT = time.gmtime()
                current_timestamp = calendar.timegm(current_GMT)
                res = account.objects.filter(login=form.cleaned_data['email'])
                reviewer_id2 = res.id#получаем id человека из БД
                new_review = reviews(#создаем новый экземпляр класса reviews (из models.py)
                    reviewer_id=reviewer_id2,
                    product_barcode = form.cleaned_data['product_barcode'],
                    title = form.cleaned_data['title'],
                    description = form.cleaned_data['description'],
                    timestamp=current_timestamp,
                )
                new_review.save()#Сохраняем экземпляр в БД
        else:
            return HttpResponse('Ошибка: auth_key недействителен!')
    else:
        return HttpResponse('Ошибка: cookie не валидны!')

def sha1_hash(string):
    # Создаем объект хеша SHA-1
    sha1 = hashlib.sha1()
    # Преобразуем строку в байтовый формат (требуется для хеширования)
    string_bytes = string.encode('utf-8')
    # Обновляем хеш с использованием байтов строки
    sha1.update(string_bytes)
    # Получаем окончательный хеш в виде шестнадцатеричной строки
    hashed_string = sha1.hexdigest()

    return hashed_string

def login_process(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            count = account.objects.filter(login=form.cleaned_data['email'],password=form.cleaned_data['password']).count()
            if(count > 0):#Если логин и пароль совпадают, впускаем человека в систему
                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)#получаем текущий таймстамп для записи в ауткей (будет служить сроком годности)
                client_ip = request.META.get('REMOTE_ADDR')#Достаем IP адрес пользователя. Будет защитой от использования auth_key на другом компьютере
                auth_key = "".join([key, form.cleaned_data['email'], form.cleaned_data['password'], client_ip])#Генерим строку из всех составляющих
                auth_key = sha1_hash(auth_key) #хешируем аут кей
                auth_key = f"{auth_key}_{time_stamp}"#добавляем к аут кею таймстамп, который будет его сроком годности
                user = account.objects.get(login=form.cleaned_data['email'])#достаем из бд пользователя с соотв. мейл адресом
                user.auth_key = auth_key#присваиваем ему новое значение auth_key
                user.save()#Сохраняем пользователя
                print(auth_key)
                response = HttpResponse("Куки заданы!")#теперь, чтобы сохранить пользователю сессию задаем ему куки
                response.set_cookie('auth_key', auth_key)#задаем куки, куда записываем актуальный аут кей.
                response.set_cookie('login', form.cleaned_data['email'])#задаем куки, куда записываем актуальный логин пользователя
                #каждый раз, когда пользователь будет заходить на сайт будет проверяться аут кей, и если его IP адрес поменялся, либо же срок годности ауткея вышел (1 день), генерим новый
                return redirect('/')#редиректим на главную

            else:#Если логин и пароль не совпадают, человека в систему не впускают
                return HttpResponse('Ошибка: Неверные логин или пароль!')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            count = account.objects.filter(login=form.cleaned_data['email']).count()#Выборка из БД - для проверки существования аккаунта
            if(count <= 0):#Если данный аккаунт не существует
                reg_timestamp1 = datetime.now().strftime('%Y-%m-%d')#Определяем текущий таймстамп и формируем дату
                last_login_timestamp2 = datetime.now().strftime('%Y-%m-%d')#Аналогично определяем текущий таймстамп для записи в дату последнего захода
                new_account = account(#создаем новый экземпляр класса account (из models.py)
                    login=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    sex=form.cleaned_data['sex'],
                    realname=form.cleaned_data['realname'],
                    reg_timestamp=reg_timestamp1,
                    last_login_timestamp=last_login_timestamp2
                )
                new_account.save()#Сохраняем экземпляр в БД
                return redirect('/')#Переносим пользователя на главную страницу
            else:#Если аккаунт уже существует
                print("Ошибка: данный аккаунт уже существует!")
    else:
        print("Ошибка: запрос не типа 'POST'!")
    
    return render(request, 'registration.html', {'form': form})