# 🏦 ATM Monitoring & Business Analytics API — To'liq Frontend Hujjati

Ushbu hujjat **Turon Bank ATM Monitoring va Biznes Analitika tizimi** frontend dasturchilari (React / Vue / Next.js / Angular) uchun to'liq texnik qo'llanma hisoblanadi. Unda tizimdagi **barcha (eski va eng yangi Senior analitika hamda AI)** APIning batafsil tavsifi, parametrlar, so'rov va javob namunalari, TypeScript interfeyslari hamda frontend integratsiya bo'yicha tavsiyalar keltirilgan.

---

## 📌 1. Umumiy Ma'lumotlar va Konfiguratsiya

### 1.1. Base URL
- **Lokal muhit (Localhost):** `http://localhost:8000`
- **Server / Staging:** `https://atm-info.turonbank.uz` (yoki berilgan test domeni)

### 1.2. Standart Headers (Sarlavhalar)
Frontenddan yuboriladigan barcha so'rovlar uchun quyidagi sarlavhalar tavsiya etiladi:
```http
Content-Type: application/json
Accept: application/json
```
> **Eslatma:** Agar backend `ngrok` orqali test qilinayotgan bo'lsa, ngrok ogohlantirish oynasini aylanib o'tish uchun quyidagi header qo'shilishi kerak:
> `ngrok-skip-browser-warning: true`

### 1.3. Autentifikatsiya (Auth)
- Hozirgi barcha `api/v1/` va `api/v2/` endpointlar ochiq (`AllowAny`) rejimda ishlaydi.
- Maxsus Bearer Token yoki Login sarlavhalari talab qilinmaydi.

### 1.4. Interaktiv Swagger va Postman fayllari
- **Swagger UI (Brauzerda test qilish):** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **OpenAPI Schema (JSON):** `schema.json` (Loyiha ildizida joylashgan, to'g'ridan-to'g'ri Postman yoki Insomniaga import qilish mumkin)
- **OpenAPI Schema (YAML):** `schema.yaml`
- **Jonli Schema Endpoint:** `http://localhost:8000/api/schema/`

