from django.db.models import Q


class MaintenanceFilterService:

    @staticmethod
    def apply(queryset, filters):

        region = filters.get("region")
        terminal_id = filters.get("terminal_id")
        serial_number = filters.get("serial_number")
        part_name = filters.get("part_name")
        mfo_bank = filters.get("mfo_bank")
        protocol_number = filters.get("protocol_number")

        date_from = filters.get("date_from")
        date_to = filters.get("date_to")

        if region:
            queryset = queryset.filter(
                technical__atm__region__iexact=region
            )

        if terminal_id:
            queryset = queryset.filter(
                technical__terminal_id__icontains=terminal_id
            )

        if serial_number:
            queryset = queryset.filter(
                technical__serial_number__icontains=serial_number
            )

        if part_name:
            queryset = queryset.filter(
                part_name__icontains=part_name
            )

        if mfo_bank:
            queryset = queryset.filter(
                mfo_bank__icontains=mfo_bank
            )

        if protocol_number:
            queryset = queryset.filter(
                protocol__protocol_number__icontains=protocol_number
            )

        if date_from:
            queryset = queryset.filter(
                protocol_date__gte=date_from
            )

        if date_to:
            queryset = queryset.filter(
                protocol_date__lte=date_to
            )

        return queryset