from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserRegistrationForm, NewMessegeform, verifyform, loginform, openform
from django.contrib.auth.decorators import login_required
from .server import Server
from random import randrange, getrandbits
from .models import Messeges, User, Revocation_list, revocation_requests
from sympy.core.numbers import igcdex
import hashlib, zlib
from django.contrib import messages
from Lib import base64



def register_user(request):
    if request.user.is_authenticated():
        messages.error(request, "Please Logout For Registering as New User", extra_tags=True)
        return HttpResponseRedirect('/home/')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                login(request, user)
                messages.success(request, ' Registration Successful !', extra_tags=False)
                return HttpResponseRedirect('/home/')
        else:
            form = UserRegistrationForm()
        return render(request, 'Groupsign/registration/register.html', {'form': form})


'''
def user_login(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/home/")
    else:
        form = loginform()
        return HttpResponseRedirect(request, 'Groupsign/registration/login.html',{'form':form})
'''


def user_login(request):
    if request.user.is_authenticated():
        msg = "Already Loged In as '"+str(request.user.get_username())+"'. Logout First !"
        messages.error(request, msg, extra_tags=True)
        return HttpResponseRedirect('/home/')
    else:
        if request.method == 'POST':
            form = loginform(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect("/home/")
                    else:
                        messages.error(request, ' Youre account is disabled !', extra_tags=True)
                        return HttpResponseRedirect('/login/')
                else:
                    messages.error(request, " Username And Password Didn't Match !", extra_tags=True)
                    return HttpResponseRedirect('/login/')
        else:
            form = loginform
            return render(request, 'Groupsign/registration/login.html', {'form': form})


def home(request):
    if request.method == 'POST':
        server1 = Server
        [K, Lp, LAM1, LAM2, GAMA1, GAMA2] = server1.get_security_parameters(server1)
        [N, A, A0, Y, G] = server1.get_public_key(server1)
        M_verify = request.POST['title'] + request.POST['text']
        C = int(request.POST['C'])
        S1 = int(request.POST['S1'])
        S2 = int(request.POST['S2'])
        S3 = int(request.POST['S3'])
        T1 = int(request.POST['T1'])
        T2 = int(request.POST['T2'])
        T3 = int(request.POST['T3'])

        T1_INV = igcdex(T1, N)[0] % N
        T2_INV = igcdex(T2, N)[0] % N

        INV_A = igcdex(A, N)[0] % N
        INV_Y = igcdex(Y, N)[0] % N
        INV_G = igcdex(G, N)[0] % N

        Numerator_part = (pow(A0, C, N) * pow(T1, S1, N) * pow(T1_INV, (C * 2 ** GAMA1), N)) % N
        Denomirator_part = (pow(INV_A, S2, N) * pow(A, C * 2 ** LAM1, N) * pow(INV_Y, S3, N)) % N
        D1_Cal = (Numerator_part * Denomirator_part) % N

        Numerator_part1 = (pow(T2, S1, N) * pow(T2_INV, C * 2 ** GAMA1, N)) % N
        Denomirator_part1 = pow(INV_G, S3, N)
        D2_Cal = (Numerator_part1 * Denomirator_part1) % N

        D3_Cal = (pow(T2, S1, N) * pow(T2_INV, C * 2 ** GAMA1, N) * pow(T3, C, N)) % N


        hashobj2 = str(G).encode('utf-8') + str(Y).encode('utf-8') + str(A0).encode(
            'utf-8') + str(A).encode('utf-8') + str(T1).encode('utf-8') + str(T2).encode('utf-8') + str(T3).encode(
            'utf-8') + str(D1_Cal).encode('utf-8') + str(D2_Cal).encode('utf-8') + str(D3_Cal).encode('utf-8') + M_verify.encode('utf-8')
        C_DASH = zlib.crc32(hashobj2)
        is_revoked = False
        revoke = Revocation_list.objects.all()
        if revoke is not None:
            for list in revoke:
                if (pow(T2, int(list.Ei), N) == T3):
                    is_revoked = True

        if C == C_DASH and is_revoked is False:
            messages.success(request, ' Messege Is Correct !', extra_tags=False)
            return HttpResponseRedirect('/home/')
        else:
            messages.error(request, ' Messege Is False !', extra_tags=True)
            return HttpResponseRedirect('/home/')
    else:
        messeges = Messeges.objects.order_by('-time')
        return render(request, 'Groupsign/home.html', {'messeges': messeges})


def about_view(request):
    return render(request, 'Groupsign/about.html')


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    messages.success(request, ' You are Loged Out Now !', extra_tags=False)
    return HttpResponseRedirect("/home/")


@login_required(login_url='/login/')
def user_join(request):
    U = request.user
    if U.sign_created is True:
        messages.error(request, ' You have already joined !', extra_tags=True)
        return HttpResponseRedirect("/home/")
    else:
        server1 = Server
        [K, Lp, LAM1, LAM2, GAMA1, GAMA2] = server1.get_security_parameters(server1)
        [N, A, A0, Y, G] = server1.public_key
        Xi = 0
        Ai = False
        Ei = False

        while Ai is False and Ei is False:
            CHECK = False
            while CHECK is False:
                XXi = randrange(0, 2 ** LAM2)
                C1 = pow(G, XXi, N)
                [ALFAi, BETAi] = server1.get_alfa_beta(server1, Num=C1)

                if ALFAi and BETAi:
                    CHECK = True

            Xi = 2 ** LAM1 + (ALFAi * XXi + BETAi) % (2 ** LAM2)
            C2 = pow(A, Xi, N)
            [Ai, Ei] = server1.get_member_cert(server1, Num=C2)

        print(Ai, Ei)
        if pow((pow(A, Xi, N) * pow(A0, 1, N)), 1, N) == pow(Ai, Ei, N):
            U.Ai = str(Ai)
            U.Ei = str(Ei)
            U.Xi = str(Xi)
            U.sign_created = True
            U.save()
            messages.success(request, ' Join Successful !', extra_tags=False)
            return HttpResponseRedirect("/home/")
        else:
            messages.warning(request, ' Error Occured ! Try again ! !', extra_tags=True)
            return HttpResponseRedirect("/home/")


@login_required(login_url='/login/')
def new_messege_view(request):
    if request.method == 'POST':
        U = request.user
        server1 = Server
        [K, Lp, LAM1, LAM2, GAMA1, GAMA2] = server1.get_security_parameters(server1)
        [N, A, A0, Y, G] = server1.get_public_key(server1)
        Ai = int(U.Ai)
        Ei = int(U.Ei)
        Xi = int(U.Xi)
        M = request.POST['title'] + request.POST['text']

        W = randrange(0, 2 ** (2 * Lp))

        T1 = (Ai * pow(Y, W, N)) % N
        T2 = pow(G, W, N)
        T3 = pow(T2, Ei, N)

        R1 = getrandbits(GAMA2 + 128 * K)
        R2 = getrandbits(LAM1 + 128 * K)
        R3 = getrandbits(GAMA1 + 2 * Lp + 128 * K + 1)

        INV_A = igcdex(A, N)[0] % N
        INV_Y = igcdex(Y, N)[0] % N
        INV_G = igcdex(G, N)[0] % N

        D1 = (pow(T1, R1, N) * (pow(INV_A, R2, N) * pow(INV_Y, R3, N))) % N
        D2 = (pow(T2, R1, N) * pow(INV_G, R3, N)) % N
        D3 = pow(T2, R1, N)


        hashobj = str(G).encode('utf-8') + str(Y).encode('utf-8') + str(A0).encode(
            'utf-8') + str(A).encode('utf-8') + str(T1).encode('utf-8') + str(T2).encode('utf-8') + str(T3).encode(
            'utf-8') + str(D1).encode('utf-8') + str(D2).encode('utf-8') + str(D3).encode('utf-8') + M.encode('utf-8')
        C = zlib.crc32(hashobj)

        S1 = R1 - C * (Ei - 2 ** GAMA1)
        S2 = R2 - C * (Xi - 2 ** LAM1)
        S3 = R3 - C * Ei * W

        inst = Messeges.objects.create()
        inst.title = request.POST['title']
        inst.text = request.POST['text']
        inst.C = str(C)
        inst.S1 = str(S1)
        inst.S2 = str(S2)
        inst.S3 = str(S3)
        inst.T1 = str(T1)
        inst.T2 = str(T2)
        inst.T3 = str(T3)

        inst.save()
        messages.success(request, ' Messege Signed and Posted successfully !',extra_tags=False)
        return HttpResponseRedirect('/newmessege/')
    else:
        form = NewMessegeform()
        return render(request, 'Groupsign/newmessege.html', {'form': form})


def verify_view(request):
    if request.method == 'POST':
        server1 = Server
        [K, Lp, LAM1, LAM2, GAMA1, GAMA2] = server1.get_security_parameters(server1)
        [N, A, A0, Y, G] = server1.get_public_key(server1)
        M_verify = request.POST['title'] + request.POST['text']
        C = int(request.POST['C'])
        S1 = int(request.POST['S1'])
        S2 = int(request.POST['S2'])
        S3 = int(request.POST['S3'])
        T1 = int(request.POST['T1'])
        T2 = int(request.POST['T2'])
        T3 = int(request.POST['T3'])

        T1_INV = igcdex(T1, N)[0] % N
        T2_INV = igcdex(T2, N)[0] % N

        INV_A = igcdex(A, N)[0] % N
        INV_Y = igcdex(Y, N)[0] % N
        INV_G = igcdex(G, N)[0] % N

        Numerator_part = (pow(A0, C, N) * pow(T1, S1, N) * pow(T1_INV, (C * 2 ** GAMA1), N)) % N
        Denomirator_part = (pow(INV_A, S2, N) * pow(A, C * 2 ** LAM1, N) * pow(INV_Y, S3, N)) % N
        D1_Cal = (Numerator_part * Denomirator_part) % N

        Numerator_part1 = (pow(T2, S1, N) * pow(T2_INV, C * 2 ** GAMA1, N)) % N
        Denomirator_part1 = pow(INV_G, S3, N)
        D2_Cal = (Numerator_part1 * Denomirator_part1) % N

        D3_Cal = (pow(T2, S1, N) * pow(T2_INV, C * 2 ** GAMA1, N) * pow(T3, C, N)) % N

        hashobj2 = str(G).encode('utf-8') + str(Y).encode('utf-8') + str(A0).encode(
            'utf-8') + str(A).encode('utf-8') + str(T1).encode('utf-8') + str(T2).encode('utf-8') + str(T3).encode(
            'utf-8') + str(D1_Cal).encode('utf-8') + str(D2_Cal).encode('utf-8') + str(D3_Cal).encode('utf-8') + M_verify.encode('utf-8')
        C_DASH = zlib.crc32(hashobj2)
        is_revoked = False
        revoke = Revocation_list.objects.all()
        if revoke is not None:
            for list in revoke:
                if (pow(T2, int(list.Ei), N) == T3):
                    is_revoked = True
        if C == C_DASH and is_revoked is False:
            messages.success(request, ' Messege Is Correct !', extra_tags=False)
            return HttpResponseRedirect('/verify/')
        else:
            messages.error(request, ' Messege Is False !', extra_tags=True)
            return HttpResponseRedirect('/verify/')
    else :
        form = verifyform()
        return render(request, 'Groupsign/verify.html', {'form': form})


@login_required(login_url='/login/')
def open_view(request):
    if request.user.is_opening_manager:
        if request.method == 'POST':
            server1 = Server
            [N, A, A0, Y, G] = server1.public_key
            X = server1.X
            T1 = int(request.POST['T1'])
            T2 = int(request.POST['T2'])
            T2_INV = igcdex(T2, N)[0] % N
            Ai_Check = (T1 * pow(T2_INV, X, N)) % N
            try:
                openuser = User.objects.get(Ai=Ai_Check)
                if openuser is None:
                    messages.error(request, ' No User Is Found !', extra_tags=True)
                    return HttpResponseRedirect('/open/')
                else:
                    return render(request, 'Groupsign/Ai_show.html', {'Ai_Check': Ai_Check, 'openuser': openuser})
            except User.DoesNotExist:
                messages.error(request, ' No User Is Found !', extra_tags=True)
                return HttpResponseRedirect('/open/')
        else:
            form = openform()
            return render(request, 'Groupsign/openform.html', {'form': form})
    else:
        messages.error(request, ' You Do not Have this Privilege !', extra_tags=True)
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def revocation_request_view(request):
    if request.user.is_opening_manager:
        if request.method == 'POST':
            try:
                revocation_Ai = Revocation_list.objects.get(Ai=request.POST['Ai'])
            except Revocation_list.DoesNotExist:
                revocation_Ai = None
            if revocation_Ai is None:
                try:
                    revocation_request_Ai = revocation_requests.objects.get(Ai=request.POST['Ai'])
                except revocation_requests.DoesNotExist:
                    revocation_request_Ai = None
                if revocation_request_Ai is None:
                    revocation_request = revocation_requests.objects.create()
                    revocation_request.Ai = request.POST['Ai']
                    revocation_request.Ei = request.POST['Ei']
                    revocation_request.completed = False
                    revocation_request.save()
                    messages.success(request, ' Request Sent Successfully !', extra_tags=False)
                    return HttpResponseRedirect('/open/')
                else:
                    messages.error(request, ' Already requested for Revocation !', extra_tags=True)
                    return HttpResponseRedirect('/open/')
            else:
                messages.error(request, ' User is Already Revoked !', extra_tags=True)
                return HttpResponseRedirect('/open/')
        else:
            messages.error(request, ' Form Error ! Submit Again', extra_tags=True)
            return HttpResponseRedirect('/open/')
    else:
        messages.error(request, ' You Do not Have this Privilege !', extra_tags=True)
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def revoke_list_add_view(request):
    if request.user.is_revocation_manager:
        if request.method == 'POST':
            if 'revoke' in request.POST:
                revocation_request = revocation_requests.objects.get(Ai=request.POST['Ai'])
                revocation_list = Revocation_list.objects.create()
                user = User.objects.get(Ai=request.POST['Ai'])
                revocation_list.Ai = request.POST['Ai']
                revocation_list.Ei = request.POST['Ei']
                revocation_request.completed = True
                user.is_revoked = True
                revocation_list.save()
                revocation_request.save()
                user.save()
                messages.success(request, ' User Revoked Successfully !', extra_tags=False)
                return HttpResponseRedirect('/revoke/')
            elif 'discard' in request.POST:
                revocation_request = revocation_requests.objects.get(Ai=request.POST['Ai'])
                revocation_request.delete()
                messages.success(request, ' Request Discarded Successfully !', extra_tags=False)
                return HttpResponseRedirect('/revoke/')
        else:
            revoke_reqest = revocation_requests.objects.filter(completed=False).order_by('-time')
            return render(request, 'Groupsign/revoke_reqest.html', {'revoke_reqest': revoke_reqest})
    else:
        messages.error(request, ' You Do not Have this Privilege !', extra_tags=True)
        return HttpResponseRedirect('/home/')


def revoke_list_view(request):
    revoke_list = Revocation_list.objects.all()
    return render(request, 'Groupsign/revoke_list.html', {'revoke_list': revoke_list})