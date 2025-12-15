/// <reference types="vite/client" />
export interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_API_USER: string
  readonly VITE_API_PASSWORD: string
  readonly MODE: 'development' | 'production'
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
