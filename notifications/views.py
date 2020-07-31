from django.shortcuts import render
from planes.models import Contract

from datetime import date, timedelta
# import locale

# Create your views here.


def index(request):

    # obj_list = Contract.objects.all()
    obj_list = Contract.objects.exclude(contract_active=False)
    # obj_list = Contract.objects.all().order_by('title')
    notes_list = []
    today = date.today()

    # задаем локаль для вывода даты на русском языке 'ru'
    # locale.setlocale(locale.LC_ALL, "ru")

    for obj in obj_list:

        delta = (obj.plan_load_date_ASEZ - today).days
        # проверка дополнительно, чтобы фактической загрузки еще не было
        if (obj.fact_load_date_ASEZ is None and delta < 31):
        # if (delta < 31):
            if (delta < 21):
                if (delta < 4):
                    notes_list.append({
                        "type": 'plan_load_date_ASEZ',
                        "date_txt": (obj.plan_load_date_ASEZ-timedelta(3)).strftime("%d.%m.%Y"),
                        "date": (obj.plan_load_date_ASEZ-timedelta(3)),
                        "text": 'До загрузки в АСЭЗ договора < ' + obj.title + ' > осталось 3 дня',
                    })
                else:
                    notes_list.append({
                        "type": 'plan_load_date_ASEZ',
                        "date_txt": (obj.plan_load_date_ASEZ-timedelta(20)).strftime("%d.%m.%Y"),
                        "date": (obj.plan_load_date_ASEZ-timedelta(20)),
                        "text": 'До загрузки в АСЭЗ договора < ' + obj.title + ' > осталось 20 дней',
                    })
            else:
                notes_list.append({
                    "type": 'plan_load_date_ASEZ',
                    "date_txt": (obj.plan_load_date_ASEZ-timedelta(30)).strftime("%d.%m.%Y"),
                    "date": (obj.plan_load_date_ASEZ-timedelta(30)),
                    "text": 'До загрузки в АСЭЗ договора < ' + obj.title + ' > осталось 30 дней',
                })

        delta = (obj.plan_sign_date - today).days
        # проверка дополнительно, чтобы фактического подписания еще не было
        if (obj.fact_sign_date is None and delta < 31):
        # if (delta < 31):
            notes_list.append({
                "type": 'plan_sign_date',
                "date_txt": (obj.plan_sign_date - timedelta(30)).strftime("%d.%m.%Y"),
                "date": (obj.plan_sign_date - timedelta(30)),
                "text": 'До планируемой даты заключения договора < ' + obj.title + ' > осталось 30 дней',
            })

        if (obj.end_time is not None):
            delta = (obj.end_time - today).days
            if (delta < 31):
                notes_list.append({
                    "type": 'end_time',
                    "date_txt": (obj.end_time - timedelta(30)).strftime("%d.%m.%Y"),
                    "date": (obj.end_time - timedelta(30)),
                    "text": 'Срок действия договора  < ' + obj.title + ' > истекает через 30 дней',
                })

    notes_list.sort(key=lambda x: x['date'], reverse=True)
    context = {'notes_list': notes_list}
    return render(request, 'notifications/index.html', context)
