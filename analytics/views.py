from django.shortcuts import render
from .forms import RDKZForm
from planes.models import Contract, Counterpart, PurchaseType, NumberPZTRU, SumsRUR, ContractStatus, ContractRemarks, SumsBYN, Currency
import datetime

def analytics(request):
    response = {}
    return render(request, './analytics/analytics.html', response)

def report_RKDZ(request):
    if request.method == 'GET':
        form=RDKZForm()
        response = {'form':form}
    form = RDKZForm()
    response = {'form': form}
    return render(request, './analytics/report_RKDZ.html', response)


def report_RKDZ_table(request):
    TABLE_LEGEND={
        "counterpart":"Контрагент",
        "fact_sign_date":"Дата заключения договора",
        "contract_number":"Номер договора",
        "title":"Наименование договора",
        "purchase_type":"Тип закупки",
        "number_ppz":"№ ППЗ",
        "number_PZTRU":"№ пункта Положения о закупках товаров, работ, услуг",
        "contract_sum_NDS_RUB":"Первоначальная цена договора, в рос.руб.",
        "contract_sum_NDS_RUB_sub":"Общая цена договора с учетом всех дополнительных соглашений, рос.руб.",
        "contract_status":"Статус договора",
        "ContractRemarks":"Примечание",
        "subsidiary":"Подразделение",
        "register_number_SAP":"Регистрационный № SAP",
        "start_max_price_ASEZ_NDS":"НМЦ АСЭЗ с НДС, рос.руб.",
        "currency_rate_on_load_date_ASEZ_NDS":"Курс в АСЭЗ",
        "contract_sum_with_NDS_BYN":"Сумма договора в SAP с НДС, бел.руб.",
        "contract_sum_NDS_RUB_2":"Сумма договора, рос.руб.",
        "currency":"Валюта договора"

    }
    CATALOG_FIELDS=[
        "counterpart",
        "purchase_type",
        "number_PZTRU",
        "contract_sum_NDS_RUB",
        "contract_sum_NDS_RUB_sub",
        "contract_status",
        "ContractRemarks",
        "subsidiary",
        "start_max_price_ASEZ_NDS",
        "currency_rate_on_load_date_ASEZ_NDS",
        "contract_sum_with_NDS_BYN",
        "contract_sum_NDS_RUB_2",
        "currency"
    ]
    final_fields=[]
    contracts=Contract.objects.all()
    mystery=[]
    super_list = []
    y = datetime.datetime.now().year
    if request.method=="GET":
        fields=request.GET
        for f in fields.keys():
            final_fields.append((str(TABLE_LEGEND[f]).replace("'","").replace("[","").replace("]",""), f))
            mystery.append(str(f))

    contr_count = 0
    for contr in Contract.objects.filter(contract_active='True').values():
        contr_count += 1
        contr_info=[]
        contr_info.append(contr_count)
        for mir in mystery:
            for key in contr.keys():
                if mir in key:
                    if mir in CATALOG_FIELDS:
                        if mir == 'counterpart':
                            try:
                                contr_info.append(Counterpart.objects.filter(id=contr[key]).values('name')[0]['name'])
                            except:
                                contr_info.append('-')
                        elif mir == 'purchase_type':
                            try:
                                contr_info.append(PurchaseType.objects.filter(id=contr[key]).values('title')[0]['title'])
                            except:
                                contr_info.append('-')
                        elif mir == "number_PZTRU":
                            try:
                                contr_info.append(NumberPZTRU.objects.filter(id=contr[key]).values('title')[0]['title'])
                            except:
                                contr_info.append('-')
                        elif mir == "contract_status":
                            try:
                                contr_info.append(ContractStatus.objects.filter(id=contr[key]).values('title')[0]['title'])
                            except:
                                contr_info.append('-')
                    else:
                        contr_info.append(contr[key])

            if mir == "contract_sum_NDS_RUB":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year=y).values(
                        'contract_sum_NDS_RUB')[0]['contract_sum_NDS_RUB'])
                except:
                    contr_info.append('-')
            elif mir == "contract_sum_NDS_RUB_sub":
                number_ppz = contr['number_ppz']
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__number_ppz=number_ppz, year='2020').aggregate(sum=Sum('contract_sum_NDS_RUB'))['sum'])
                except:
                    contr_info.append('-')
            elif mir == "ContractRemarks":
                try:
                    contr_info.append(ContractRemarks.objects.filter(contract__id=contr['id']).values(
                        'remark_text')[0]['remark_text'])
                except:
                    contr_info.append('-')
            elif mir == "subsidiary":
                contr_info.append("Филиал Минское УМГ")
            elif mir == "start_max_price_ASEZ_NDS":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year=y).values(
                        'start_max_price_ASEZ_NDS')[0]['start_max_price_ASEZ_NDS'])
                except:
                    contr_info.append('-')
            elif mir == "currency_rate_on_load_date_ASEZ_NDS":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year=y).values(
                        'currency_rate_on_load_date_ASEZ_NDS')[0]['currency_rate_on_load_date_ASEZ_NDS'])
                except:
                    contr_info.append('-')
            elif mir == "contract_sum_with_NDS_BYN":
                try:
                    contr_info.append(SumsBYN.objects.filter(contract__id=contr['id'], year='2020').values(
                        'contract_sum_with_NDS_BYN')[0]['contract_sum_with_NDS_BYN'])
                except:
                    contr_info.append('-')
            elif mir == "contract_sum_NDS_RUB_2":
                try:
                    contr_info.append(SumsRUR.objects.filter(contract__id=contr['id'], year=y).values(
                        'contract_sum_NDS_RUB')[0]['contract_sum_NDS_RUB'])
                except:
                    contr_info.append('-')
            elif mir == "currency":

                try:
                    cur = SumsRUR.objects.filter(contract__id=contr['id'], year=y).values(
                        'currency')[0]['currency']
                    contr_info.append(Currency.objects.filter(id=cur).values(
                        'title')[0]['title'])
                except:
                    contr_info.append('-')

        super_list.append(contr_info)

    for item in super_list:
        for each in item:
            if not each:
                a = item.index(each)
                b = super_list.index(item)
                super_list[b][a] = "-"

    response = {
        "final_fields":final_fields,
        "len":range(1, (len(final_fields) + 2)),
        "contracts":contracts,
        "mystery":mystery,
        "super_list":super_list
        }
    return render(request, './analytics/report_RKDZ_table.html', response)

