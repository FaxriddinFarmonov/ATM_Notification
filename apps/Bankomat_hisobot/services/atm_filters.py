class ATMFilterService:

    @staticmethod
    def apply(queryset, filters):

        status = filters.get("status")
        region = filters.get("region")
        card_type = filters.get("card_type")
        model = filters.get("model")
        is_active = filters.get(
            "is_active",
            None,
        )

        if status:
            queryset = queryset.filter(
                technical__status=status
            )

        if region:
            queryset = queryset.filter(
                region=region
            )

        if card_type:
            queryset = queryset.filter(
                technical__card_type=card_type
            )

        if model:
            queryset = queryset.filter(
                technical__model_name=model
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active
            )

        return queryset