### 1.5. Pagination (Sahifalash) formati
Ro'yxat qaytaruvchi APIlar (`/api/v1/atms/`, `/api/v1/maintenance/`) standart pagination formatiga ega:
```json
{
  "count": 482,
  "next": "http://localhost:8000/api/v1/atms/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## 📑 2. API Mundarijasi (Tezkor o'tish)

| № | Bo'lim | Endpoint | Method | Tavsifi |
|---|--------|----------|--------|---------|
| **1** | **Dashboard** | `/api/v1/dashboard/` | `GET` | Asosiy boshqaruv paneli ko'rsatkichlari va grafiklari |
| **2** | **Bankomatlar (ATM)** | `/api/v1/atms/filters/` | `GET` | Frontend filter dropdownlari uchun dinamik parametrlar |
| **3** | **Bankomatlar (ATM)** | `/api/v1/atms/` | `GET` | Bankomatlar ro'yxati (qidiruv, filtrlar, sahifalash) |
| **4** | **Bankomatlar (ATM)** | `/api/v1/atms/{id}/` | `GET` | Bitta bankomatning to'liq tafsilotlari va statistikasi |
| **5** | **Eksport (Excel)** | `/api/v1/atms/export/` | `GET` | Barcha/filtrlangan bankomatlar ro'yxatini Excel yuklab olish |
| **6** | **Eksport (Excel)** | `/api/v1/atms/{id}/export/` | `GET` | Bitta bankomatning to'liq Excel hisoboti |
| **7** | **Ta'mirlash** | `/api/v1/maintenance/` | `GET` | Ta'mirlash va ehtiyot qismlar aktlari ro'yxati |
| **8** | **Ta'mirlash** | `/api/v1/maintenance/{id}/` | `GET` | Bitta ta'mirlash aktining to'liq ma'lumoti |
| **9** | **Senior Analitika (Yangi)** | `/api/v1/analytics/regions/` | `GET` | Viloyatlar moliyaviy reytingi va chuqur tahlili |
| **10** | **Senior Analitika (Yangi)** | `/api/v1/analytics/atms/top-income/` | `GET` | Eng daromadli bankomatlar reytingi (Top Revenue) |
| **11** | **Senior Analitika (Yangi)** | `/api/v1/analytics/atms/top-expense/` | `GET` | Eng xarajatli bankomatlar (zapchast, ijara, elektr, servis) |
| **12** | **Senior Analitika (Yangi)** | `/api/v1/analytics/atms/loss-making/` | `GET` | Zarardagi bankomatlar va relokatsiya tavsiyalari |
| **13** | **Senior Analitika (Yangi)** | `/api/v1/analytics/overview/` | `GET` | Rahbariyat uchun umumiy moliyaviy KPI xulosasi |
| **14** | **AI Analitika (Yangi)** | `/api/v1/atms/{id}/ai-analysis/` | `POST` | Bitta bankomat bo'yicha Ollama LLM xulosasi |
| **15** | **AI Analitika (Yangi)** | `/api/v1/regions/ai-analysis/` | `POST` | Viloyat va davr bo'yicha Ollama LLM xulosasi |
| **16** | **AI Analitika v2** | `/api/v2/regions/ai-analysis/` | `POST` | Viloyat AI tahlili (v2 endpoint) |

---

## 📊 3. Boshqaruv Paneli (Dashboard)

### `GET /api/v1/dashboard/`
Asosiy bosh sahifani chizish uchun barcha umumiy statistika va grafiklar ma'lumotlarini bitta so'rovda qaytaradi.

- **Query parametrlar:** Yo'q.
- **Qachon chaqiriladi:** Dashboard sahifasi ochilganda 1 marta.

#### Javob namunasi (Response):
```json
{
  "summary": {
    "total_atms": 482,
    "active_atms": 460,
    "inactive_atms": 22,
    "operational_atms": 435,
    "non_operational_atms": 47,
    "total_income": "12543000000.00",
    "total_expense": "3210000000.00",
    "net_profit": "9333000000.00",
    "profit_margin": 74.41,
    "maintenance_records_count": 1420,
    "total_maintenance_expense": "845000000.00"
  },
  "top_regions": [
    {
      "region": "Тошкент ш.",
      "total_atms": 120,
      "operational_atms": 115,
      "non_operational_atms": 5,
      "total_income": "4500000000.00",
      "total_expense": "950000000.00",
      "net_profit": "3550000000.00"
    }
  ],
  "status_chart": {
    "operational": 435,
    "non_operational": 47
  },
  "card_type_chart": {
    "UZCARD": 280,
    "HUMO": 202
  },
  "monthly_financials": [
    {
      "year": 2025,
      "month": 1,
      "month_name": "Yanvar",
      "income": "980000000.00",
      "expense": "250000000.00",
      "net_profit": "730000000.00"
    }
  ],
  "models_distribution": [
    {
      "model": "GRG H68N",
      "count": 180
    },
    {
      "model": "Nautilus Hyosung",
      "count": 140
    }
  ],
  "recent_maintenances": [
    {
      "id": 154,
      "protocol_number": "12-V",
      "protocol_date": "2025-02-15",
      "terminal_id": "T001245",
      "part_name": "Kassetani ta'mirlash",
      "total_with_vat": "1450000.00"
    }
  ]
}
```

---

## 🏧 4. Bankomatlar (ATM) Bo'limi

### 4.1. Filtr variantlarini olish
### `GET /api/v1/atms/filters/`
Frontenddagi select / dropdown elementlarini to'ldirish uchun mavjud qiymatlarni qaytaradi.

- **Query parametrlar:** Yo'q.
- **Frontend tavsiyasi:** Sayt yuklanganda yoki Bankomatlar sahifasiga kirilganda 1 marta chaqirib, Redux / Pinia / Context / State-ga saqlab qo'yish tavsiya qilinadi.

#### Javob namunasi (Response):
```json
{
  "status": [
    { "value": "SOZ", "label": "SOZ" },
    { "value": "NOSOZ", "label": "NOSOZ" }
  ],
  "card_type": [
    { "value": "UZCARD", "label": "UZCARD" },
    { "value": "HUMO", "label": "HUMO" }
  ],
  "regions": [
    "Андижон", "Бухоро", "Фарғона", "Жиззах", "Хоразм", 
    "Наманган", "Навоий", "Қашқадарё", "Қорақалпоғистон", 
    "Самарқанд", "Сирдарё", "Сурхондарё", "Тошкент в.", "Тошкент ш.", "МАБ"
  ],
  "models": ["GRG", "Nautilus", "NCR", "Diebold"],
  "years": [2024, 2025, 2026],
  "months": [
    { "value": 1, "label": "Yanvar" },
    { "value": 2, "label": "Fevral" },
    { "value": 12, "label": "Dekabr" }
  ],
  "is_active": [
    { "value": true, "label": "Faol" },
    { "value": false, "label": "Nofaol" }
  ]
}
```

---

### 4.2. Bankomatlar ro'yxati (Search & Filters & Pagination)
### `GET /api/v1/atms/`
Bankomatlarning qidiruv, ko'p parametrli filtrlash va sahifalangan ro'yxati.

- **Query parametrlar:**
  | Parametr | Turi | Majburiyligi | Tavsifi / Ruxsat etilgan qiymatlar |
  |----------|------|--------------|-----------------------------------|
  | `page` | `integer` | Ixtiyoriy | Sahifa raqami (default: 1) |
  | `page_size` | `integer` | Ixtiyoriy | Har sahifadagi elementlar soni |
  | `search` | `string` | Ixtiyoriy | ATM nomi, TID, MID, Seriya raqami, Manzil, Model bo'yicha qidiruv |
  | `status` | `string` | Ixtiyoriy | `SOZ`, `NOSOZ` |
  | `region` | `string` | Ixtiyoriy | Viloyat nomi (masalan: `Самарқанд`, `Тошкент ш.`) |
  | `card_type`| `string` | Ixtiyoriy | `UZCARD`, `HUMO` |
  | `model` | `string` | Ixtiyoriy | Model nomi |
  | `is_active`| `boolean`| Ixtiyoriy | `true` yoki `false` |

#### Misol so'rov:
`GET /api/v1/atms/?search=Tashkent&status=SOZ&card_type=UZCARD&page=1`

#### Javob namunasi (Response):
```json
{
  "count": 28,
  "next": "http://localhost:8000/api/v1/atms/?page=2",
  "previous": null,
  "results": [
    {
      "id": 12,
      "terminal_id": "T001452",
      "merchant_id": "M889412",
      "name": "Bosh ofis vestibyul",
      "region": "Тошкент ш.",
      "address": "Navoiy ko'chasi, 16-uy",
      "card_type": "UZCARD",
      "status": "SOZ",
      "model": "GRG H68N",
      "serial_number": "SN4481920",
      "is_active": true,
      "current_month_income": "45200000.00",
      "current_month_expense": "8500000.00",
      "current_month_profit": "36700000.00"
    }
  ]
}
```

---

### 4.3. Bitta bankomat to'liq kartochkasi (Detail)
### `GET /api/v1/atms/{id}/`
Tanlangan bankomatning biznes, texnik, oylik statistika va ta'mirlash tarixi ma'lumotlari.

- **URL parametr:** `id` (Bankomatning birlamchi kaliti yoki Terminal ID)
- **Misol:** `GET /api/v1/atms/T001452/` yoki `GET /api/v1/atms/12/`

#### Javob namunasi (Response):
```json
{
  "id": 12,
  "business": {
    "terminal_id": "T001452",
    "merchant_id": "M889412",
    "name": "Bosh ofis vestibyul",
    "region": "Тошкент ш.",
    "district": "Shayxontohur",
    "address": "Navoiy ko'chasi, 16-uy",
    "status": "SOZ",
    "card_type": "UZCARD",
    "installed_date": "2022-05-10",
    "is_active": true
  },
  "technical": {
    "model": "GRG H68N",
    "serial_number": "SN4481920",
    "inventory_number": "INV-2022-991",
    "cassettes_count": 4,
    "ip_address": "10.20.15.42",
    "software_version": "v4.2.1"
  },
  "monthly_statistics": [
    {
      "year": 2025,
      "month": 1,
      "cash_withdrawal_amount": "980000000.00",
      "transactions_count": 1450,
      "income": "9800000.00",
      "rent_expense": "1500000.00",
      "electricity_expense": "350000.00",
      "collection_expense": "600000.00",
      "maintenance_expense": "450000.00",
      "total_expense": "2900000.00",
      "net_profit": "6900000.00"
    }
  ],
  "maintenance_history": [
    {
      "id": 84,
      "protocol_number": "54-V",
      "protocol_date": "2025-01-20",
      "part_name": "Dispenser valiklarini almashtirish",
      "quantity": 2,
      "price_per_unit": "250000.00",
      "total_with_vat": "560000.00"
    }
  ]
}
```

---

## 📥 5. Excel Eksport (Fayllarni yuklab olish)

### 5.1. Barcha/filtrlangan bankomatlar hisoboti
### `GET /api/v1/atms/export/`
Bankomatlar ro'yxatini filtrlangan holda to'liq `.xlsx` formatida yuklab beradi.

- **Query parametrlar:** `/api/v1/atms/` bilan bir xil filtrlar (`region`, `card_type`, `model`, `status`, `is_active`).
- **Response Type:** Binary (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`).

