<template>
  <div>
    <!-- put on the daily chengyu (left-aligned, with the chinese class) and today's date (right-aligned, detailed) -->
    <div class="flex justify-between items-center">
      <div class="chinese text-3xl">{{ chengyu }}</div>
      <div class="text-right">{{ today }}</div>
    </div>
    <!-- progress bar -->
    <div class="m-2">
      <div class="w-full stats rounded-none">
        <div class="stat bg-light-300">
          <div class="stat-value text-lg">4,724/5,000</div>
          <div class="stat-title opacity-100">Vocabulary Size</div>
          <div class="stat-desc">
            <progress
              :value="(4724 / 5000) * 100"
              max="100"
              class="progress"
            ></progress>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    const chengyu = ref("总体上说"); // TODO: fetch chengyu from backend

    // get today in the format: "Monday, January 1, 2020"
    const today = new Date().toLocaleDateString("en-US", {
      weekday: "long",
      month: "long",
      day: "numeric",
      year: "numeric",
    });

    return {
      chengyu,
      today,
    };
  },
};
</script>
