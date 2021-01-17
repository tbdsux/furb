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
          @click="QueryManga"
          class="mt-2 md:mt-0 px-10 py-3 bg-indigo-400 hover:bg-indigo-500 text-white border-indigo-400 border-2 ml-2 rounded-lg text-lg uppercase tracking-wide"
        >
          query
        </button>
      </div>

      <!-- results -->
      <div class="my-6 w-full sm:w-5/6 mx-auto">
        <p class="text-gray-400 text-lg tracking-wide">
          Manga:
          <span class="font-bold underline">Hello World</span>
        </p>

        <hr class="mb-2" />

        <Results />
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios'

import Header from './components/Header.vue'
import Results from './components/Results.vue'

export default {
  name: 'App',
  components: {
    Header,
    Results,
  },
  data() {
    return {
      manga_url_input: '',
      chapters: [],
    }
  },
  methods: {
    QueryManga() {
      console.log(this.manga_url_input)
    },
  },
}
</script>
