class PromptBuilder:
    @staticmethod
    def build(data: dict) -> str:
        atm_info = data.get("atm", {})
        metrics = data.get("metrics", {})
        service = data.get("service", {})
        records = data.get("monthly_records", [])

        terminal_id = atm_info.get("terminal_id") or "Noma'lum"
        name = atm_info.get("name") or "Noma'lum"
        region = atm_info.get("region") or "Noma'lum"
        model = atm_info.get("model") or "Noma'lum"
        status = atm_info.get("status") or "SOZ"
        serial_number = atm_info.get("serial_number") or "Mavjud emas"

        total_cash_withdrawn = metrics.get("total_cash_withdrawn", 0)
        total_income = metrics.get("total_income", 0)
        total_expense = metrics.get("total_expense", 0)
        net_profit = metrics.get("net_profit", 0)
        profitability_rate = metrics.get("profitability_rate", 0)
        average_income = metrics.get("average_income", 0)
        average_expense = metrics.get("average_expense", 0)

        total_service_fee = service.get("total_service_fee", 0)
        total_utility_cost = service.get("total_utility_cost", 0)
        total_repair_cost = service.get("total_repair_cost", 0)

        monthly_lines = []
        for r in records:
            period = r.get("period", "")
            withdrawn = r.get("cash_withdrawn", 0)
            inc = r.get("income", 0)
            srv = r.get("service_cost", 0)
            util = r.get("utility_cost", 0)
            rep = r.get("repair_cost", 0)
            tot_exp = r.get("total_expense", 0)
            prof = r.get("net_profit", 0)

            monthly_lines.append(
                f"  * {period}: Naqd pul aylanmasi: {withdrawn:,.0f} so'm | "
                f"Komissiya tushumi: {inc:,.0f} so'm | "
                f"Xarajatlar: {tot_exp:,.0f} so'm (Servis: {srv:,.0f}, Svet/Ijara: {util:,.0f}, Ta'mir: {rep:,.0f}) | "
                f"Sof foyda: {prof:,.0f} so'm"
            )

        dynamic_lines_str = chr(10).join(monthly_lines) if monthly_lines else "  * Oylik ma'lumotlar mavjud emas"

        prompt = f"""
Siz Turonbank ATB Bosh ofisining professional bank tahlilchisisiz.
Quyida bitta bankomatning OXIRGI 6 OYLIK aniq va to'g'ri hisoblangan moliyaviy va texnik ko'rsatkichlari berilgan:

BANKOMAT PASPORTI:
- Terminal ID: {terminal_id}
- Nomi: {name}
- Hudud / Filial: {region}
- Modeli: {model}
- Texnik holati: {status} (Seriya raqami: {serial_number})

6 OYLIK YAKUNIY MOLIYAVIY KO'RSATKICHLAR:
- Jami naqd pul aylanmasi (mijozlar yechgan naqd pul): {total_cash_withdrawn:,.0f} so'm (bu bankomatning faollik va tranzaksiya hajmidir)
- Bankning yalpi komissiya daromadi (tushum): {total_income:,.0f} so'm
- Bankning jami haqiqiy operatsion xarajatlari: {total_expense:,.0f} so'm, shundan:
  * Servis to'lovlari (BTech va Glob): {total_service_fee:,.0f} so'm
  * Kommunal va ijara to'lovlari (elektr toki, joy ijarasi, inkassatsiya): {total_utility_cost:,.0f} so'm
  * Ehtiyot qismlar va ta'mirlash xarajatlari: {total_repair_cost:,.0f} so'm
- 6 OYLIK SOF FOYDA (Komissiya tushumi - Jami xarajatlar): {net_profit:,.0f} so'm
- Rentabellik darajasi: {profitability_rate:.1f}%
- Oylik o'rtacha komissiya daromadi: {average_income:,.0f} so'm
- Oylik o'rtacha xarajat: {average_expense:,.0f} so'm

OXIRGI 6 OY DINAMIKASI (OYLAR KESIMIDA):
{dynamic_lines_str}

ASOSIY TALABLAR VA USLUB:
1. Faqat adabiy va sof O'ZBEK tilida, lo'nda va professional bank tahlili uslubida yozing.
2. Moliyaviy mohiyat:
   - "Naqd pul aylanmasi" - mijozlar yechgan mablag' bo'lib, bu bankning xarajati emas, balki bankomatning ish hajmidir.
   - "Komissiya daromadi (Tushum)" - ushbu aylanmadan bankka tushgan sof komissiya.
   - "Operatsion xarajatlar" - servis xizmati, elektr toki, ijara va ehtiyot qismlar ta'mirlash xarajatlari.
   - "Sof foyda" - komissiya tushumidan operatsion xarajatlar chegirilgandan keyin qolgan yakuniy foyda.
3. Agar bankomat faoliyatsiz bo'lsa yoki ko'rsatkichlar 0 bo'lsa:
   "Ushbu bankomat tahlil etilayotgan davrda faoliyat ko'rsatmagan, mijozlar tomonidan naqd pul yechish operatsiyalari amalga oshirilmagan va bankka komissiya tushumi keltirmagan. Bankomatni sozlab, talab yuqori bo'lgan hududga qayta o'rnatish tavsiya etiladi" deb lo'nda va sof o'zbek tilida yozing.
4. Ichki o'ylash (thinking) yozmang, to'g'ridan-to'g'ri hisobot sarlavhalari bilan boshlang.

HISOBOT TUZILISHI:
### 1. Qisqacha xulosa
Bankomatning joylashuvi, texnik holati, naqd pul aylanmasi va 6 oylik yakuniy sof foydasi.

### 2. Naqd pul aylanmasi va daromad tahlili
Mijozlar yechgan naqd pul hajmi (aylanma), bankning komissiya tushumi va oylik dinamika.

### 3. Haqiqiy xarajatlar va servis tahlili
Servis to'lovlari (BTech, Glob), kommunal to'lovlar (elektr, ijara, inkassatsiya) va ehtiyot qismlar ta'mirlash xarajatlari taqsimoti.

### 4. Sof foyda va rentabellik bahosi
Bankning sof foyda dinamikasi, rentabellik darajasi va xarajatlarning samaradorligi.

### 5. Rahbariyat uchun amaliy tavsiyalar
Bankomat samaradorligini oshirish, xarajatlarni optimallashtirish va texnik xizmat bo'yicha 3 ta aniq tavsiya.
"""
        return prompt.strip()