### 5.2. Bitta bankomat Excel hisoboti
### `GET /api/v1/atms/{id}/export/`
- **URL parametr:** `id` (Bankomat ID yoki Terminal ID).
- **Response Type:** Binary `.xlsx` fayl.

#### 💡 Frontend Dasturchiga Kod Namunasi (Axios orqali yuklab olish):
```typescript
import axios from 'axios';

export const downloadATMExcel = async (terminalId?: string) => {
  const url = terminalId 
    ? `/api/v1/atms/${terminalId}/export/` 
    : `/api/v1/atms/export/`;

  const response = await axios.get(url, {
    responseType: 'blob', // MUHIM: fayl sifatida olish
  });

  const blob = new Blob([response.data], { 
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
  });
  const downloadUrl = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = downloadUrl;
  link.setAttribute('download', terminalId ? `ATM_${terminalId}.xlsx` : 'ATM_All_Report.xlsx');
  document.body.appendChild(link);
  link.click();
  link.remove();
};
```

---

## 🛠 6. Ta'mirlash va Ehtiyot Qismlar (Maintenance)

### 6.1. Ta'mirlash ro'yxati
### `GET /api/v1/maintenance/`
Protokollar bo'yicha bankomatlarga bajarilgan ishlar, sarflangan ehtiyot qismlar va xarajatlar ro'yxati.

