from .inlines import *
from .service_contract import *
from .service_payment import *
# Keyingi qismlarda qo'shiladi
from .atm_admin import *
# from .monthly_admin import *
# from .yearly_admin import *
# from .excel_import_admin import *
from .atm_texnik import *
from .excel_admin import *
from .atm_admin import *
from django.http import HttpResponse
from django.urls import path
from ..services.excel_exporter import ATMExcelExporter