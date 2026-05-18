import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import LottoTicket, LottoResult


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('home')


def purchase(request):
    return render(request, 'lotto/purchase.html')


@login_required
def auto_purchase(request):
    if request.method == 'POST':
        count = request.POST.get('count')

        try:
            count = int(count)
        except:
            messages.error(request, '구매 개수를 숫자로 입력해주세요.')
            return render(request, 'lotto/auto_purchase.html')

        if count < 1:
            messages.error(request, '1개 이상 구매해야 합니다.')
            return render(request, 'lotto/auto_purchase.html')

        if count > 10:
            messages.error(request, '한 번에 최대 10개까지만 구매할 수 있습니다.')
            return render(request, 'lotto/auto_purchase.html')

        last_result = LottoResult.objects.order_by('-round_number').first()

        if last_result:
            round_number = last_result.round_number + 1
        else:
            round_number = 1

        purchased_tickets = []

        for i in range(count):
            numbers = random.sample(range(1, 46), 6)
            numbers.sort()

            ticket = LottoTicket.objects.create(
                user=request.user,
                round_number=round_number,
                number1=numbers[0],
                number2=numbers[1],
                number3=numbers[2],
                number4=numbers[3],
                number5=numbers[4],
                number6=numbers[5],
            )

            purchased_tickets.append(ticket)

        return render(request, 'lotto/purchase_complete.html', {
            'tickets': purchased_tickets
        })

    return render(request, 'lotto/auto_purchase.html')


@login_required
def manual_purchase(request):
    if request.method == 'POST':
        selected_numbers = request.POST.getlist('numbers')

        if len(selected_numbers) != 6:
            messages.error(request, '번호는 정확히 6개를 선택해야 합니다.')
            return render(request, 'lotto/manual_purchase.html')

        try:
            numbers = []

            for number in selected_numbers:
                numbers.append(int(number))

        except:
            messages.error(request, '잘못된 번호가 포함되어 있습니다.')
            return render(request, 'lotto/manual_purchase.html')

        if len(numbers) != len(set(numbers)):
            messages.error(request, '중복된 번호는 선택할 수 없습니다.')
            return render(request, 'lotto/manual_purchase.html')

        for number in numbers:
            if number < 1 or number > 45:
                messages.error(request, '번호는 1부터 45까지만 선택할 수 있습니다.')
                return render(request, 'lotto/manual_purchase.html')

        numbers.sort()

        last_result = LottoResult.objects.order_by('-round_number').first()

        if last_result:
            round_number = last_result.round_number + 1
        else:
            round_number = 1

        ticket = LottoTicket.objects.create(
            user=request.user,
            round_number=round_number,
            number1=numbers[0],
            number2=numbers[1],
            number3=numbers[2],
            number4=numbers[3],
            number5=numbers[4],
            number6=numbers[5],
        )

        return render(request, 'lotto/purchase_complete.html', {
            'ticket': ticket
        })

    return render(request, 'lotto/manual_purchase.html')


@login_required
def purchase_complete(request):
    return render(request, 'lotto/purchase_complete.html')


@login_required
def my_tickets(request):
    tickets = LottoTicket.objects.filter(user=request.user).order_by('-round_number', '-id')

    lotto_results = LottoResult.objects.all()

    result_map = {}

    for result in lotto_results:
        result_map[result.round_number] = [
            result.number1,
            result.number2,
            result.number3,
            result.number4,
            result.number5,
            result.number6,
        ]

    grouped_map = {}

    for ticket in tickets:
        ticket_numbers = [
            ticket.number1,
            ticket.number2,
            ticket.number3,
            ticket.number4,
            ticket.number5,
            ticket.number6,
        ]

        winning_numbers = result_map.get(ticket.round_number, [])

        number_list = []

        for number in ticket_numbers:
            if number in winning_numbers:
                number_list.append({
                    'value': number,
                    'matched': True
                })
            else:
                number_list.append({
                    'value': number,
                    'matched': False
                })

        if ticket.round_number not in grouped_map:
            grouped_map[ticket.round_number] = {
                'round_number': ticket.round_number,
                'winning_numbers': winning_numbers,
                'tickets': []
            }

        grouped_map[ticket.round_number]['tickets'].append({
            'id': ticket.id,
            'created_at': ticket.created_at,
            'numbers': number_list
        })

    grouped_tickets = list(grouped_map.values())

    return render(request, 'lotto/my_tickets.html', {
        'grouped_tickets': grouped_tickets
    })


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def lotto_admin_home(request):
    return render(request, 'lotto/lotto_admin_home.html')


@user_passes_test(is_admin)
def sales_history(request):
    tickets = LottoTicket.objects.all().order_by('-round_number', '-id')

    return render(request, 'lotto/sales_history.html', {
        'tickets': tickets
    })


@user_passes_test(is_admin)
def draw_lotto(request):
    if request.method == 'POST':
        last_result = LottoResult.objects.order_by('-round_number').first()

        if last_result:
            round_number = last_result.round_number + 1
        else:
            round_number = 1

        numbers = random.sample(range(1, 46), 6)
        numbers.sort()

        result = LottoResult.objects.create(
            round_number=round_number,
            number1=numbers[0],
            number2=numbers[1],
            number3=numbers[2],
            number4=numbers[3],
            number5=numbers[4],
            number6=numbers[5],
        )

        return render(request, 'lotto/draw_result.html', {
            'result': result,
            'numbers': numbers
        })

    return render(request, 'lotto/draw_lotto.html')


@user_passes_test(is_admin)
def winning_history(request):
    results = LottoResult.objects.all().order_by('-round_number')

    return render(request, 'lotto/winning_history.html', {
        'results': results
    })


@login_required
def check_result(request):
    tickets = LottoTicket.objects.filter(user=request.user).order_by('-round_number', '-id')
    results = LottoResult.objects.all()

    result_map = {}

    for result in results:
        result_map[result.round_number] = [
            result.number1,
            result.number2,
            result.number3,
            result.number4,
            result.number5,
            result.number6,
        ]

    checked_tickets = []

    for ticket in tickets:
        ticket_numbers = [
            ticket.number1,
            ticket.number2,
            ticket.number3,
            ticket.number4,
            ticket.number5,
            ticket.number6,
        ]

        winning_numbers = result_map.get(ticket.round_number, [])

        matched_numbers = []

        for number in ticket_numbers:
            if number in winning_numbers:
                matched_numbers.append(number)

        checked_tickets.append({
            'ticket': ticket,
            'numbers': ticket_numbers,
            'winning_numbers': winning_numbers,
            'matched_numbers': matched_numbers,
            'match_count': len(matched_numbers),
        })

    return render(request, 'lotto/check_result.html', {
        'checked_tickets': checked_tickets
    })