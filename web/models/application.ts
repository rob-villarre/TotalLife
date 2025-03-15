export interface Appointment {
    id: number;
    patientId: number;
    clinicianId: number
    startTime: string;
    endTime: string;
    status: string;
}