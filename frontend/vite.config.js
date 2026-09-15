import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        proxy: {
            '/usuarios': 'http://localhost:8000',
            '/ranking': 'http://localhost:8000',
            '/reto1': 'http://localhost:8000',
            '/reto2': 'http://localhost:8000',
            '/reto3': 'http://localhost:8000',
        },
    },
});
