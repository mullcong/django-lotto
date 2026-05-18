from django.db import models
from django.contrib.auth.models import User


class LottoTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round_number = models.IntegerField()

    number1 = models.IntegerField()
    number2 = models.IntegerField()
    number3 = models.IntegerField()
    number4 = models.IntegerField()
    number5 = models.IntegerField()
    number6 = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def numbers_list(self):
        return [
            self.number1,
            self.number2,
            self.number3,
            self.number4,
            self.number5,
            self.number6,
        ]

    def __str__(self):
        return f"{self.user.username} - {self.round_number}회차"


class LottoResult(models.Model):
    round_number = models.IntegerField(unique=True)

    number1 = models.IntegerField()
    number2 = models.IntegerField()
    number3 = models.IntegerField()
    number4 = models.IntegerField()
    number5 = models.IntegerField()
    number6 = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def numbers_list(self):
        return [
            self.number1,
            self.number2,
            self.number3,
            self.number4,
            self.number5,
            self.number6,
        ]

    def __str__(self):
        return f"{self.round_number}회차 당첨번호"