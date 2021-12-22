<template>
  <div>
    <!-- Displays the users total history -->
    <p class="mx-auto text-center w-full">Time Breakdown</p>
    <client-only>
      <v-chart class="chart" :option="option" />
    </client-only>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent } from "vue";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

export default defineComponent({
  name: "PieChart",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  async setup() {
    const allLogData = await useAsyncData("allUserData", () =>
      $fetch("http://127.0.0.1:5000/full-historical-breakdown")
    );

    if (allLogData.timeBreakdown === undefined) {
      allLogData.timeBreakdown = [{ value: 0, name: "No Data" }];
    }

    const option = ref({
      title: {
        text: "Time Breakdown",
        left: "center",
        show: false
      },
      tooltip: {
        trigger: "item",
      },
      legend: {
        right: "0%",
      },
      series: [
        {
          name: "Hours spent",
          type: "pie",
          radius: ["50%", "70%"],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: "#fff",
            borderWidth: 2,
          },
          data:
            // [{ value: 1048, name: "Search Engine" }],
            allLogData.timeBreakdown,
        },
      ],
    });

    return { option };
  },
});
</script>

<style scoped>
.chart {
  height: 25vh;
}
</style>
