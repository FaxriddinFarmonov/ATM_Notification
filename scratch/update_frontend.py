import os

# 1. Update engineerService.ts
engineer_service_content = '''import axios from 'axios';
import type {
  Engineer,
  EngineerDetail,
  AssignAtmPayload,
  CreateEngineerPayload,
} from '@/types/engineer';

const API_BASE = '/api/v1/engineers';
const DIRECT_API_BASE = 'http://127.0.0.1:8000/api/v1/engineers';

export interface AvailableATMItem {
  id: number;
  serial: string;
  tid: string;
  model_name: string;
  branch_number: string;
  address: string;
  service_status: string;
  cash_amount: number;
  responsible_engineer_id?: number | null;
  responsible_engineer_name?: string | null;
}

export const engineerService = {
  async getEngineers(params?: { search?: string; region?: string }): Promise<Engineer[]> {
    try {
      const res = await axios.get<Engineer[]>(API_BASE, { params });
      return res.data;
    } catch (err) {
      console.warn('Proxy /api/v1/engineers failed, falling back to direct port 8000...', err);
      const res = await axios.get<Engineer[]>(DIRECT_API_BASE, { params });
      return res.data;
    }
  },

  async getEngineerDetail(id: number): Promise<EngineerDetail> {
    try {
      const res = await axios.get<EngineerDetail>(`${API_BASE}/${id}/`);
      return res.data;
    } catch (err) {
      const res = await axios.get<EngineerDetail>(`${DIRECT_API_BASE}/${id}/`);
      return res.data;
    }
  },

  async getAvailableAtms(search?: string): Promise<AvailableATMItem[]> {
    try {
      const res = await axios.get<AvailableATMItem[]>(`${API_BASE}/atms/available/`, { params: { search } });
      return res.data;
    } catch (err) {
      const res = await axios.get<AvailableATMItem[]>(`${DIRECT_API_BASE}/atms/available/`, { params: { search } });
      return res.data;
    }
  },

  async assignAtm(engineerId: number, payload: AssignAtmPayload): Promise<{ status: string; message: string }> {
    try {
      const res = await axios.post(`${API_BASE}/${engineerId}/assign-atm/`, payload);
      return res.data;
    } catch (err) {
      const res = await axios.post(`${DIRECT_API_BASE}/${engineerId}/assign-atm/`, payload);
      return res.data;
    }
  },

  async unassignAtm(engineerId: number, payload: AssignAtmPayload): Promise<{ status: string; message: string }> {
    try {
      const res = await axios.post(`${API_BASE}/${engineerId}/unassign-atm/`, payload);
      return res.data;
    } catch (err) {
      const res = await axios.post(`${DIRECT_API_BASE}/${engineerId}/unassign-atm/`, payload);
      return res.data;
    }
  },

  async createEngineer(payload: CreateEngineerPayload): Promise<Engineer> {
    try {
      const res = await axios.post<Engineer>(`${API_BASE}/`, payload);
      return res.data;
    } catch (err) {
      const res = await axios.post<Engineer>(`${DIRECT_API_BASE}/`, payload);
      return res.data;
    }
  },

  async getAtmResponsibleEngineer(serial: string): Promise<any | null> {
    try {
      const res = await axios.get(`${API_BASE}/atm/${encodeURIComponent(serial)}/engineer/`);
      return res.data;
    } catch (err) {
      try {
        const res = await axios.get(`${DIRECT_API_BASE}/atm/${encodeURIComponent(serial)}/engineer/`);
        return res.data;
      } catch {
        return null;
      }
    }
  },
};
'''

with open(r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\services\engineerService.ts', 'w', encoding='utf-8') as f:
    f.write(engineer_service_content)

print("Updated engineerService.ts successfully!")