- **Query parametrlar:**
  | Parametr | Turi | Tavsifi |
  |----------|------|---------|
  | `page` | `integer` | Sahifa raqami |
  | `search` | `string` | Ehtiyot qism, seriya raqami yoki filial bo'yicha qidiruv |
  | `region` | `string` | Viloyat |
  | `terminal_id` | `string` | TID (Terminal ID) |
  | `serial_number` | `string` | Seriya raqami |
  | `part_name` | `string` | Ehtiyot qism nomi |
  | `protocol_number` | `string` | Protokol/Akt raqami |
  | `date_from` | `date` (YYYY-MM-DD) | Boshlang'ich sana |
  | `date_to` | `date` (YYYY-MM-DD) | Tugash sanasi |

#### Javob namunasi (Response):
```json
{
  "count": 312,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 142,
      "protocol_number": "11-V",
      "protocol_date": "2025-02-10",
      "terminal_id": "T001452",
      "serial_number": "SN4481920",
      "filial_name": "Toshkent shahar filiali",
      "equipment_module": "Dispenser",
      "part_name": "Shkif tasmalar to'plami",
      "quantity": 1,
      "price_per_unit": "340000.00",
      "total_amount": "340000.00",
      "vat_amount": "40800.00",
      "total_with_vat": "380800.00"
    }
  ]
}
```

