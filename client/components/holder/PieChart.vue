<template>
  <div>
    <!-- Displays the users total history -->
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
import VChart from "vue-echarts";
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
  props: {
    starting_date: {
      type: String,
      required: true,
    },
    period: {
      type: String,
      required: true,
    },
    isDefaultView: {
      type: Boolean,
      required: true,
    },
    toggler: {
      type: Boolean,
      required: true,
    },
    theme: {
      type: String,
      required: true,
    },
    correctKeys: {
      type: Array,
      required: false,
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
    const tempDefaultView = ref(true);

    const allLogData = await useAsyncData("pieChart", () =>
      $fetch(
        `http://127.0.0.1:5000/historical-breakdown?period=${tempPeriod.value}&starting_date=${tempStartingDate.value}&default_view=${tempDefaultView.value}`
      )
    );

    // now rearrange allData.data.value.time_breakdown, so that the 'name' follows the order of props.correctKeys
    function sortTheData(data) {
      const comparisonArray = props.correctKeys.filter(
        (item) => item !== "Total"
      );

      /*
      Rearrange data so that it follows the order of comparisonArray.

      Example:
      comparisonArray = ['dog', 'cat', 'bug']
      data = [
        {
          name: 'dog',
          value: 10
        },
        {
          name: 'cat',
          value: 20
        },
        {
          name: 'bug',
          value: 30
        },
      ]

      Note how the name attribute of the data is in the same order as it is listed in comparisonArray
      */
      data.sort(function(a, b) {
        return comparisonArray.indexOf(a.name) - comparisonArray.indexOf(b.name);
      });

      return data;
    }

    watch(
      () => [
        props.starting_date,
        props.period,
        props.isDefaultView,
        props.toggler,
        props.theme,
        props.correctKeys,
      ],
      (new_val, _old_val) => {
        tempStartingDate.value = new_val[0];
        tempPeriod.value = new_val[1];
        tempDefaultView.value = new_val[2];
        allLogData.refresh().then(() => {
          allLogData.data.value.time_breakdown = sortTheData(
            allLogData.data.value.time_breakdown
          );
          option.value.series[0].data = allLogData.data.value.time_breakdown;
          option.value.title.textStyle.color =
            props.theme === "dark" ? "white" : "black";
          option.value.legend.textStyle.color =
            props.theme === "dark" ? "white" : "black";
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
        show: true,
        textStyle: { color: props.theme === "dark" ? "white" : "black" },
      },
      tooltip: {
        trigger: "item",
        formatter: "{b}: {c} hrs ({d}%)",
      },
      legend: {
        right: "0%",
        orient: "vertical",
        show: true,
        textStyle: {
          color: props.theme === "dark" ? "white" : "black",
        },
      },
      series: [
        {
          name: "Hours spent",
          type: "pie",
          radius: ["40%", "66%"],
          label: {
            show: false,
            position: "outside",
          },
          // itemStyle: {
          //   borderRadius: 10,
          //   borderColor: "#fff",
          //   borderWidth: 2,
          // },
          center: ["50%", "55%"],
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
  height: 29vh;
}
</style>
