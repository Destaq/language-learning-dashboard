<template>
  <div class="grid grid-cols-3 items-center">
    <div class="chinese text-xl mt-1">
      {{ data.data.value.chengyu.word }}
    </div>
    <h2 class="mx-auto text-xl mt-1">Chinese Learning Dashboard</h2>
    <div class="text-right italic font-light mt-1 font-serif">{{ today }}</div>
  </div>
  <!-- progress bar -->
  <div class="-mt-1">
    <div>
      <div class="mx-auto w-full">
        <div class="mx-auto flex items-center content-center">
          <progress
            :value="
              (vocabData.data.value.vocab_size /
                vocabData.data.value.milestone) *
                100
            "
            max="100"
            class="progress h-1 mr-2 ml-1"
            :class="theme === 'dark' ? 'reverse-progress' : ''"
          ></progress>
          <span class="mr-1 font-serif">{{ vocabData.data.value.milestone }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    theme: {
      type: String,
      default: "garden",
    },
  },
  async setup() {
    const [data, vocabData] = await Promise.all([
      useFetch(`http://127.0.0.1:5000/random-chengyu`),
      useFetch(`http://127.0.0.1:5000/get-vocab-size-and-milestone`),
    ]);

    // get today in the format: "Monday, January 1, 2020"
    const today = new Date().toLocaleDateString("en-US", {
      weekday: "long",
      month: "long",
      day: "numeric",
      year: "numeric",
    });

    return {
      data,
      today,
      vocabData,
    };
  },
};
</script>

<style scoped>
.reverse-progress::-moz-progress-bar {
  --tw-bg-opacity: 1;
  background-color: rgb(125, 125, 125);
}
.reverse-progress::-webkit-progress-bar {
  --tw-bg-opacity: 1;
  --tw-bg-opacity: 0.2;
  background-color: rgb(125, 125, 125);
  border-radius: var(--rounded-box, 1rem);
}
.reverse-progress::-webkit-progress-value {
  --tw-bg-opacity: 1;
  background-color: #fff;
  border-radius: var(--rounded-box, 1rem);
}
</style>