RKDZ_ADD = [
        ("Статья финансирования", "Из реестра графа 'Статья финансирования'", "finance_cost"),
        ("Куратор", "Из реестра графа 'Куратор'", "curator"),
        ("Тип договора", "Из реестра графа 'Тип договора'", "contract_type"),
        ("Вид договора", "Из реестра графа 'Вид договора'", "contract_mode"),
        ("Вид деятельности", "Из реестра графа 'Вид деятельности'", "activity_form"),
        ("Состояние в АСЭЗ", "Из реестра графа 'Состояние в Автоматизированной системе эллектронных закупок'", "stateASEZ"),
        ("Планируемая дата загрузки в АСЭЗ", "Из реестра графа 'Планируемая дата загрузки в АСЭЗ'", "plan_load_date_ASEZ"),
        ("Фактическая дата загрузки в АСЭЗ", "Из реестра графа 'Фактическая дата загрузки в АСЭЗ'", "fact_load_date_ASEZ"),
        ("Номер договора от центрального органа", "Из реестра графа 'Номер договора от центрального органа'", "number_KGG"),
        ("Планируемая дата подписания договора", "Из реестра графа 'Планируемая дата подписания договора'", "plan_sign_date"),
        ("Фактическая дата подписания договора", "Из реестра графа 'Фактическая дата подписания договора'", "fact_sign_date"),
        ("Дата начала контракта", "Из реестра графа 'Дата начала контракта'", "start_date"),
        ("Сумма всего договора без НДС", "Из реестра графа 'Сумма всего договора без НДС'", "contract_sum_without_NDS_BYN"),
        ("Прогноз", "Из реестра графа 'Прогноз'", "forecast_total"),
        ("Экономия по заключенному договору", "Из реестра графа 'Экономия по заключенному договору'", "economy_total"),
        ("Факт, всего", "Из реестра графа 'Факт, всего'", "fact_total"),
        ("Абсолютная экономия по договору, всего", "Из реестра графа 'Абсолютная экономия по договору, всего'", "economy_total_absolute"),
        ]

def RKDZ_add(request):
    response = {
        "ADD":RKDZ_ADD
    }
    return render(request, './analytics/RKDZ_add.html', response)

def RKDZ_template(request):
    RKDZ_TEMPLATE = [
        ("Наименование контрагента", "Из реестра графа 'Контрагент'"),
        ("Дата заключения", "Из реестра графа 'Дата заключения'"),
        ("Номер договора", "Из реестра графа 'Номер договора'"),
        ("Предмет договора", "Из реестра графа 'Наименование договора'"),
        ("Способ закупки", "Из реестра графа 'Способ закупки'"),
        ("№ ППЗ", "Из реестра '№ ППЗ АСЭЗ'"),
        ("Номер пункта Положения о закупках товаров, работ, услуг ПАО 'Газпром' и компаний группы Газпром № 3168", "Из реестра графа '№ Пункта Положения о закупках'"),
        ("Первоначальная цена договора в рос.руб.", "Из реестра графа 'Сумма заключенного договора с НДС, рос.руб."),
        ("Общая цена договора с учетом всех дополнительных соглашений, рос.руб.", "Из карточки договора сумма по основному договору и дополнительным соглашениям по данному договору"),
        ("Статус договора", "Из реестра графа 'Статус договора'"),
        ("Примечание", "Редактируемое поле в карточке договора"),
        ("Подразделение", "Филиал Минское УМГ"),
        ("Регистрационный № SAP", "Из реестра графа 'Регистрационный номер SAP'"),
        ("НМЦ АСЭЗ с НДС, рос.руб.", "Из реестра графа 'Начальная максимальная цена АСЭЗ с НДС, рос.руб.'"),
        ("Курс в АСЭЗ", "Из реестра графа 'Курс валют в АСЭЗ'"),
        ("Сумма договора в SAP с НДС, бел.руб.", "Сумма заключенного договора с НДС, всего, бел.руб."),
        ("Сумма договора в RUB", "Из реестра графа 'Сумма заключенного договора с НДС, рос.руб.'"),
        ("Валюта договора", "Из реестра графа 'Валюта договора'")
    ]
    if request.method == 'GET':
        for field in RKDZ_ADD:
            if field[2] in request.GET.keys():
                RKDZ_TEMPLATE.append(field)
    response = {
        "RKDZ": RKDZ_TEMPLATE,
        "len": range(1, (len(RKDZ_TEMPLATE) + 2)),
    }
    return render(request, './analytics/RKDZ_template.html', response)

