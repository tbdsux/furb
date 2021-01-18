<template>
  <li class="my-3">
    <div
      class="border-2 border-indigo-300 w-full flex items-center justify-between py-1 px-4 text-lg rounded-lg shadow"
    >
      <p class="text-gray-600 w-full mr-3 truncate">
        {{ chapter.chapter_name }}
        <span class="font-light tracking-wide">
          <small>(chapter)</small>
        </span>
      </p>
      <a
        v-if="grab_done"
        type="button"
        :href="download_link"
        target="_blank"
        class="py-2 px-4 bg-green-500 opacity-90 hover:opacity-100 text-white rounded-lg uppercase"
      >
        download
      </a>
      <button
        v-else
        @click.once="Grab"
        class="py-2 px-4 bg-indigo-500 opacity-90 hover:opacity-100 text-white rounded-lg"
      >
        {{ btn_grab_text }}
      </button>
    </div>
  </li>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Chapter',
  data() {
    return {
      btn_grab_text: 'grab',
      grab_done: false,
      download_link: '',
    }
  },
  methods: {
    Grab() {
      this.btn_grab_text = 'grabbing'

      // request
      axios
        .get(
          `${
            process.env.NODE_ENV === 'production'
              ? process.env.VITE_FURB_BACKEND_API
              : import.meta.env.VITE_FURB_BACKEND_API
          }/get/q/${this.chapter.b64_hash}`,
        )
        .then((resp) => {
          const grab = resp.data

          // set download link
          this.download_link = grab.data.link

          // set state
          this.grab_done = true
        })
        .catch((e) => console.error(e))
    },
  },
  props: {
    chapter: Object,
  },
}
</script>
