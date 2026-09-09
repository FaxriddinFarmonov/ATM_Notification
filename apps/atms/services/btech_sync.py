import logging
from django.utils import timezone
from django.db import transaction
from apps.atms.models import BTechConfig, BTechATMSnapshot, ATM, ATMCurrentState
from apps.atms.services.monitoring_client import MonitoringClient

logger = logging.getLogger(__name__)


class BTechSyncService:

    @classmethod
    def sync_all(cls):
        """
        Fetches ATM data from BTech API and updates BTechATMSnapshot,
        ATM, and ATMCurrentState in DB.
        Returns dictionary with sync statistics.
        """
        config = BTechConfig.objects.filter(is_active=True).first()
        if not config:
            config = BTechConfig.objects.create()

        try:
            client = MonitoringClient()
            data = client.get_atms()

            if not isinstance(data, list):
                raise ValueError(f"Expected list response from BTech API, got {type(data)}")

            synced_count = 0
            with transaction.atomic():
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    btech_id = item.get("id")
                    if not btech_id:
                        continue

                    card = item.get("card") or {}
                    extra = card.get("extraAttrs") or {}
                    state = item.get("state") or {}
                    agent = item.get("agentStatus") or {}
                    cdm_cash = item.get("cdmRemainingAmount") or {}
                    model = item.get("model") or {}
                    vendor = model.get("vendor") or {}

                    serial = item.get("serial") or f"UNKNOWN_{btech_id}"
                    tid = extra.get("terminalId") or item.get("tid") or ""

                    # Calculate cash amounts
                    total_cash_uzs = 0
                    try:
                        total_cash_uzs = int(cdm_cash.get("totalUzs") or 0)
                    except (ValueError, TypeError):
                        pass

                    total_cash_usd = 0
                    try:
                        total_cash_usd = int(cdm_cash.get("totalUsd") or 0)
                    except (ValueError, TypeError):
                        pass

                    # 1. Update BTechATMSnapshot
                    BTechATMSnapshot.objects.update_or_create(
                        btech_id=btech_id,
                        defaults={
                            "serial": serial,
                            "tid": tid,
                            "status": item.get("status") or "production",
                            "service_status": state.get("serviceStatus") or "InService",
                            "app_conn_status": state.get("appConnStatus") or "Online",
                            "agent_status": agent.get("status") or "online",
                            "last_online": agent.get("lastOnline"),
                            "total_cash_uzs": total_cash_uzs,
                            "total_cash_usd": total_cash_usd,
                            "address": card.get("address") or "",
                            "model_name": model.get("name") or "",
                            "vendor_name": vendor.get("name") or "",
                            "branch_number": card.get("branchNumber") or "",
                            "raw_data": item,
                        }
                    )

                    # 2. Update ATM & ATMCurrentState models for core app compatibility
                    atm, _ = ATM.objects.update_or_create(
                        external_id=btech_id,
                        defaults={
                            "atm_uid": item.get("atmUid"),
                            "serial": serial,
                            "tid": tid,
                            "branch_number": card.get("branchNumber"),
                            "address": card.get("address"),
                            "model_name": model.get("name"),
                            "extra_attrs": extra,
                        }
                    )

                    ATMCurrentState.objects.update_or_create(
                        atm=atm,
                        defaults={
                            "agent_status": agent.get("status") or "UNKNOWN",
                            "service_status": state.get("serviceStatus") or "UNKNOWN",
                            "app_status": state.get("appStatus") or "UNKNOWN",
                            "app_conn_status": state.get("appConnStatus") or "UNKNOWN",
                            "cash_amount": total_cash_uzs,
                            "last_online": agent.get("lastOnline"),
                        }
                    )

                    synced_count += 1

            config.last_synced_at = timezone.now()
            config.last_sync_status = f"SUCCESS: Synced {synced_count} ATMs at {config.last_synced_at.strftime('%Y-%m-%d %H:%M:%S')}"
            config.save(update_fields=["last_synced_at", "last_sync_status"])

            logger.info(f"BTech Sync completed successfully: {synced_count} ATMs updated.")
            return {"status": "success", "synced_count": synced_count}

        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            logger.error(f"BTech Sync failed: {error_msg}")
            config.last_sync_status = error_msg[:150]
            config.save(update_fields=["last_sync_status"])
            return {"status": "error", "message": error_msg}
