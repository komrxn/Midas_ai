export enum CategoryType {
    INCOME = 'income',
    EXPENSE = 'expense',
}

export interface Category {
    id: string;
    name: string;
    slug: string;
    type: CategoryType;
    icon: string;
    color: string;
    user_id: string | null;
    is_default: boolean;
    created_at: string;
}

export interface CategoryCreateData {
    name: string;
    slug: string;
    type: CategoryType;
    icon: string;
    color: string;
}

export interface CategoryUpdateData {
    name: string;
    icon: string;
    color: string;
}

export interface CategoryFormData {
    name: string;
    icon: string;
    color?: string;
    type?: CategoryType;
    isHidden?: boolean;
}

export interface GetCategoriesParams {
    type?: CategoryType;
}
