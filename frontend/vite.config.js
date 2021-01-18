import path from 'path'
import vue from '@vitejs/plugin-vue'

const viteEnv = {}
Object.keys(process.env).forEach((key) => {
  if (key.startsWith(`VITE_`)) {
    viteEnv[`import.meta.env.${key}`] = process.env[key]
  }
})

console.log(viteEnv)

export default {
  alias: {
    '@': path.resolve(__dirname, 'src'),
  },
  define: viteEnv,
  plugins: [vue()],
}
