from django.db.models import Q


class MaintenanceSearchService:

    @staticmethod
    def apply(queryset, search: str):

        if not search:
            return queryset

        search = search.strip()

        if not search:
            return queryset

        return queryset.filter(
            Q(technical__terminal_id__icontains=search)
            |
            Q(technical__serial_number__icontains=search)
            |
            Q(technical__atm__name__icontains=search)
            |
            Q(technical__atm__region__icontains=search)
            |
            Q(part_name__icontains=search)
            |
            Q(protocol__protocol_number__icontains=search)
            |
            Q(mfo_bank__icontains=search)
            |
            Q(filial_name__icontains=search)
        )