<template>
  <main class="antialiased">
    <!-- service checker
    this will be shown if the backend is being contacted
    or it is currently down / not working
     -->
    <Service
      v-if="!backendServiceStatus"
      :serviceStatusMessage="backendContactStatus"
    />

    <!-- main app (show only if backend is working / alive) -->
    <div v-else class="w-11/12 md:w-5/6 lg:w-4/5 mx-auto py-12">
      <Header />

      <hr class="my-4" />

      <!-- queuer error message -->
      <div class="mb-5" v-show="errorQueue">
        <p class="text-center text-lg text-red-500">
          Queued grabber are limited to
          <span class="font-bold">TWO (2)</span>
          concurrent requests.
          <br />
          Please wait for other requests to finish.
        </p>
      </div>

      <!-- main url input -->
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
          v-show="query"
          :key="btn_request_key"
          @click.once="QueryManga"
          class="mt-2 md:mt-0 px-10 py-3 bg-indigo-400 hover:bg-indigo-500 text-white border-indigo-400 border-2 ml-2 rounded-lg text-lg uppercase tracking-wide"
        >
          {{ btn_request_text }}
        </button>
        <button
          v-show="!query"
          @click.once="AnotherSession"
          class="mt-2 md:mt-0 px-10 py-3 bg-gray-400 hover:bg-gray-500 text-white border-gray-400 border-2 ml-2 rounded-lg text-lg lowercase tracking-wide"
        >
          another
        </button>
      </div>

      <!-- form request error -->
      <div class="mt-1 mb-3 sm:w-5/6 mx-auto" v-show="queryError">
        <p class="text-red-500 text-center md:text-left">
          There was a problem with your request. Please check the URL of the
          Manga / Manhwa / Manhua and try again.
        </p>
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
              :errorQueue="errorQueue"
              @add-queuer="Queuer('add')"
              @subtract-queuer="Queuer('subtract')"
            ></chapter>
          </ul>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios'

import Service from './components/Service.vue'
import Header from './components/Header.vue'
import Chapter from './components/Chapter.vue'

const InitialData = () => {
  return {
    manga_url_input: '',
    btn_request_text: 'query',
    query: true,
    request_done: false,
    manga: {},
    queue: 0,
    errorQueue: false,
    queryError: false,
    btn_request_key: 1,
  }
}

export default {
  name: 'App',
  components: {
    Service,
    Header,
    Chapter,
  },
  data() {
    return {
      ...InitialData(),
      maxSetQueue: 2,
      backendServiceStatus: false,
      backendContactStatus: 'Contacting the BACKEND API Server...',
    }
  },
  methods: {
    QueryManga() {
      // change button text
      this.btn_request_text = 'querying...'

      axios
        .post(
          `${import.meta.env.VITE_FURB_BACKEND_API}/grab`,
          {
            url: this.manga_url_input,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          },
        )
        .then((resp) => {
          // set the manga
          this.manga = resp.data

          // change states
          this.request_done = true
          this.btn_request_text = 'query'
          this.query = false
          this.queryError = false
        })
        .catch((_) => {
          // show error, error could either mean that
          // the inputted url is not valid / not the url of
          // the manga itself
          this.queryError = true

          // reset button
          this.btn_request_text = 'query'
          this.btn_request_key++
        })
    },
    Queuer(method) {
      // for adding to queue
      if (method === 'add') {
        // if the requests == max grabber jobs
        // this is to limit the amount of requests being
        // sent to the backend server
        // which could result to failing requests
        if (this.queue === this.maxSetQueue) {
          // show limit error
          this.errorQueue = true
        } else {
          // otherwise, increment worker job
          this.queue++
        }
      }
      // for subtracting requests
      else if (method === 'subtract') {
        // decrement worker job
        this.queue--
        // do not show error
        this.errorQueue = false
      }
    },
    AnotherSession() {
      // reset everything and create a new session
      Object.assign(this.$data, InitialData())
    },
  },
  mounted() {
    // contact the backend api if it is on or not
    axios
      .get(`${import.meta.env.VITE_FURB_BACKEND_API}/api`)
      .then(() => {
        // update state status => true
        this.backendServiceStatus = true
        this.backendContactStatus = ''
      })
      .catch(() => {
        // set failed status
        this.backendServiceStatus = false
        this.backendContactStatus =
          'The BACKEND API Server is currently down, please try again later.'
      })
  },
}
</script>
