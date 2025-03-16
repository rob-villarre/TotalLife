import { create } from 'zustand'
import { Clinician } from '@/models/clinician';

interface DataState {
    data: Clinician[] | null;
    loading: boolean;
    error: string | null;
    fetchClinicians: (endpoint: string) => Promise<void>;
}

const useClinicianStore = create<DataState>((set: (args: { loading: boolean; error?: string | null; data?: Clinician[]; }) => void) => ({
    data: null,
    loading: false,
    error: null,
    fetchClinicians: async (endpoint) => {
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
            console.log(data)
            set({ data, loading: false });
        } catch (error) {
            set({ error: (error as Error).message, loading: false });
        }
    },
}));

export default useClinicianStore;