export interface Appointment {
    id: number;
    patient_id: number;
    clinician_id: number
    start_time: string;
    end_time: string;
    status: string;
    created_at: string;
}