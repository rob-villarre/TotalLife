"use client";

import { useEffect } from 'react';
import useAppointmentStore from './storeAppointment'
import { Appointment } from '@/models/application';
import usePatientStore from './storePatient';
import { Patient } from '@/models/patient';
import useClinicianStore from './storeClinician';
import { Clinician } from '@/models/clinician';

export default function Home() {

    const appointmentStore = useAppointmentStore();
    const patientStore = usePatientStore();
    const clinicianStore = useClinicianStore();

    useEffect(() => {
        const appointmentEndpoint = process.env.NEXT_PUBLIC_RESTAPI_APPOINTMENT_URL;
        if (!appointmentEndpoint) {
            console.error('NEXT_PUBLIC_RESTAPI_APPOINTMENT_URL is not set');
            return;
        }
        appointmentStore.fetchAppointments(appointmentEndpoint);

        const patientEndpoint = process.env.NEXT_PUBLIC_RESTAPI_PATIENT_URL;
        if (!patientEndpoint) {
            console.error('NEXT_PUBLIC_RESTAPI_PATIENT_URL is not set');
            return;
        }
        patientStore.fetchPatients(patientEndpoint);

        const clinicianEndpoint = process.env.NEXT_PUBLIC_RESTAPI_CLINICIAN_URL;
        if (!clinicianEndpoint) {
            console.error('NEXT_PUBLIC_RESTAPI_CLINICIAN_URL is not set');
            return;
        }
        clinicianStore.fetchClinicians(clinicianEndpoint);

    }, []);

    return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <div>
            {appointmentStore.loading ? (
                <p>Loading...</p>
            ) : appointmentStore.error ? (
                <p>Error fetching data: {appointmentStore.error}</p>
            ) : (
                <ul>
                {appointmentStore.data?.map((appointment: Appointment) => (
                    <div key={appointment.id}>
                        <h3>{appointment.status}</h3>
                        <p>Patient ID: {appointment.patient_id}</p>
                        <p>Clinician ID: {appointment.clinician_id}</p>
                        <p>Start Time: {new Date(appointment.start_time).toLocaleString()}</p>
                        <p>End Time: {new Date(appointment.end_time).toLocaleString()}</p>
                    </div>
                ))}
            </ul>
            )}
        </div>
        <div>
            {patientStore.loading ? (
                <p>Loading...</p>
            ) : appointmentStore.error ? (
                <p>Error fetching data: {patientStore.error}</p>
            ) : (
                <ul>
                {patientStore.data?.map((patient: Patient) => (
                    <div key={patient.id}>
                        <h3>{patient.first_name} {patient.last_name}</h3>
                        <p>DoB: {patient.dob}</p>
                        <p>Gender: {patient.gender}</p>
                        <p>Phone Number: {patient.phone_number}</p>
                        <p>Email: {patient.email}</p>
                    </div>
                ))}
                </ul>
            )}
            </div>
        <div>
            {clinicianStore.loading ? (
                <p>Loading...</p>
            ) : appointmentStore.error ? (
                <p>Error fetching data: {clinicianStore.error}</p>
            ) : (
                <ul>
                {clinicianStore.data?.map((clinician: Clinician) => (
                    <div key={clinician.id}>
                        <h3>{clinician.first_name} {clinician.last_name}</h3>
                        <p>NPI Number: {clinician.npi_number}</p>
                        <p>State: {clinician.state}</p>
                    </div>
                ))}
                </ul>
            )}
            </div>
        </main>
    </div>
    );
}
