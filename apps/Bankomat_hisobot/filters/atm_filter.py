import django_filters

from ..models import ATMTURON


class ATMFilter(
    django_filters.FilterSet
):

    region = django_filters.CharFilter(
        lookup_expr="iexact",
    )

    card_type = django_filters.CharFilter(
        lookup_expr="iexact",
    )

    model = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    terminal_id = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    is_active = django_filters.BooleanFilter()

    class Meta:

        model = ATMTURON

        fields = (
            "region",
            "card_type",
            "model",
            "terminal_id",
            "is_active",
        )