### 6.2. Bitta ta'mirlash yozuvi tafsiloti
### `GET /api/v1/maintenance/{id}/`
- **URL parametr:** `id`
- Tanlangan ehtiyot qism / ishning barcha rekvizitlari va protokol ma'lumotlarini qaytaradi.

---

## 💎 7. Senior Moliyaviy va Operatsion Analitika (YANGI!)

Ushbu bo'lim rahbarlar, moliyachilar va biznes tahlilchilar uchun maxsus ishlab chiqilgan ilg'or ko'rsatkichlarni taqdim etadi.

---

### 7.1. Top Viloyatlar Tahlili va Reytingi
### `GET /api/v1/analytics/regions/`
Har bir viloyat bo'yicha daromad, xarajatlar turlari, sof foyda, marja va bankomatlar holati.

- **Query parametrlar:**
  | Parametr | Turi | Majburiyligi | Default | Mumkin bo'lgan qiymatlar | Tavsifi |
  |----------|------|--------------|---------|---------------------------|---------|
  | `year` | `integer` | Ixtiyoriy | Oxirgi yil | `2024`, `2025`, `2026` | Tahlil yili |
  | `month` | `integer` | Ixtiyoriy | Hammasi | `1` - `12` | Tahlil oyi |
  | `sort_by` | `string` | Ixtiyoriy | `income` | `income`, `expense`, `profit`, `profit_margin`, `atms_count`, `cash_withdrawal` | Saralash parametri |
  | `limit` | `integer` | Ixtiyoriy | `20` | Har qanday son | Natijalar soni |

#### Misol so'rov:
`GET /api/v1/analytics/regions/?year=2025&sort_by=profit`

#### Javob namunasi (Response):
```json
[
  {
    "region": "Тошкент ш.",
    "atms_count": 120,
    "operational_count": 115,
    "non_operational_count": 5,
    "operational_rate": 95.83,
    "total_cash_withdrawal": "480000000000.00",
    "total_income": "4800000000.00",
    "total_expense": "1100000000.00",
    "expenses_breakdown": {
      "maintenance": "350000000.00",
      "rent": "420000000.00",
      "electricity": "110000000.00",
      "collection": "180000000.00",
      "service": "40000000.00"
    },
    "net_profit": "3700000000.00",
    "profit_margin": 77.08,
    "avg_income_per_atm": "40000000.00",
    "avg_profit_per_atm": "30833333.33"
  }
]
```

---

### 7.2. Eng Daromadli Bankomatlar (Top Revenue ATMs)
### `GET /api/v1/analytics/atms/top-income/`
Eng ko'p daromad keltirgan bankomatlar reytingi.

- **Query parametrlar:**
  | Parametr | Turi | Majburiyligi | Default | Tavsifi |
  |----------|------|--------------|---------|---------|
  | `year` | `integer` | Ixtiyoriy | Oxirgi | Yil |
  | `month` | `integer` | Ixtiyoriy | Hammasi | Oy (1-12) |
  | `region` | `string` | Ixtiyoriy | Hammasi | Viloyat |
  | `card_type`| `string`| Ixtiyoriy | Hammasi | `UZCARD`, `HUMO` |
  | `limit` | `integer` | Ixtiyoriy | `10` | Top bankomatlar soni (masalan 10, 20, 50) |

