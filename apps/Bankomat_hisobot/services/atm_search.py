from django.db.models import Q


class ATMSearchService:

    @staticmethod
    def apply(queryset, search: str):

        if not search:
            return queryset

        search = search.strip()

        return queryset.filter(

            Q(name__icontains=search)

            | Q(region__icontains=search)

            | Q(technical__terminal_id__icontains=search)

            | Q(technical__merchant_id__icontains=search)

            | Q(technical__serial_number__icontains=search)

            | Q(technical__address__icontains=search)

            | Q(technical__model_name__icontains=search)

        )