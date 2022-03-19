<template>
  <div class="bg-base-200 px-4">
    <!-- put on the daily chengyu (left-aligned, with the chinese class) and today's date (right-aligned, detailed) -->
    <HolderTopInfo :theme="theme" />
    <HolderCustomLog :log="log" @refreshCharts="refreshAndPropagate" :theme="theme" class="mt-1" />
    <!-- NOTE: toggler is used for when there is a new log added -->
    <div class="my-4"></div>
    <HolderHistoryChart
      @updateStartingDate="starting_date = $event"
      @updatePeriod="period = $event"
      @updateDefaultView="isDefaultView = $event"
      @updateCorrectKeys="correctKeys = $event"
      :toggler="toggler"
      :theme="theme"
    />
    <div class="grid grid-cols-2 -mt-8">
      <HolderPieChart :starting_date="starting_date" :correctKeys="correctKeys" :isDefaultView="isDefaultView" :period="period" :toggler="toggler" :theme="theme" />
      <HolderLevelsRadar :theme="theme" />
    </div>
  </div>
</template>

<script>
export default {
  // get the props
  props: {
    // the data for the custom log
    log: {
      type: Array,
      required: false,
    },
    theme: {
      type: String,
      required: true,
    },
  },
  setup(_props, { emit }) {
    const starting_date = ref(
      new Date(
        new Date().setDate(
          new Date().getDate() -
            new Date().getDay() +
            (new Date().getDay() === 0 ? -6 : 1)
        )
      )
        .toISOString()
        .slice(0, 10)
    );
    const period = ref("week");
    const isDefaultView = ref(true);
    const toggler = ref(true);
    const correctKeys = ref([]);

    function refreshAndPropagate($event) {
      toggler.value = $event;
      emit("refreshCharts");
    }

    return {
      starting_date,
      period,
      toggler,
      isDefaultView,
      refreshAndPropagate,
      correctKeys
    };
  },
};
</script>
