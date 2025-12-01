import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// [https://vitejs.dev/config/](https://vitejs.dev/config/)
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // [重要] 允许局域网内的其他设备（如手机/电脑）访问
    port: 3000,      // 指定端口为 3000
  }
})
