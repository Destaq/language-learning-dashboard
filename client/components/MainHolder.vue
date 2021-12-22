<template>
  <div>
    <!-- put on the daily chengyu (left-aligned, with the chinese class) and today's date (right-aligned, detailed) -->
    <HolderTopInfo />
    <HolderCustomLog :log="log" />
    <HolderHistoryChart />
    <div class="grid grid-cols-2 -mt-8">
      <HolderPieChart />
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
}
</script>
