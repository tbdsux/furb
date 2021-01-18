// vite doesn't allow defining and accessing variables outside
// so, this is a solution I found on importing
// non .env variables (or system)
// solution from: https://github.com/vitejs/vite/issues/562

import path from 'path'
import vue from '@vitejs/plugin-vue'

const viteEnv = {}
Object.keys(process.env).forEach((key) => {
  if (key.startsWith(`VITE_`)) {
    viteEnv[`import.meta.env.${key}`] = process.env[key]
  }
})

export default {
  alias: {
    '@': path.resolve(__dirname, 'src'),
  },
  define: viteEnv,
  plugins: [vue()],
}
