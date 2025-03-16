"use client";

import { useEffect, useState } from 'react';
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

    const [startDate, setStartTime] = useState<string>('');
    const [endDate, setEndTime] = useState<string>('');

    const filteredAppointments = appointmentStore.data?.filter((appointment: Appointment) => {
        const appointmentStartDate = new Date(appointment.start_date);
        const appointmentEndDate = new Date(appointment.end_date);

        const filterStartDate = startDate ? new Date(`${startDate}T00:00:00`) : null;
        // filterStartDate?.setHours(0, 0, 0, 0);
        const filterEndDate = endDate ? new Date(`${endDate}T23:59:59`) : null;
        console.log(filterEndDate)
        // filterEndDate?.setHours(23, 59, 59, 999);
        console.log(filterEndDate)

        if (filterStartDate && appointmentStartDate < filterStartDate) {
            return false;
        }
        if (filterEndDate && appointmentEndDate > filterEndDate) {
            return false;
        }
        return true;
    }).sort((a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime());

    return (
    <div className="grid grid-rows-[20px_1fr_20px] justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1 className="text-[32px] font-[700]">Appointments</h1>
        <div className="flex gap-4 mb-4">
            <div className='flex flex-col'>
                <h2>Start</h2>
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartTime(e.target.value)}
                    className="p-2 border border-gray-300 rounded"
                    max={endDate}
                />
            </div>

            <div className='flex flex-col'>
                <h2>End</h2>
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndTime(e.target.value)}
                    className="p-2 border border-gray-300 rounded"
                    min={startDate}
                    disabled={!startDate}
                />
            </div>
        </div>
        {appointmentStore.loading && clinicianStore.loading && patientStore.loading ? (
            <p>Loading...</p>
        ) : appointmentStore.error || clinicianStore.error || patientStore.error ? (
            <p>Error fetching data: {appointmentStore.error || clinicianStore.error || patientStore.error}</p>
        ) : (
            <table className="min-w-full table-auto border-collapse border border-gray-200 dark:border-gray-700">
                <thead className="bg-gray-100 dark:bg-gray-800">
                    <tr>
                        <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Id</th>
                        <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Patient</th>
                        <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Clinician</th>
                        <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Date</th>
                        <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Start Time</th>
                        <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">End Time</th>
                        <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredAppointments?.map((appointment: Appointment) => {
                        const patient = patientStore.getPatientById(appointment.patient);
                        const clinician = clinicianStore.getClinicianById(appointment.clinician);
                        return (
                            <tr key={appointment.id} className="border-t border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-300">{appointment.id}</td>
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-300">{patient?.first_name} {patient?.last_name}</td>
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-300">{clinician?.first_name} {clinician?.last_name}</td>
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-300">{new Date(appointment.start_date).toLocaleDateString()}</td>
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-300">{new Date(appointment.start_date).toLocaleTimeString()}</td>
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-300">{new Date(appointment.end_date).toLocaleTimeString()}</td>
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-300">{appointment.status}</td>
                            </tr>
                        )})}
                </tbody>
            </table>
        )}
        </main>
    </div>
    );
}
