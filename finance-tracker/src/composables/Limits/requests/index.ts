import $axios from "@/api";
import { GetLimitsParams, LimitCreateData, LimitUpdateData } from "../types";
import { setLimits } from "../models";
import type { Limit } from "../types";

export const useLimitsRequests = () => {
    const getLimits = async (params?: GetLimitsParams): Promise<Limit[]> => {
        try {
            const response = await $axios.get<Limit[]>('/limits', { params });
            return response.data.map(item => setLimits(item));
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const addLimit = async (limit: LimitCreateData): Promise<Limit> => {
        try {
            const response = await $axios.post<Limit>('/limits', limit);
            return setLimits(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const removeLimit = async (id: string): Promise<void> => {
        try {
            await $axios.delete<Limit>(`/limits/${id}`);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const updateLimit = async (id: string, limit: LimitUpdateData): Promise<Limit> => {
        try {
            const response = await $axios.put<Limit>(`/limits/${id}`, limit);
            return setLimits(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    return {
        getLimits,
        addLimit,
        removeLimit,
        updateLimit,
    }
}