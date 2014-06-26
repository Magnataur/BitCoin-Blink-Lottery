from django.shortcuts import render_to_response, HttpResponse, redirect
from blink_web.models import BitcoinPlayer, Blink, Query, ServerBitcoinAddress
from django import forms
from django.core.context_processors import csrf
from functools import wraps
from django.db import transaction
from django.http import Http404
from BCAddressField import BCAddressField


class LoginForm(forms.Form):
    address = BCAddressField(max_length=64)


def check_login(f):
    @wraps(f)
    def wrapper(request, *args, **kwds):
        if not 'address' in request.session:
            return redirect(to='/login/')
        return f(request, *args, **kwds)
    return wrapper


@check_login
def index(request):
    # Step 1: Get Player from database
    p = BitcoinPlayer.objects.get(address=request.session['address'])

    # Step 2: Get Blinks from database
    bs = Blink.objects.filter(active=True)

    response = {
        'player': p,
        'blinks': bs,
    }
    return render_to_response('index.html', response)


def login(request):
    if not request.POST:
        form = LoginForm()
        response = {
            'form': form,
        }
        response.update(csrf(request))
        return render_to_response('login.html', response)

    form = LoginForm(request.POST)
    if not form.is_valid():
        return HttpResponse('Invalid bitcoin address')

    # Step 1: get or create bitcoin player
    address = form.cleaned_data['address']
    try:
        p = BitcoinPlayer.objects.get(address=address)
    except BitcoinPlayer.DoesNotExist:
        with transaction.atomic():
            p = BitcoinPlayer()
            ws = ServerBitcoinAddress.objects.filter(active=False)
            wallet = ws.first()
            wallet.active = True
            wallet.save()
            p.wallet = wallet
            p.address = address
            p.save()

    # Step 2: save player address to session
    request.session['address'] = p.address

    # Step 3: redirect to index
    return redirect('/')


def logout(request):
    request.session.flush()
    return HttpResponse('You are logged out')


@check_login
def join(request, blink_pk, place):
    blink_pk = int(blink_pk)
    place = int(place)

    # Step 1: get Player from database
    p = BitcoinPlayer.objects.get(address=request.session['address'])

    with transaction.atomic():
        b = Blink.objects.get(pk=blink_pk)
        if not b.active:
            return HttpResponse('The blink is full')

        if place > b.size:
            return HttpResponse('Invalid place, %s, %s, %s' % (place, type(place), b.size))

        # Step 2: check place is free
        q = Query.objects.filter(blink=b, player=p, place=place)
        if q:
            return HttpResponse('The place is occupied')

        # Step 3: add player to blink query
        q = Query(blink=b, player=p, place=place)  # ToDo: player place selection
        q.save()

        # Step 3: check Blink is still active
        qs = Query.objects.filter(blink=b)
        if len(qs) == b.size:
            b.active = False
            b.save()

        # Step 4: get bet from Player
        p.cash -= b.bet
        p.save()

    # Step 3: go to blink page
    return redirect(to='/blink/%s/' % (b.pk, ))


@check_login
def blink(request, blink_pk):

    # Step 1: get Blink and Blink Queue from database
    try:
        b = Blink.objects.get(pk=blink_pk)
    except Blink.DoesNotExist:
        raise Http404

    query = Query.objects.filter(blink=b)
    return HttpResponse('%s active players, cash=%s' % (len(query), b.cash()))


def test(request):
    return render_to_response('test.html')