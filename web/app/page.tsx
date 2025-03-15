"use client";

import { useEffect } from 'react';
import useAppointmentStore from './storeAppointment'
import { Appointment } from '@/models/application';

export default function Home() {

    const { data, loading, error, fetchData } = useAppointmentStore();

    useEffect(() => {
        const endpoint = process.env.NEXT_PUBLIC_RESTAPI_APPOINTMENT_URL;
        if (!endpoint) {
            console.error('NEXT_PUBLIC_RESTAPI_APPOINTMENT_URL is not set');
            return;
        }
        console.log(endpoint);
        fetchData(endpoint);
    }, []);

    return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <div>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>Error fetching data: {error}</p>
            ) : (
                <ul>
                {data?.map((appointment: Appointment) => (
                    <div key={appointment.id}>
                        <h3>{appointment.status}</h3>
                        <p>Patient ID: {appointment.patientId}</p>
                        <p>Clinician ID: {appointment.clinicianId}</p>
                        <p>Start Time: {new Date(appointment.startTime).toLocaleString()}</p>
                        <p>End Time: {new Date(appointment.endTime).toLocaleString()}</p>
                    </div>
                ))}
                </ul>
            )}
            </div>
        </main>
    </div>
    );
}
