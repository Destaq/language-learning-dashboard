<template>
  <div>
    <!-- Displays the users total history -->
    <p class="mx-auto text-center">Time Breakdown</p>
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
import { ref, defineComponent, watch } from "vue";

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
  props: {
    starting_date: {
      type: String,
      required: true,
    },
    period: {
      type: String,
      required: true,
    },
  },
  async setup(props) {
    const tempPeriod = ref("week");
    // set starting date to the closest elapsed monday
    const tempStartingDate = ref(
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

    const allLogData = await useAsyncData("pieChart", () =>
      $fetch(
        `http://127.0.0.1:5000/historical-breakdown?period=${tempPeriod.value}&starting_date=${tempStartingDate.value}`
      )
    );

    watch(
      () => [props.starting_date, props.period],
      (new_val, old_val) => {
        console.log(new_val, old_val);
        tempStartingDate.value = new_val[0];
        tempPeriod.value = new_val[1];
        allLogData.refresh().then(() => {
          option.value.series[0].data = allLogData.data.value.time_breakdown;
        });
      }
    );

    if (allLogData.data.value.time_breakdown === undefined) {
      allLogData.data.value.time_breakdown = [{ value: 0, name: "No Data" }];
    }

    const option = ref({
      title: {
        text: "Time Breakdown",
        left: "center",
        show: false,
      },
      tooltip: {
        trigger: "item",
      },
      legend: {
        right: "0%",
        orient: "vertical",
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
          data: allLogData.data.value.time_breakdown,
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
