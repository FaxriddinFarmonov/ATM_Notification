class ATMRules:

    @staticmethod
    def is_offline(old, new):
        return old != "OFFLINE" and new == "OFFLINE"

    @staticmethod
    def is_online(old, new):
        return old == "OFFLINE" and new == "ONLINE"

    @staticmethod
    def is_cash_low(amount):
        return amount < 500000  # misol threshold

    @staticmethod
    def is_no_transaction(last_tx_hours):
        return last_tx_hours >= 12