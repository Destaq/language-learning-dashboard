<template>
  <div>
    <!-- Displays a graph of the users total hours -->
    <client-only>
      <v-chart class="chart" :option="option" />
    </client-only>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent } from "vue";

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

export default defineComponent({
  name: "StackedBarChart",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  async setup() {
    const cumulativeSum = ((sum) => (value) => (sum += value))(0);

    // TODO: support daily, weekly, monthly history
    const allLogData = await useAsyncData("allUserData", () =>
      $fetch("http://127.0.0.1:5000/hours-by-period?period=daily")
    );

    if (allLogData.information === undefined) {
      // random array of data for testing purposes
      allLogData.information = [5, 3, 1, 3.5, 2];
    }

    const cumulativeSumData = allLogData.information.map(cumulativeSum);

    const option = ref({
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "cross",
          crossStyle: {
            color: "#999",
          },
        },
      },
      toolbox: {
        feature: {
          dataView: { show: true, readOnly: false },
          magicType: { show: true, type: ["line", "bar"] },
          restore: { show: true },
          saveAsImage: { show: true },
        },
      },
      legend: {
        data: ["Cumulative Hours", "Hours Spent"],
      },
      xAxis: [
        {
          type: "category",
          // TODO: fix data points
          data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          axisPointer: {
            type: "shadow",
          },
        },
      ],
      yAxis: [
        {
          type: "value",
          name: "Hours Spent",
          min: 0,
          max: Math.max(...allLogData.information) * 1.25,
          interval: Math.max(...allLogData.information) / 5,
          axisLabel: {
            formatter: "{value} h",
          },
        },
        {
          type: "value",
          name: "Cumulative",
          min: 0,
          max: cumulativeSumData.at(-1) * 1.25,
          interval: cumulativeSumData.at(-1) / 5,
          axisLabel: {
            formatter: "{value} h",
          },
        },
      ],
      series: [
        {
          name: "Cumulative",
          type: "line",
          yAxisIndex: 1,
          data: cumulativeSumData,
        },
        {
          name: "Hours Spent in Period",
          type: "bar",
          data: allLogData.information
        },
      ],
    });

    return { option };
  },
});
</script>
