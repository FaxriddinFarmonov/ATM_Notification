# matcher.py

from apps.atms.models import ATM

class ATMSmartMatcher:

    def find(self, data: dict):

        serial = data.get("serial")
        tid = data.get("tid")
        terminal_id = data.get("terminal_id")
        merchant_id = data.get("merchant_id")

        if serial:
            atm = ATM.objects.filter(serial=serial).first()
            if atm:
                return atm

        if tid:
            atm = ATM.objects.filter(tid=tid).first()
            if atm:
                return atm

        if terminal_id:
            atm = ATM.objects.filter(
                extra_attrs__terminalId=terminal_id
            ).first()
            if atm:
                return atm

        if merchant_id:
            atm = ATM.objects.filter(
                extra_attrs__merchantId=merchant_id
            ).first()
            if atm:
                return atm

        return None