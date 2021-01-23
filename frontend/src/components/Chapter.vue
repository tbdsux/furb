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
        :key="btnKey"
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
      btnKey: 1,
    }
  },
  methods: {
    Grab() {
      if (!this.errorQueue) {
        // emit addition to the requests queuer
        this.$emit('add-queuer')
        // increment the button to re-enable the @click.once
        // prob & sol: https://stackoverflow.com/questions/56041297/re-enable-button-click-once-after-clicking
        this.btnKey++
      }

      // defer update from the props errorQueue
      this.$nextTick(function () {
        if (!this.errorQueue) {
          this.btn_grab_text = 'grabbing'

          // request
          axios
            .get(
              `${import.meta.env.VITE_FURB_BACKEND_API}/get/q/${
                this.chapter.b64_hash
              }`,
            )
            .then((resp) => {
              const grab = resp.data

              // set download link
              this.download_link = grab.data.link

              // set state
              this.grab_done = true

              // emit subtract to the requests queuer
              this.$emit('subtract-queuer')
            })
            .catch((_) => {
              // on error, rename button text to retry
              // this will attemp to re-request again
              // this is useful for larger downloads
              // NOTE: not yet tested
              this.btn_grab_text = 'retry'

              // increment the button to re-enable the @click.once
              // prob & sol: https://stackoverflow.com/questions/56041297/re-enable-button-click-once-after-clicking
              this.btnKey++
            })
        }
      })
    },
  },
  props: {
    chapter: Object,
    errorQueue: Boolean,
  },
}
</script>
