from apps.Bankomat_hisobot.models import ATMTechnical

from apps.maintenance.models import MaintenanceItem


def link_maintenance_items():

    technicals = {
        x.serial_number: x
        for x in ATMTechnical.objects.exclude(
            serial_number=""
        )
    }

    updates = []

    for item in MaintenanceItem.objects.filter(
        technical__isnull=True
    ):

        tech = technicals.get(item.serial_number)

        if tech:
            item.technical = tech
            updates.append(item)

    MaintenanceItem.objects.bulk_update(
        updates,
        ["technical"],
        batch_size=1000,
    )

    return len(updates)