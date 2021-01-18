<template>
  <main class="antialiased">
    <div class="w-11/12 md:w-5/6 lg:w-4/5 mx-auto py-12">
      <Header />

      <hr class="my-4" />

      <!-- main ulr input -->
      <div
        class="w-full sm:w-5/6 mx-auto flex flex-col md:flex-row items-center justify-center"
      >
        <input
          v-model="manga_url_input"
          type="url"
          placeholder="Enter the url of the manga / manhwa / manhua"
          class="border-2 py-3 px-4 text-lg tracking-wider rounded-lg w-full focus:outline-none focus:border-indigo-500 text-gray-600"
        />
        <button
          v-if="query"
          @click.once="QueryManga"
          class="mt-2 md:mt-0 px-10 py-3 bg-indigo-400 hover:bg-indigo-500 text-white border-indigo-400 border-2 ml-2 rounded-lg text-lg uppercase tracking-wide"
        >
          {{ btn_request_text }}
        </button>
        <button
          v-else
          @click.once="QueryManga"
          class="mt-2 md:mt-0 px-10 py-3 bg-gray-400 hover:bg-gray-500 text-white border-gray-400 border-2 ml-2 rounded-lg text-lg lowercase tracking-wide"
        >
          another
        </button>
      </div>

      <!-- results -->
      <div v-show="request_done" class="my-6 w-full sm:w-5/6 mx-auto">
        <div
          class="flex flex-col md:flex-row items-start md:items-center justify-between"
        >
          <p class="text-gray-400 text-lg tracking-wide md:my-1 md:mr-2">
            Manga:
            <span class="font-bold underline">{{ manga.manga_title }}</span>
          </p>
          <p class="text-gray-400 tracking-wide md:my-1">
            Source:
            <span class="underline">{{ manga.source }}</span>
          </p>
        </div>

        <hr class="mb-2" />

        <div class="my-3 w-11/12 mx-auto h-96 overflow-y-scroll">
          <ul>
            <chapter
              v-for="chapter in manga.results"
              :key="manga.results.indexOf(chapter)"
              :chapter="chapter"
            ></chapter>
          </ul>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios'

import Header from './components/Header.vue'
import Chapter from './components/Chapter.vue'

import { envs } from './utils/config'

export default {
  name: 'App',
  components: {
    Header,
    Chapter,
  },
  data() {
    return {
      manga_url_input: '',
      btn_request_text: 'query',
      query: true,
      request_done: false,
      manga: {},
      queue: 0,
    }
  },
  methods: {
    QueryManga() {
      console.log(process.env)
      console.log(import.meta.env)
      console.log(import.meta.env.VITE_FURB_BACKEND_API)
      // // change button text
      // this.btn_request_text = 'querying...'

      // axios
      //   .post(
      //     `${
      //       process.env.NODE_ENV === 'production'
      //         ? process.env.VITE_FURB_BACKEND_API
      //         : import.meta.env.VITE_FURB_BACKEND_API
      //     }/grab`,
      //     {
      //       url: this.manga_url_input,
      //     },
      //     {
      //       headers: {
      //         'Content-Type': 'application/json',
      //       },
      //     },
      //   )
      //   .then((resp) => {
      //     // set the manga
      //     this.manga = resp.data

      //     // change states
      //     this.request_done = true
      //     this.btn_request_text = 'query'
      //     this.query = false
      //   })
      //   .catch((e) => console.error(e))
    },
    Queuer() {},
  },
}
</script>