#### Javob namunasi (Response):
```json
[
  {
    "rank": 1,
    "terminal_id": "T001452",
    "name": "Bosh ofis vestibyul",
    "region": "Тошкент ш.",
    "model": "GRG H68N",
    "card_type": "UZCARD",
    "cash_withdrawal": "5200000000.00",
    "total_income": "52000000.00",
    "total_expense": "8500000.00",
    "net_profit": "43500000.00",
    "profit_margin": 83.65
  }
]
```

---

### 7.3. Eng Xarajatli Bankomatlar (Top Expense ATMs)
### `GET /api/v1/analytics/atms/top-expense/`
Eng ko'p xarajat yegan bankomatlar va xarajatlarning qayerga ketgani (zapchast, ijara, elektr, inkassatsiya, servis).

- **Query parametrlar:** `year`, `month`, `region`, `limit` (default: 10).

#### Javob namunasi (Response):
```json
[
  {
    "rank": 1,
    "terminal_id": "T009912",
    "name": "Bozor filiali tashqi",
    "region": "Самарқанд",
    "model": "Nautilus Hyosung",
    "total_expense": "28500000.00",
    "total_income": "14000000.00",
    "net_profit": "-14500000.00",
    "profit_margin": -103.57,
    "expenses_breakdown": {
      "maintenance": "18000000.00",
      "rent": "6000000.00",
      "electricity": "1500000.00",
      "collection": "2500000.00",
      "service": "500000.00"
    },
    "main_cost_driver": "maintenance"
  }
]
```

---

