<template>
  <div>
    <!-- put on the daily chengyu (left-aligned, with the chinese class) and today's date (right-aligned, detailed) -->
    <HolderTopInfo />
    <HolderCustomLog :log="log" />
    <HolderHistoryChart
      @updateStartingDate="starting_date = $event"
      @updatePeriod="period = $event"
    />
    <div class="grid grid-cols-2 -mt-8">
      <HolderPieChart :starting_date="starting_date" :period="period" />
      <HolderLevelsRadar />
    </div>
  </div>
</template>

<script>
export default {
  // get the props
  props: {
    // the data for the custom log
    log: {
      type: Object,
      required: false,
    },
  },
  setup() {
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

    return {
      starting_date,
      period,
    };
  },
};
</script>
