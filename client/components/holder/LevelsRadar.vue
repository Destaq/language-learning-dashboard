<template>
  <div>
    <!-- Displays a graph of the users total hours -->
    <client-only>
      <v-chart class="chart" :option="option" />
    </client-only>
    <!-- <button>Edit</button> -->
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { RadarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent } from "vue";

use([
  CanvasRenderer,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

export default defineComponent({
  name: "LevelsRadar",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  async setup() {
    const option = ref({
      title: {
        text: "Ability Breakdown",
        left: "0%",
      },
      tooltip: {
        trigger: "axis",
      },
      legend: {
        data: ["Current Ability", "End of 2020"],
        right: "0%",
      },
      radar: [
        {
          indicator: [
            { text: "Reading", max: 100 },
            { text: "Listening", max: 100 },
            { text: "Speaking", max: 100 },
            { text: "Writing", max: 100 },
          ],
        },
      ],
      series: [
        {
          type: "radar",
          tooltip: {
            trigger: "item",
          },
          areaStyle: {},
          data: [
            {
              value: [
                Math.round((4 / 6) * 100),
                Math.round((3.7 / 6) * 100),
                Math.round((2.8 / 6) * 100),
                Math.round((2 / 6) * 100),
              ],
              name: "Current Ability",
            },
          ],
        },
        {
          type: "radar",
          tooltip: {
            trigger: "item",
          },
          areaStyle: {},
          data: [
            {
              value: [
                Math.round((2.3 / 6) * 100),
                Math.round((2.1 / 6) * 100),
                Math.round((1.2 / 6) * 100),
                Math.round((1.7 / 6) * 100),
              ],
              name: "End of 2020",
            },
          ],
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
