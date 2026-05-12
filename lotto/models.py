from django.db import models
from django.contrib.auth.models import User
import random

class LottoDraw(models.Model):
    round_number = models.PositiveIntegerField(unique=True)
    number1 = models.PositiveIntegerField()
    number2 = models.PositiveIntegerField()
    number3 = models.PositiveIntegerField()
    number4 = models.PositiveIntegerField()
    number5 = models.PositiveIntegerField()
    number6 = models.PositiveIntegerField()
    bonus_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def numbers(self):
        return [
            self.number1,
            self.number2,
            self.number3,
            self.number4,
            self.number5,
            self.number6,
        ]

    def __str__(self):
        return f"{self.round_number}회차 추첨 결과"


class LottoTicket(models.Model):
    BUY_TYPE_CHOICES = [
        ("manual", "수동"),
        ("auto", "자동"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round_number = models.PositiveIntegerField()
    buy_type = models.CharField(max_length=10, choices=BUY_TYPE_CHOICES)

    number1 = models.PositiveIntegerField()
    number2 = models.PositiveIntegerField()
    number3 = models.PositiveIntegerField()
    number4 = models.PositiveIntegerField()
    number5 = models.PositiveIntegerField()
    number6 = models.PositiveIntegerField()

    price = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def numbers(self):
        return [
            self.number1,
            self.number2,
            self.number3,
            self.number4,
            self.number5,
            self.number6,
        ]

    @staticmethod
    def generate_auto_numbers():
        return sorted(random.sample(range(1, 46), 6))

    def check_result(self):
        try:
            draw = LottoDraw.objects.get(round_number=self.round_number)
        except LottoDraw.DoesNotExist:
            return "아직 추첨 전"

        ticket_numbers = set(self.numbers())
        winning_numbers = set(draw.numbers())

        match_count = len(ticket_numbers & winning_numbers)
        bonus_match = draw.bonus_number in ticket_numbers

        if match_count == 6:
            return "1등"
        elif match_count == 5 and bonus_match:
            return "2등"
        elif match_count == 5:
            return "3등"
        elif match_count == 4:
            return "4등"
        elif match_count == 3:
            return "5등"
        else:
            return "낙첨"

    def __str__(self):
        return f"{self.user.username} - {self.round_number}회차 복권"


class WinningHistory(models.Model):
    ticket = models.OneToOneField(LottoTicket, on_delete=models.CASCADE)
    result = models.CharField(max_length=20)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.user.username} - {self.result}"