/**
 * API client for the Clinic Prescription App.
 * All functions are typed and use the Axios instance with baseURL /api/v1.
 */

import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

// ---- Generic types ----

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// ---- Master data types ----

export interface Illness {
  id: number;
  name: string;
  created_at?: string;
  updated_at?: string;
}

export interface Medicine {
  id: number;
  name: string;
  medicine_type: string;
  default_duration_days: number;
  dose_times: string;
  prerequisite: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface Patient {
  id: number;
  name: string;
  name_marathi: string | null;
  gender: string | null;
  age: number | null;
  mobile_number: string | null;
  residence: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface LabTest {
  id: number;
  name: string;
}

export interface Symptom {
  id: number;
  name: string;
}

export interface ReferralDoctor {
  id: number;
  name: string;
  address: string | null;
  phone_number: string | null;
}

export interface AdviceTemplate {
  id: number;
  text: string;
}

// ---- Prescription template types ----

export interface PrescriptionTemplate {
  id: number;
  name: string;
  symptom_links?: { symptom_id: number }[];
  medicines?: TemplateMedicine[];
  advice?: { advice_text: string }[];
  lab_test_links?: { lab_test_id: number }[];
  created_at?: string;
  updated_at?: string;
}

export interface TemplateMedicine {
  medicine_id: number;
  duration_days: number;
  dose_times: string;
  prerequisite: string | null;
}

// ---- Prescription types ----

export interface PrescriptionCreate {
  patient: {
    id: number | null;
    name: string;
    name_marathi?: string;
    gender?: string;
    age?: number;
    mobile_number?: string;
    residence?: string;
  };
  date: string;
  patient_type: string;
  illness_id?: number | null;
  blood_pressure?: string;
  temperature?: string;
  spo2?: string;
  pulse?: string;
  symptoms: { id: number | null; name: string }[];
  medicines: {
    medicine: { id: number; name: string; medicine_type?: string };
    duration_days: number;
    dose_times: string;
    prerequisite: string | null;
  }[];
  advice: { advice_text: string }[];
  lab_tests: { id: number | null; name: string }[];
  referrals: { id: number | null; name: string; address?: string; phone_number?: string }[];
  save_as_template: boolean;
  template_symptom_ids: number[];
}

export interface PrescriptionDetail {
  id: number;
  patient: Patient;
  date: string;
  patient_type: string;
  illness_id: number | null;
  blood_pressure: string | null;
  temperature: string | null;
  spo2: string | null;
  pulse: string | null;
  symptom_links: { symptom: Symptom }[];
  medicines: { medicine: Medicine; duration_days: number; dose_times: string; prerequisite: string | null }[];
  advice: { advice_text: string }[];
  lab_test_links: { lab_test: LabTest }[];
  referral_links: { referral_doctor: ReferralDoctor }[];
  created_at: string;
}

// ---- API functions ----

// Master data CRUD
export const illnessApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<Illness>>('/illnesses', { params }),
  get: (id: number) => api.get<Illness>(`/illnesses/${id}`),
  create: (data: Partial<Illness>) => api.post<Illness>('/illnesses', data),
  update: (id: number, data: Partial<Illness>) => api.put<Illness>(`/illnesses/${id}`, data),
  delete: (id: number) => api.delete(`/illnesses/${id}`),
};

export const medicineApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<Medicine>>('/medicines', { params }),
  get: (id: number) => api.get<Medicine>(`/medicines/${id}`),
  create: (data: Partial<Medicine>) => api.post<Medicine>('/medicines', data),
  update: (id: number, data: Partial<Medicine>) => api.put<Medicine>(`/medicines/${id}`, data),
  delete: (id: number) => api.delete(`/medicines/${id}`),
};

export const patientApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<Patient>>('/patients', { params }),
  get: (id: number) => api.get<Patient>(`/patients/${id}`),
  create: (data: Partial<Patient>) => api.post<Patient>('/patients', data),
  update: (id: number, data: Partial<Patient>) => api.put<Patient>(`/patients/${id}`, data),
  delete: (id: number) => api.delete(`/patients/${id}`),
};

export const labTestApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<LabTest>>('/lab-tests', { params }),
  get: (id: number) => api.get<LabTest>(`/lab-tests/${id}`),
  create: (data: Partial<LabTest>) => api.post<LabTest>('/lab-tests', data),
  update: (id: number, data: Partial<LabTest>) => api.put<LabTest>(`/lab-tests/${id}`, data),
  delete: (id: number) => api.delete(`/lab-tests/${id}`),
};

export const symptomApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<Symptom>>('/symptoms', { params }),
  get: (id: number) => api.get<Symptom>(`/symptoms/${id}`),
  create: (data: Partial<Symptom>) => api.post<Symptom>('/symptoms', data),
  update: (id: number, data: Partial<Symptom>) => api.put<Symptom>(`/symptoms/${id}`, data),
  delete: (id: number) => api.delete(`/symptoms/${id}`),
};

export const referralDoctorApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<ReferralDoctor>>('/referral-doctors', { params }),
  get: (id: number) => api.get<ReferralDoctor>(`/referral-doctors/${id}`),
  create: (data: Partial<ReferralDoctor>) => api.post<ReferralDoctor>('/referral-doctors', data),
  update: (id: number, data: Partial<ReferralDoctor>) => api.put<ReferralDoctor>(`/referral-doctors/${id}`, data),
  delete: (id: number) => api.delete(`/referral-doctors/${id}`),
};

export const adviceTemplateApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<AdviceTemplate>>('/advice-templates', { params }),
  get: (id: number) => api.get<AdviceTemplate>(`/advice-templates/${id}`),
  create: (data: Partial<AdviceTemplate>) => api.post<AdviceTemplate>('/advice-templates', data),
  update: (id: number, data: Partial<AdviceTemplate>) => api.put<AdviceTemplate>(`/advice-templates/${id}`, data),
  delete: (id: number) => api.delete(`/advice-templates/${id}`),
};

// Prescription templates
export const prescriptionTemplateApi = {
  list: (params?: { q?: string; skip?: number; limit?: number }) => api.get<PaginatedResponse<PrescriptionTemplate>>('/prescription-templates', { params }),
  get: (id: number) => api.get<PrescriptionTemplate>(`/prescription-templates/${id}`),
  create: (data: unknown) => api.post<PrescriptionTemplate>('/prescription-templates', data),
  update: (id: number, data: unknown) => api.put<PrescriptionTemplate>(`/prescription-templates/${id}`, data),
  delete: (id: number) => api.delete(`/prescription-templates/${id}`),
  recommend: (symptomIds: number[]) => api.get<PrescriptionTemplate[]>('/prescription-templates/recommend', { params: { symptom_ids: symptomIds.join(',') } }),
};

// Prescriptions
export const prescriptionApi = {
  list: (params?: { patient_id?: number; date?: string; q?: string; skip?: number; limit?: number }) =>
    api.get<PaginatedResponse<PrescriptionDetail>>('/prescriptions', { params }),
  get: (id: number) => api.get<PrescriptionDetail>(`/prescriptions/${id}`),
  create: (data: PrescriptionCreate) => api.post<PrescriptionDetail>('/prescriptions', data),
};

export default api;
