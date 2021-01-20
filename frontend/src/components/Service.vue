<template>
  <div class="fixed w-full h-screen bg-white flex items-center justify-center">
    <div class="text-center w-5/6 mx-auto">
      <h5 class="text-2xl text-indigo-500 font-bold tracking-wide">
        {{ serviceStatusMessage }}
      </h5>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Service',
  props: {
    serviceStatusMessage: String,
  },
}
</script>
