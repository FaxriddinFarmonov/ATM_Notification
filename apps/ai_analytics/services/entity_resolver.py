from __future__ import annotations

from typing import Any

from django.db.models import Q

from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import (
    ATMTURON,
)


class ATMEntityResolver:

    @staticmethod
    def _normalize(value: Any) -> str | None:
        """
        User yoki AI tomonidan kelgan qiymatni
        qidiruv uchun normalizatsiya qiladi.
        """

        if value is None:
            return None

        value = str(value).strip()

        if not value:
            return None

        return value

    @staticmethod
    def _serialize_atm(atm: ATMTURON) -> dict:

        technical = getattr(
            atm,
            "technical",
            None,
        )

        return {
            "id": atm.id,

            "name": atm.name,

            "region": atm.region,

            "is_active": atm.is_active,

            "terminal_id": (
                technical.terminal_id
                if technical
                else atm.terminal_id
            ),

            "merchant_id": (
                technical.merchant_id
                if technical
                else None
            ),

            "serial_number": (
                technical.serial_number
                if technical
                else None
            ),

            "model": (
                technical.model_name
                if technical
                else atm.model
            ),

            "status": (
                technical.status
                if technical
                else None
            ),

            "card_type": (
                technical.card_type
                if technical
                else atm.card_type
            ),
        }

    @classmethod
    def resolve(
            cls,

            *,

            atm_id: int | str | None = None,

            serial_number: str | None = None,

            terminal_id: str | None = None,

            merchant_id: str | None = None,

            region: str | None = None,

            model: str | None = None,

            name: str | None = None,

            status: str | None = None,

            card_type: str | None = None,

            is_active: bool | None = None,

    ) -> dict:

        """
        Universal multi-entity ATM resolver.

        Barcha berilgan parametrlar AND
        shart bilan ishlaydi.

        Example:

        region="МАБ"
        model="NCR6622"
        status="NOSOZ"
        card_type="UZCARD"

        Bu parametrlarning barchasi birgalikda
        filter qilinadi.
        """

        # ---------------------------------
        # 1. NORMALIZATION
        # ---------------------------------

        atm_id = cls._normalize(atm_id)

        serial_number = cls._normalize(
            serial_number
        )

        terminal_id = cls._normalize(
            terminal_id
        )

        merchant_id = cls._normalize(
            merchant_id
        )

        region = cls._normalize(
            region
        )

        model = cls._normalize(
            model
        )

        name = cls._normalize(
            name
        )

        status = cls._normalize(
            status
        )

        card_type = cls._normalize(
            card_type
        )

        # ---------------------------------
        # 2. BASE QUERYSET
        # ---------------------------------

        queryset = (
            ATMTURON.objects
            .select_related("technical")
        )

        # ---------------------------------
        # 3. ATM ID
        # ---------------------------------

        if atm_id:

            try:

                queryset = queryset.filter(
                    id=int(atm_id)
                )

            except ValueError:

                return cls._empty_result(
                    reason="invalid_atm_id"
                )

        # ---------------------------------
        # 4. SERIAL NUMBER
        # ---------------------------------

        if serial_number:
            queryset = queryset.filter(
                technical__serial_number__iexact=(
                    serial_number
                )
            )

        # ---------------------------------
        # 5. TERMINAL ID
        # ---------------------------------

        if terminal_id:
            queryset = queryset.filter(

                Q(
                    terminal_id__iexact=(
                        terminal_id
                    )
                )

                |

                Q(
                    technical__terminal_id__iexact=(
                        terminal_id
                    )
                )

            )

        # ---------------------------------
        # 6. MERCHANT ID
        # ---------------------------------

        if merchant_id:
            queryset = queryset.filter(
                technical__merchant_id__iexact=(
                    merchant_id
                )
            )

        # ---------------------------------
        # 7. REGION
        # ---------------------------------

        if region:
            queryset = queryset.filter(
                region__icontains=region
            )

        # ---------------------------------
        # 8. MODEL
        # ---------------------------------

        if model:
            queryset = queryset.filter(

                Q(
                    model__icontains=model
                )

                |

                Q(
                    technical__model_name__icontains=(
                        model
                    )
                )

            )

        # ---------------------------------
        # 9. ATM NAME
        # ---------------------------------

        if name:
            queryset = queryset.filter(
                name__icontains=name
            )

        # ---------------------------------
        # 10. STATUS
        # ---------------------------------

        if status:
            queryset = queryset.filter(
                technical__status__iexact=status
            )

        # ---------------------------------
        # 11. CARD TYPE
        # ---------------------------------

        if card_type:
            queryset = queryset.filter(

                Q(
                    card_type__iexact=card_type
                )

                |

                Q(
                    technical__card_type__iexact=(
                        card_type
                    )
                )

            )

        # ---------------------------------
        # 12. ACTIVE STATUS
        # ---------------------------------

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active
            )

        # ---------------------------------
        # 13. SERIALIZE
        # ---------------------------------

        items = [

            cls._serialize_atm(atm)

            for atm in queryset
        ]

        return {

            "found": bool(items),

            "count": len(items),

            "filters": {

                "atm_id": atm_id,

                "serial_number": serial_number,

                "terminal_id": terminal_id,

                "merchant_id": merchant_id,

                "region": region,

                "model": model,

                "name": name,

                "status": status,

                "card_type": card_type,

                "is_active": is_active,

            },

            "items": items,

        }
    @staticmethod
    def _detect_match_type(

        *,

        serial_number=None,

        terminal_id=None,

        merchant_id=None,

        region=None,

        model=None,

        name=None,

    ) -> str:

        if serial_number:

            return "serial_number"

        if terminal_id:

            return "terminal_id"

        if merchant_id:

            return "merchant_id"

        if region:

            return "region"

        if model:

            return "model"

        if name:

            return "name"

        return "unknown"

    @staticmethod
    def _empty_result(
            reason: str | None = None,
    ) -> dict:

        return {

            "found": False,

            "count": 0,

            "filters": {},

            "items": [],

            "reason": reason,

        }