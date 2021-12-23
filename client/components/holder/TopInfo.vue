<template>
  <div class="grid grid-cols-3 items-center">
    <div class="chinese text-3xl">{{ data.data.value.chengyu.word }}</div>
    <div class="text-xl mx-auto underline">TraceLang</div>
    <div class="text-right">{{ today }}</div>
  </div>
  <!-- progress bar -->
  <div class="border border-base-300">
    <div>
      <div class="stat-desc mx-auto w-full">
        <div class="mx-auto flex items-center content-center">
          <span class="ml-1">0</span>
          <progress
            :value="
              (vocabData.data.value.vocab_size /
                vocabData.data.value.milestone) *
                100
            "
            max="100"
            class="progress progress-secondary mx-2"
          ></progress>
          <span class="mr-1">{{ vocabData.data.value.milestone }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
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
