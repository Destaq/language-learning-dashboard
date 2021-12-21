<template>
  <div>
    <!-- put on the daily chengyu (left-aligned, with the chinese class) and today's date (right-aligned, detailed) -->
    <HolderTopInfo />
    <div class="grid grid-cols-2 gap-2">
      <HolderCustomLog class="inline" />
      <HolderStatisticLog class="inline" />
    </div>
    <HolderHistoryView />
    <div class="grid grid-cols-2 gap-2">
      <HolderPieChart />
      <HolderStackedBarchart />
    </div>
  </div>
</template>
