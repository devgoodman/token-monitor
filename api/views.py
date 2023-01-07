from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

import pandas as pd


class TxnView(APIView):

    def get(self, request):
        # разбираем запрос, если нет парамтеров фильтра, то ставим ноль
        method_filter = request.GET.get("filter", 0)
        data = cache.get('txnx')
        # если есть фильтрация, то получаем данные из кэша согласно фильтру
        if method_filter != '0':

            temp_list = []
            for item in data:
                method = item.get('Method', 0)
                if method == method_filter:
                    temp_list.append(item)
                    data = temp_list
        # обрабатываем данные для правильной работы
        data = pd.DataFrame(data).rename_axis(
            'id').reset_index().to_dict('records')

        return Response(data)
