<template>
  <div>
    <!-- Displays a graph of the users total hours -->
    <button>Week</button>
    <button>Month</button>
    <button>Year</button>
    <button>Custom Calendar</button>
    <client-only>
      <v-chart class="chart mt-4" :option="option" />
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
import VChart, { LOADING_OPTIONS_KEY, THEME_KEY } from "vue-echarts";
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
  name: "HistoryView",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  async setup() {
    const findCumulativeSum = (arr) => {
      const creds = arr.reduce(
        (acc, val) => {
          let { sum, res } = acc;
          sum += val;
          res.push(sum);
          return { sum, res };
        },
        {
          sum: 0,
          res: [],
        }
      );
      return creds.res;
    };

    // TODO: support daily, weekly, monthly history
    const allLogData = await useAsyncData("allUserData", () =>
      $fetch("http://127.0.0.1:5000/hours-by-period?period=daily") // TODO: improve
    );

    if (allLogData.information === undefined) {
      // random array of data for testing purposes
      allLogData.information = {
        Reading: [5, 3, 1, 3.5, 2],
        Speaking: [5, 3, 1, 3.5, 2],
        Listening: [5, 3, 1, 3.5, 2],
        Writing: [5, 3, 1, 3.5, 2],
        Other: [5, 3, 1, 3.5, 2],
        Total: []
      };
    }

    // create a cumulative sum of reading, speaking, listening, writing, and other from the above data
    // in the format: {
    //   Reading: [5, 8, 9, 12.5, 14.5],
    //   Speaking: [5, 8, 10, 12, 15],
    //   ...
    // }
    const cumulativeDataSum = {
      Reading: [],
      Speaking: [],
      Listening: [],
      Writing: [],
      Other: [],
      Total: [],
    };

    Object.keys(allLogData.information).forEach((key) => {
      cumulativeDataSum[key] = findCumulativeSum(allLogData.information[key]);
    });

    // now get the total for each day
    // e.g. [5, 8, 10, 12, 15], [5, 8, 10, 12, 15] -> [10, 18, 20, 24, 30]
    cumulativeDataSum.Total = cumulativeDataSum.Reading.map((reading, i) => {
      return (
        reading +
        cumulativeDataSum.Speaking[i] +
        cumulativeDataSum.Listening[i] +
        cumulativeDataSum.Writing[i] +
        cumulativeDataSum.Other[i]
      );
    });


    allLogData.information.Total = allLogData.information.Reading.map((reading, i) => {
      return (
        reading +
        allLogData.information.Speaking[i] +
        allLogData.information.Listening[i] +
        allLogData.information.Writing[i] +
        allLogData.information.Other[i]
      );
    });

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
        data: ["Reading", "Listening", "Writing", "Speaking", "Other", "Cumulative Sum"],
      },
      xAxis: [
        {
          type: "category",
          data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          axisPointer: {
            type: "shadow",
          },
        },
      ],
      yAxis: [
        {
          type: "value",
          name: "Period Hours",
          min: 0,
          max: Math.max(...allLogData.information.Total),
          interval: Math.max(...allLogData.information.Total) / 5,
          axisLabel: {
            formatter: "{value} h",
          },
        },
        {
          type: "value",
          name: "Cumulative Hours",
          min: 0,
          max: cumulativeDataSum.Total.at(-1),
          interval: cumulativeDataSum.Total.at(-1) / 5,
          axisLabel: {
            formatter: "{value} h",
          },
        },
      ],
      series: [
        {
          name: "Cumulative Sum",
          type: "line",
          yAxisIndex: 1,
          data: cumulativeDataSum.Total,
        },
        {
          name: "Reading",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.information.Reading,
        },
        {
          name: "Listening",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.information.Listening,
        },
        {
          name: "Speaking",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.information.Speaking,
        },
        {
          name: "Writing",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.information.Writing,
        },
        {
          name: "Other",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.information.Other,
        },
      ],
    });

    return { option };
  },
});
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>
