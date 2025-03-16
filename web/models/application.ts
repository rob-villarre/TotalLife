export interface Appointment {
    id: number;
    patient: number;
    clinician: number
    start_date: string;
    end_date: string;
    status: string;
    created_at: string;
}