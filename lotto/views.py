from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import LottoTicket, LottoDraw, WinningHistory
from .forms import ManualLottoForm, AutoLottoForm, DrawLottoForm
import random


def is_admin(user):
    return user.is_staff or user.is_superuser


def home(request):
    return render(request, "lotto/home.html")


@login_required
def buy_manual(request):
    if request.method == "POST":
        form = ManualLottoForm(request.POST)

        if form.is_valid():
            numbers = sorted([
                form.cleaned_data["number1"],
                form.cleaned_data["number2"],
                form.cleaned_data["number3"],
                form.cleaned_data["number4"],
                form.cleaned_data["number5"],
                form.cleaned_data["number6"],
            ])

            LottoTicket.objects.create(
                user=request.user,
                round_number=form.cleaned_data["round_number"],
                buy_type="manual",
                number1=numbers[0],
                number2=numbers[1],
                number3=numbers[2],
                number4=numbers[3],
                number5=numbers[4],
                number6=numbers[5],
            )

            messages.success(request, "수동 로또 구매가 완료되었습니다.")
            return redirect("my_tickets")
    else:
        form = ManualLottoForm()

    return render(request, "lotto/buy_manual.html", {"form": form})


@login_required
def buy_auto(request):
    if request.method == "POST":
        form = AutoLottoForm(request.POST)

        if form.is_valid():
            numbers = LottoTicket.generate_auto_numbers()

            LottoTicket.objects.create(
                user=request.user,
                round_number=form.cleaned_data["round_number"],
                buy_type="auto",
                number1=numbers[0],
                number2=numbers[1],
                number3=numbers[2],
                number4=numbers[3],
                number5=numbers[4],
                number6=numbers[5],
            )

            messages.success(request, f"자동 번호 {numbers} 구매가 완료되었습니다.")
            return redirect("my_tickets")
    else:
        form = AutoLottoForm()

    return render(request, "lotto/buy_auto.html", {"form": form})


@login_required
def my_tickets(request):
    tickets = LottoTicket.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "lotto/my_tickets.html", {"tickets": tickets})


@login_required
def check_result(request):
    tickets = LottoTicket.objects.filter(user=request.user).order_by("-created_at")

    results = []

    for ticket in tickets:
        result = ticket.check_result()

        if result != "아직 추첨 전":
            WinningHistory.objects.update_or_create(
                ticket=ticket,
                defaults={"result": result}
            )

        results.append({
            "ticket": ticket,
            "result": result,
        })

    return render(request, "lotto/check_result.html", {"results": results})


@user_passes_test(is_admin)
def admin_dashboard(request):
    total_sales = LottoTicket.objects.count() * 1000
    total_tickets = LottoTicket.objects.count()
    total_draws = LottoDraw.objects.count()

    context = {
        "total_sales": total_sales,
        "total_tickets": total_tickets,
        "total_draws": total_draws,
    }

    return render(request, "lotto/admin_dashboard.html", context)


@user_passes_test(is_admin)
def draw_lotto(request):
    if request.method == "POST":
        form = DrawLottoForm(request.POST)

        if form.is_valid():
            round_number = form.cleaned_data["round_number"]

            if LottoDraw.objects.filter(round_number=round_number).exists():
                messages.error(request, "이미 해당 회차의 추첨 결과가 존재합니다.")
                return redirect("draw_lotto")

            numbers = sorted(random.sample(range(1, 46), 6))

            remaining_numbers = list(set(range(1, 46)) - set(numbers))
            bonus_number = random.choice(remaining_numbers)

            LottoDraw.objects.create(
                round_number=round_number,
                number1=numbers[0],
                number2=numbers[1],
                number3=numbers[2],
                number4=numbers[3],
                number5=numbers[4],
                number6=numbers[5],
                bonus_number=bonus_number,
            )

            tickets = LottoTicket.objects.filter(round_number=round_number)

            for ticket in tickets:
                result = ticket.check_result()
                WinningHistory.objects.update_or_create(
                    ticket=ticket,
                    defaults={"result": result}
                )

            messages.success(request, f"{round_number}회차 추첨이 완료되었습니다.")
            return redirect("winning_history")
    else:
        form = DrawLottoForm()

    draws = LottoDraw.objects.all().order_by("-round_number")

    return render(request, "lotto/draw_lotto.html", {
        "form": form,
        "draws": draws,
    })


@user_passes_test(is_admin)
def sales_history(request):
    tickets = LottoTicket.objects.all().order_by("-created_at")
    total_sales = tickets.count() * 1000

    return render(request, "lotto/sales_history.html", {
        "tickets": tickets,
        "total_sales": total_sales,
    })


@user_passes_test(is_admin)
def winning_history(request):
    histories = WinningHistory.objects.all().order_by("-checked_at")

    return render(request, "lotto/winning_history.html", {
        "histories": histories,
    })