from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from apps.users.models import Engineer
from apps.atms.models import ATM, BTechConfig, BTechATMSnapshot
from apps.atms.services.btech_sync import BTechSyncService
from apps.users.serializers import (
    EngineerSerializer,
    EngineerDetailSerializer,
    CreateEngineerSerializer,
    AssignAtmSerializer,
)


class EngineerListCreateAPIView(APIView):
    def get(self, request):
        queryset = Engineer.objects.filter(is_active=True).prefetch_related("assigned_atms")

        # Filters
        search = request.query_params.get("search")
        region = request.query_params.get("region")

        if region and region.lower() != "all":
            queryset = queryset.filter(region__icontains=region)

        if search:
            search = search.strip()
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(telegram_username__icontains=search) |
                Q(phone__icontains=search) |
                Q(region__icontains=search) |
                Q(specialization__icontains=search)
            )

        serializer = EngineerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateEngineerSerializer(data=request.data)
        if serializer.is_valid():
            engineer = serializer.save()
            return Response(
                EngineerSerializer(engineer).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EngineerDetailAPIView(APIView):
    def get(self, request, pk):
        engineer = get_object_or_404(Engineer, pk=pk)
        serializer = EngineerDetailSerializer(engineer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        engineer = get_object_or_404(Engineer, pk=pk)
        serializer = CreateEngineerSerializer(engineer, data=request.data, partial=True)
        if serializer.is_valid():
            engineer = serializer.save()
            return Response(EngineerDetailSerializer(engineer).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        engineer = get_object_or_404(Engineer, pk=pk)
        engineer.is_active = False
        engineer.save()
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)


class AssignAtmAPIView(APIView):
    def post(self, request, pk):
        engineer = get_object_or_404(Engineer, pk=pk)
        serializer = AssignAtmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serial = serializer.validated_data["serial"]
        tid = serializer.validated_data.get("tid")

        # Find or create ATM
        atm = ATM.objects.filter(Q(serial=serial) | (Q(tid=tid) if tid else Q())).first()
        if not atm:
            atm = ATM.objects.create(
                external_id=hash(serial) % 1000000000,
                serial=serial,
                tid=tid or "",
                responsible_engineer=engineer
            )
        else:
            atm.responsible_engineer = engineer
            atm.save(update_fields=["responsible_engineer"])

        return Response({
            "status": "success",
            "message": f"ATM {serial} muhandis {engineer.full_name}ga biriktirildi."
        }, status=status.HTTP_200_OK)


class UnassignAtmAPIView(APIView):
    def post(self, request, pk):
        engineer = get_object_or_404(Engineer, pk=pk)
        serializer = AssignAtmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serial = serializer.validated_data["serial"]
        ATM.objects.filter(serial=serial, responsible_engineer=engineer).update(responsible_engineer=None)

        return Response({
            "status": "success",
            "message": f"ATM {serial} muhandis {engineer.full_name}dan ajratildi."
        }, status=status.HTTP_200_OK)


class AvailableATMsAPIView(APIView):
    def get(self, request):
        search = request.query_params.get("search", "").strip()
        queryset = ATM.objects.select_related("responsible_engineer", "atmcurrentstate").all()

        if search:
            queryset = queryset.filter(
                Q(serial__icontains=search) |
                Q(tid__icontains=search) |
                Q(address__icontains=search) |
                Q(model_name__icontains=search) |
                Q(branch_number__icontains=search)
            )

        results = []
        for atm in queryset[:200]:
            eng = atm.responsible_engineer
            results.append({
                "id": atm.id,
                "serial": atm.serial,
                "tid": atm.tid,
                "model_name": atm.model_name or "ATM",
                "branch_number": atm.branch_number or "",
                "address": atm.address or "",
                "service_status": atm.atmcurrentstate.service_status if hasattr(atm, "atmcurrentstate") else "InService",
                "cash_amount": atm.atmcurrentstate.cash_amount if hasattr(atm, "atmcurrentstate") else 0,
                "responsible_engineer_id": eng.id if eng else None,
                "responsible_engineer_name": eng.full_name if eng else None,
            })
        return Response(results, status=status.HTTP_200_OK)


class AtmEngineerAPIView(APIView):
    def get(self, request, serial):
        atm = ATM.objects.filter(serial=serial).first()
        if not atm or not atm.responsible_engineer:
            return Response({"engineer": None}, status=status.HTTP_200_OK)
        return Response(EngineerSerializer(atm.responsible_engineer).data, status=status.HTTP_200_OK)


class BTechTokenAPIView(APIView):
    def get(self, request):
        config = BTechConfig.objects.filter(is_active=True).first()
        if not config:
            config = BTechConfig.objects.create()
        return Response({
            "token": config.bearer_token,
            "api_url": config.api_url,
            "last_synced_at": config.last_synced_at,
            "last_sync_status": config.last_sync_status
        }, status=status.HTTP_200_OK)


class BTechSyncAPIView(APIView):
    def post(self, request):
        result = BTechSyncService.sync_all()
        return Response(result, status=status.HTTP_200_OK)
