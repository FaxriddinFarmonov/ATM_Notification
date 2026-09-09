import os

# 1. Update endpoints.ts
endpoints_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\api\endpoints.ts'
with open(endpoints_path, 'r', encoding='utf-8') as f:
    endpoints_code = f.read()

if 'annualFinancials:' not in endpoints_code:
    endpoints_code = endpoints_code.replace(
        "models: '/analytics/models/'",
        "models: '/analytics/models/',\n    annualFinancials: '/analytics/annual-financials/'"
    )
    with open(endpoints_path, 'w', encoding='utf-8') as f:
        f.write(endpoints_code)
    print("Updated endpoints.ts")

# 2. Update analyticsService.ts
analytics_service_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\services\analyticsService.ts'
with open(analytics_service_path, 'r', encoding='utf-8') as f:
    service_code = f.read()

if 'getAnnualFinancials' not in service_code:
    new_method = '''
  async getAnnualFinancials(): Promise<any> {
    const { data } = await http.get('/analytics/annual-financials/');
    return data;
  },'''
    service_code = service_code.replace(
      "async getModelAnalytics(): Promise<any> {",
      new_method + "\n\n  async getModelAnalytics(): Promise<any> {"
    )
    with open(analytics_service_path, 'w', encoding='utf-8') as f:
        f.write(service_code)
    print("Updated analyticsService.ts")

# 3. Update DashboardAtmView.vue to replace top large static hero with Executive Annual Financial Hero Header
dashboard_vue_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\DashboardAtmView.vue'

with open(dashboard_vue_path, 'r', encoding='utf-8') as f:
    current_dashboard_code = f.read()

# Let's inspect where the hero header starts in DashboardAtmView.vue
print("Current DashboardAtmView.vue length:", len(current_dashboard_code))
