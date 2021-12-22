<template>
  <div class="grid grid-cols-3 items-center">
    <div class="chinese text-3xl">{{ data.chengyu.word }}</div>
    <div class="text-xl mx-auto">LingoJot</div>
    <div class="text-right">{{ today }}</div>
  </div>
  <!-- progress bar -->
  <div class="mx-2">
    <div class="w-full stats rounded-none">
      <div class="stat">
        <!-- <div class="stat-value text-lg">4,724/5,000</div>
        <div class="stat-title opacity-100">Vocabulary Size</div> -->
        <div class="stat-desc">
          <progress
            :value="(4724 / 5000) * 100"
            max="100"
            class="progress w-full h-2.5 rounded-xl"
          ></progress>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async setup() {
    const { data } = await useAsyncData("randomchengyu", () =>
      $fetch("http://127.0.0.1:5000/random-chengyu")
    );

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
    };
  },
};
</script>
