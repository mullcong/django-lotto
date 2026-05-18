from django.contrib import admin
from .models import LottoTicket, LottoResult


@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'round_number',
        'number1',
        'number2',
        'number3',
        'number4',
        'number5',
        'number6',
        'created_at',
    )


@admin.register(LottoResult)
class LottoResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'round_number',
        'number1',
        'number2',
        'number3',
        'number4',
        'number5',
        'number6',
        'created_at',
    )