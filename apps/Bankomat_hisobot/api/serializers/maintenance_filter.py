from rest_framework import serializers


class MaintenanceFilterSerializer(
    serializers.Serializer
):

    search = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=100,
    )

    region = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=100,
    )

    terminal_id = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=100,
    )

    serial_number = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=100,
    )

    part_name = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=255,
    )

    mfo_bank = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=20,
    )

    protocol_number = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=100,
    )

    date_from = serializers.DateField(
        required=False,
    )

    date_to = serializers.DateField(
        required=False,
    )

    def validate(self, attrs):

        date_from = attrs.get("date_from")
        date_to = attrs.get("date_to")

        if (
            date_from
            and date_to
            and date_from > date_to
        ):
            raise serializers.ValidationError(
                {
                    "date_to": (
                        "date_to date_from dan "
                        "kichik bo'lishi mumkin emas."
                    )
                }
            )

        return attrs