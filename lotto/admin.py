from django.contrib import admin
from .models import LottoTicket, LottoDraw, WinningHistory

admin.site.register(LottoTicket)
admin.site.register(LottoDraw)
admin.site.register(WinningHistory)