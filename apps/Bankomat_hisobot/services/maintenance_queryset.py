from apps.maintenance.models import MaintenanceItem


class MaintenanceQuerySet:

    @staticmethod
    def list():

        return (
            MaintenanceItem.objects

            .select_related(
                "technical",
                "technical__atm",
                "protocol",
                "document",
            )

            .only(
                "id",
                "row_number",
                "protocol_date",
                "equipment_module",
                "serial_number",
                "filial_name",
                "mfo_bank",
                "part_name",
                "measurement_unit",
                "quantity",
                "price_per_unit",
                "total_amount",
                "vat_rate",
                "vat_amount",
                "total_with_vat",

                "technical__terminal_id",
                "technical__serial_number",
                "technical__model_name",
                "technical__card_type",
                "technical__status",

                "technical__atm__id",
                "technical__atm__name",
                "technical__atm__region",
                "technical__atm__address",

                "protocol__protocol_number",
                "protocol__protocol_date",

                "document__id",
                "document__title",
            )

            .order_by(
                "-protocol_date",
                "-id",
            )
        )