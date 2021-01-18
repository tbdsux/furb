import vue from '@vitejs/plugin-vue'

const viteEnv = {}
Object.keys(process.env).forEach((key) => {
  if (key.startsWith(`VITE_`)) {
    viteEnv[`import.meta.env.${key}`] = process.env[key]
  }
})

export default {
  alias: {
    '@': require('path').resolve(__dirname, 'src'),
  },
  define: viteEnv,
  plugins: [vue()],
}
