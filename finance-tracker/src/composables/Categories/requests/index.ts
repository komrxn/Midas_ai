import $axios from "@/api";
import { CategoryCreateData, CategoryUpdateData, GetCategoriesParams } from "../types";
import { setCategory } from "../models";
import type { Category } from "../types";

export const useCategoriesRequests = () => {
    const getCategories = async (params?: GetCategoriesParams): Promise<Category[]> => {
        try {
            const response = await $axios.get<Category[]>('/categories', { params });
            return response.data.map(item => setCategory(item));
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const createCategory = async (category: CategoryCreateData): Promise<Category> => {
        try {
            const response = await $axios.post<Category>('/categories', category);
            return setCategory(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const updateCategory = async (id: string, category: CategoryUpdateData): Promise<Category> => {
        try {
            const response = await $axios.patch<Category>(`/categories/${id}`, category);
            return setCategory(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const deleteCategory = async (id: string): Promise<void> => {
        try {
            await $axios.delete(`/categories/${id}`);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    return {
        getCategories,
        createCategory,
        updateCategory,
        deleteCategory,
    }
}
