import {AxiosError, AxiosRequestConfig, AxiosResponse} from "axios";
import {Ref} from "vue";

interface AxiosResult<T = any> extends AxiosResponse<T>{
  error?: AxiosError<T>
};

declare module 'axios' {
  export interface AxiosRequestConfig {
    loading?: Ref<boolean>;
  }
}

declare module "axios" {
  export interface AxiosInstance {
    get<T = any, R = AxiosResult<T>>(url: string, config?: AxiosRequestConfig): Promise<R>;
    post<T = any, R = AxiosResult<T>>(url: string, data?: any, config?: AxiosRequestConfig): Promise<R>;
    put<T = any, R = AxiosResult<T>>(url: string, data?: any, config?: AxiosRequestConfig): Promise<R>;
    delete<T = any, R = AxiosResult<T>>(url: string, config?: AxiosRequestConfig): Promise<R>;
  }
}