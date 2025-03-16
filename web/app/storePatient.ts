import { create } from 'zustand'
import { Patient } from '@/models/patient';

interface DataState {
    data: Patient[] | null;
    loading: boolean;
    error: string | null;
    fetchPatients: (endpoint: string) => Promise<void>;
    getPatientById: (id: number) => Patient | undefined;
}

const usePatientStore = create<DataState>((set: (args: { loading: boolean; error?: string | null; data?: Patient[]; }) => void) => ({
    data: null,
    loading: false,
    error: null,
    fetchPatients: async (endpoint) => {
        set({ error: null, loading: true });

        const apiURL = endpoint;
        if (!apiURL) {
            set({error: 'endpoint variable is not set', loading: false});
            return;
        }

        try {
            const response = await fetch(apiURL);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const data = await response.json();
            set({ data, loading: false });
        } catch (error) {
            set({ error: (error as Error).message, loading: false });
        }
    },
    getPatientById: (id: number): Patient | undefined => {
        const state = usePatientStore.getState();
        return state.data?.find((clinician: Patient) => clinician.id === id);
    },
}));

export default usePatientStore;