### 7.4. Zarar Keltiruvchi / Muammoli Bankomatlar (Loss-Making & Relocation)
### `GET /api/v1/analytics/atms/loss-making/`
Sof foydasi manfiy bo'lgan yoki belgilangan thresholddan kam foyda berayotgan bankomatlar ro'yxati. Har bir bankomat uchun tizim avtomatik tahlil qilib, **zarar sababi** va **Senior tavsiya** (Relokatsiya, ijarani qayta ko'rib chiqish, modelni almashtirish) beradi.

- **Query parametrlar:**
  | Parametr | Turi | Majburiyligi | Default | Tavsifi |
  |----------|------|--------------|---------|---------|
  | `year` | `integer` | Ixtiyoriy | Oxirgi | Yil |
  | `month` | `integer` | Ixtiyoriy | Hammasi | Oy (1-12) |
  | `region` | `string` | Ixtiyoriy | Hammasi | Viloyat |
  | `threshold_profit` | `number` | Ixtiyoriy | `0` | Shu summadan kam foyda qilganlar (masalan `0` yoki `1000000`) |
  | `limit` | `integer` | Ixtiyoriy | `50` | Bankomatlar soni |

#### Javob namunasi (Response):
```json
[
  {
    "terminal_id": "T004510",
    "name": "Qishloq filiali",
    "region": "Қашқадарё",
    "model": "NCR 6622",
    "status": "NOSOZ",
    "income": "3200000.00",
    "expense": "11500000.00",
    "net_profit": "-8300000.00",
    "profit_margin": -259.38,
    "cash_withdrawal": "320000000.00",
    "reason": "Yuqori ta'mirlash xarajatlari va tez-tez nosozlik",
    "action_recommendation": "Bankomat modelini almashtirish yoki gavjumroq savdo markaziga relokatsiya qilish tavsiya etiladi"
  }
]
```

---

### 7.5. Rahbariyat uchun Umumiy Xulosa (Executive KPI Overview)
### `GET /api/v1/analytics/overview/`
Boshqaruv va rahbariyat hisoboti: Asosiy moliyaviy KPIlar, o'tgan davrga nisbatan o'sish dinamikasi (growth %), yetakchi viloyat va eng yaxshi bankomat.

- **Query parametrlar:** `year` (int), `month` (int).

#### Javob namunasi (Response):
```json
{
  "period": {
    "year": 2025,
    "month": 2,
    "month_name": "Fevral"
  },
  "kpis": {
    "total_income": {
      "value": "12500000000.00",
      "previous_value": "11200000000.00",
      "growth_percent": 11.61
    },
    "total_expense": {
      "value": "3100000000.00",
      "previous_value": "3400000000.00",
      "growth_percent": -8.82
    },
    "net_profit": {
      "value": "9400000000.00",
      "previous_value": "7800000000.00",
      "growth_percent": 20.51
    },
    "profit_margin": {
      "value": 75.20,
      "previous_value": 69.64,
      "growth_percent": 5.56
    },
    "loss_making_atms_count": 14
  },
  "leaders": {
    "top_region": {
      "region": "Тошкент ш.",
      "income": "4500000000.00",
      "net_profit": "3500000000.00"
    },
    "top_atm": {
      "terminal_id": "T001452",
      "name": "Bosh ofis vestibyul",
      "net_profit": "43500000.00"
    }
  }
}
```

---

## 🤖 8. Sun'iy Intellekt Analitikasi (Ollama LLM)

Ushbu APIlar mahalliy Ollama sun'iy intellekti yordamida bankomatlar va hududlar statistikasini tahlil qilib, inson tushunadigan o'zbek tilida tayyor tahliliy xulosalar yaratadi.

---

### 8.1. Bitta bankomat bo'yicha AI tahlili
### `POST /api/v1/atms/{id}/ai-analysis/`
- **URL parametr:** `id` (Bankomat ID yoki TID).
- **Request Body:** Bo'sh (hech narsa yuborish shart emas).
- **Kutilish vaqti (Timeout):** LLM matn generatsiya qilishi sababli, frontenda so'rov kutish vaqtini (timeout) kamida `30 - 60 sekund` qilib qo'yish kerak!
- **Frontend tavsiyasi:** Tugma bosilganda Spinner / Loading Skeleton ko'rsatish zarur.

#### Javob namunasi (Response):
```json
{
  "analysis": "Ushbu bankomat (T001452) bo'yicha tahlil:\n1. Moliyaviy holat: Rentabellik darajasi yuqori (83.6%), naqd pul aylanmasi barqaror.\n2. Texnik holat: Oxirgi 6 oyda faqat 1 marta profilaktika o'tkazilgan, nosozliklar kuzatilmagan.\n3. Tavsiya: Inkassatsiya chastotasini haftasiga 3 martaga oshirish va mavjud joylashuvni saqlab qolish maqsadga muvofiq."
}
```

---

### 8.2. Viloyat va Davr bo'yicha AI Tahlili
### `POST /api/v1/regions/ai-analysis/`  *(va `POST /api/v2/regions/ai-analysis/`)*
Viloyatning ko'rsatilgan yillar va oylar oralig'idagi umumiy ko'rsatkichlarini AI orqali tahlil qilish.

- **Request Headers:** `Content-Type: application/json`
- **Request Body parametrlar:**
  | Maydon | Turi | Majburiyligi | Tavsifi / Namunalar |
  |--------|------|--------------|---------------------|
  | `region` | `string` | **Majburiy** | Viloyat nomi (masalan: `"Самарқанд"`, `"Тошкент ш."`) |
  | `start_year` | `integer` | Ixtiyoriy | Boshlang'ich yil (masalan: `2025`) |
  | `end_year` | `integer` | Ixtiyoriy | Tugash yili (masalan: `2025`) |
  | `start_month` | `integer` | Ixtiyoriy | Boshlang'ich oy (1-12) |
  | `end_month` | `integer` | Ixtiyoriy | Tugash oyi (1-12) |

#### So'rov namunasi (Request):
```json
{
  "region": "Самарқанд",
  "start_year": 2025,
  "end_year": 2025,
  "start_month": 1,
  "end_month": 12
}
```

#### Javob namunasi (Response):
```json
{
  "region": "Самарқанд",
  "start_year": 2025,
  "end_year": 2025,
  "start_month": 1,
  "end_month": 12,
  "analytics": {
    "total_atms": 68,
    "operational_atms": 61,
    "total_income": "2400000000.00",
    "total_expense": "820000000.00",
    "net_profit": "1580000000.00"
  },
  "analysis": "Самарқанд вилояти бўйича 2025-йил якунлари таҳлили:\n\n• Умумий ҳолат: Вилоятдаги 68 та банкоматдан 61 таси узлуксиз ишламоқда (90% созлик кўрсаткичи).\n• Молиявий самарадорлик: Жами даромад 2.4 млрд сўмни, соф фойда эса 1.58 млрд сўмни ташкил этди.\n• Асосий муаммолар: 4 та банкоматда диспенсер модули бўйича такрорий таъмирлаш харажатлари юқори бўлган.\n• Хулоса ва таклиф: Туристлар оқими юқори бўлган Регистон ва Сиёб бозори ҳудудидаги банкоматларни янги авлод қурилмаларига алмаштириш тавсия этилади."
}
```

---

## 💻 9. Frontend (TypeScript / React) Integratsiya Qo'llanmasi

### 9.1. Asosiy TypeScript Modellar (Types / Interfaces)
Frontend loyihangizga `src/types/atm.ts` faylini ochib, quyidagi interfeyslarni qo'yishingiz mumkin:

```typescript
// --- Umumiy Pagination ---
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// --- Bankomat Item ---
export interface ATMListItem {
  id: number;
  terminal_id: string;
  merchant_id: string;
  name: string;
  region: string;
  address: string;
  card_type: 'UZCARD' | 'HUMO';
  status: 'SOZ' | 'NOSOZ';
  model: string;
  serial_number: string;
  is_active: boolean;
  current_month_income: string;
  current_month_expense: string;
  current_month_profit: string;
}

// --- Viloyat Analitikasi ---
export interface RegionAnalyticsItem {
  region: string;
  atms_count: number;
  operational_count: number;
  non_operational_count: number;
  operational_rate: number;
  total_cash_withdrawal: string;
  total_income: string;
  total_expense: string;
  expenses_breakdown: {
    maintenance: string;
    rent: string;
    electricity: string;
    collection: string;
    service: string;
  };
  net_profit: string;
  profit_margin: number;
  avg_income_per_atm: string;
  avg_profit_per_atm: string;
}

// --- Top Daromadli ATM ---
export interface TopIncomeATM {
  rank: number;
  terminal_id: string;
  name: string;
  region: string;
  model: string;
  card_type: string;
  cash_withdrawal: string;
  total_income: string;
  total_expense: string;
  net_profit: string;
  profit_margin: number;
}

// --- Zarardagi ATM ---
export interface LossMakingATM {
  terminal_id: string;
  name: string;
  region: string;
  model: string;
  status: string;
  income: string;
  expense: string;
  net_profit: string;
  profit_margin: number;
  cash_withdrawal: string;
  reason: string;
  action_recommendation: string;
}
```

---

## 🎯 10. Frontchiga Nimalarni Taqdim Etish Kerak? (Handover Cheklisti)

Frontend dasturchiga quyidagi 4 ta narsani taqdim etsangiz, u hech qanday savollarsiz to'liq integratsiyani amalga oshira oladi:

1. **Ushbu Hujjat:** Loyihadagi `API_DOCUMENTATION.md` fayli.
2. **Swagger Linki:**
   - Lokal: `http://localhost:8000/api/docs/`
   - Server: `https://atm-info.turonbank.uz/api/docs/`
3. **OpenAPI Schema Fayllari (Postman uchun):**
   - Loyihaning bosh papkasidagi `schema.json` yoki `schema.yaml` fayli (Postman-da *Import* tugmasini bosib faylni tanlasa, barcha 16 ta so'rov tayyor to'plam bo'lib tushadi).
4. **Base URL va Muhit sozlamalari:**
   - Base URL: `http://localhost:8000` (yoki test server manzili)
   - CORS ruxsat berilgan: Ha (`*`)
   - Autentifikatsiya: Ochiq (`AllowAny`)
