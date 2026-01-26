/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                background: '#0a0a0f',
                surface: '#12121a',
                primary: '#3b82f6', // blue-500
                secondary: '#8b5cf6', // violet-500
                accent: '#06b6d4', // cyan-500
                success: '#10b981',
                warning: '#f59e0b',
                danger: '#ef4444',
            },
            fontFamily: {
                sans: ['Outfit', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
