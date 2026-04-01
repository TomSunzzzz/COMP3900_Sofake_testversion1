import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  //test use: only
  test: {
    // 关键点：这一行告诉 Vitest 模拟一个浏览器环境
    environment: 'jsdom', 
    // 建议加上这个，这样你就不需要在每个测试文件里手动 import { describe, it } 了
    globals: true, 
  },
})
