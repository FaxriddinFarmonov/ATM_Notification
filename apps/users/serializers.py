from rest_framework import serializers
from apps.users.models import Engineer
from apps.atms.models import ATM, BTechATMSnapshot, ATMCurrentState


class EngineerSerializer(serializers.ModelSerializer):
    assigned_atms_count = serializers.SerializerMethodField()
    in_service_count = serializers.SerializerMethodField()
    out_of_service_count = serializers.SerializerMethodField()
    total_cash = serializers.SerializerMethodField()
    atms_preview = serializers.SerializerMethodField()

    class Meta:
        model = Engineer
        fields = [
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "full_name",
            "telegram_username",
            "telegram_chat_id",
            "phone",
            "region",
            "specialization",
            "avatar_url",
            "is_active",
            "assigned_atms_count",
            "in_service_count",
            "out_of_service_count",
            "total_cash",
            "atms_preview",
            "created_at",
            "updated_at",
        ]

    def get_assigned_atms_count(self, obj):
        return obj.assigned_atms.count()

    def _get_atms_snapshots(self, obj):
        if not hasattr(obj, "_cached_snapshots"):
            atms = obj.assigned_atms.all()
            serials = [a.serial for a in atms if a.serial]
            tids = [a.tid for a in atms if a.tid]
            
            snapshots = BTechATMSnapshot.objects.filter(
                serial__in=serials
            ) | BTechATMSnapshot.objects.filter(
                tid__in=tids
            )
            
            snap_map = {}
            for s in snapshots:
                if s.serial:
                    snap_map[s.serial] = s
                if s.tid:
                    snap_map[s.tid] = s
            obj._cached_snapshots = (atms, snap_map)
        return obj._cached_snapshots

    def get_in_service_count(self, obj):
        atms, snap_map = self._get_atms_snapshots(obj)
        count = 0
        for atm in atms:
            snap = snap_map.get(atm.serial) or snap_map.get(atm.tid)
            if snap and snap.service_status.lower() in ["inservice", "soz"]:
                count += 1
            elif not snap and hasattr(atm, "atmcurrentstate"):
                if atm.atmcurrentstate.service_status.lower() in ["inservice", "soz"]:
                    count += 1
        return count

    def get_out_of_service_count(self, obj):
        total = obj.assigned_atms.count()
        in_service = self.get_in_service_count(obj)
        return max(0, total - in_service)

    def get_total_cash(self, obj):
        atms, snap_map = self._get_atms_snapshots(obj)
        total = 0
        for atm in atms:
            snap = snap_map.get(atm.serial) or snap_map.get(atm.tid)
            if snap:
                total += snap.total_cash_uzs
            elif hasattr(atm, "atmcurrentstate"):
                total += atm.atmcurrentstate.cash_amount or 0
        return total

    def get_atms_preview(self, obj):
        atms, snap_map = self._get_atms_snapshots(obj)
        preview = []
        for atm in atms[:5]:
            snap = snap_map.get(atm.serial) or snap_map.get(atm.tid)
            preview.append({
                "serial": atm.serial,
                "tid": atm.tid or (snap.tid if snap else ""),
                "model_name": atm.model_name or (snap.model_name if snap else "ATM"),
                "service_status": snap.service_status if snap else (atm.atmcurrentstate.service_status if hasattr(atm, "atmcurrentstate") else "InService"),
                "cash_amount": snap.total_cash_uzs if snap else (atm.atmcurrentstate.cash_amount if hasattr(atm, "atmcurrentstate") else 0),
            })
        return preview


class AssignedATMSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    serial = serializers.CharField()
    tid = serializers.CharField(allow_blank=True, default="")
    model_name = serializers.CharField(allow_blank=True, default="")
    vendor = serializers.CharField(allow_blank=True, default="")
    branch_number = serializers.CharField(allow_blank=True, default="")
    address = serializers.CharField(allow_blank=True, default="")
    service_status = serializers.CharField(default="InService")
    agent_status = serializers.CharField(default="online")
    cash_amount = serializers.IntegerField(default=0)
    last_online = serializers.DateTimeField(allow_null=True, required=False)
    latitude = serializers.FloatField(allow_null=True, required=False)
    longitude = serializers.FloatField(allow_null=True, required=False)
    hw_faults = serializers.ListField(required=False, default=list)
    cdmCassetteStatusBrief = serializers.ListField(required=False, default=list)
    raw_btech_data = serializers.DictField(required=False, default=dict)


class EngineerDetailSerializer(EngineerSerializer):
    atms = serializers.SerializerMethodField()

    class Meta(EngineerSerializer.Meta):
        fields = EngineerSerializer.Meta.fields + ["atms"]

    def get_atms(self, obj):
        atms, snap_map = self._get_atms_snapshots(obj)
        result = []
        for atm in atms:
            snap = snap_map.get(atm.serial) or snap_map.get(atm.tid)
            raw = snap.raw_data if snap else {}
            card = raw.get("card", {})
            gps = card.get("gpsCoords", {})

            lat = None
            lng = None
            try:
                if gps.get("latitude"):
                    lat = float(gps.get("latitude"))
                if gps.get("longitude"):
                    lng = float(gps.get("longitude"))
            except (ValueError, TypeError):
                pass

            result.append({
                "id": atm.id,
                "serial": atm.serial,
                "tid": atm.tid or (snap.tid if snap else ""),
                "model_name": atm.model_name or (snap.model_name if snap else "ATM"),
                "vendor": snap.vendor_name if snap else "",
                "branch_number": atm.branch_number or (snap.branch_number if snap else ""),
                "address": atm.address or (snap.address if snap else ""),
                "service_status": snap.service_status if snap else (atm.atmcurrentstate.service_status if hasattr(atm, "atmcurrentstate") else "InService"),
                "agent_status": snap.agent_status if snap else (atm.atmcurrentstate.agent_status if hasattr(atm, "atmcurrentstate") else "online"),
                "cash_amount": snap.total_cash_uzs if snap else (atm.atmcurrentstate.cash_amount if hasattr(atm, "atmcurrentstate") else 0),
                "last_online": snap.last_online if snap else (atm.atmcurrentstate.last_online if hasattr(atm, "atmcurrentstate") else None),
                "latitude": lat,
                "longitude": lng,
                "hw_faults": raw.get("deviceStatus") or [],
                "cdmCassetteStatusBrief": raw.get("cdmCassetteStatusBrief") or [],
                "raw_btech_data": raw,
            })
        return result


class CreateEngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "telegram_username",
            "phone",
            "region",
            "specialization",
        ]


class AssignAtmSerializer(serializers.Serializer):
    serial = serializers.CharField(required=True)
    tid = serializers.CharField(required=False, allow_blank=True)
