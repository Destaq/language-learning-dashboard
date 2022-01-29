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
        return (
          comparisonArray.indexOf(a.name) - comparisonArray.indexOf(b.name)
        );
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
          // allLogData.data.value.time_breakdown = allLogData.data.value.time_breakdown.sort(
          //   function(a, b) {
          //     return b.value - a.value;
          //   }
          // );
          option.value.series[0].data = allLogData.data.value.time_breakdown;
          option.value.title.textStyle.color =
            props.theme === "dark" ? "white" : "black";
          option.value.legend.textStyle.color =
            props.theme === "dark" ? "white" : "black";
          option.value.legend.pageIconColor =
            props.theme === "dark" ? "white" : "black";
          option.value.legend.pageTextStyle.color =
            props.theme === "dark" ? "white" : "black";
        });
      }
    );

    if (allLogData.data.value.time_breakdown === undefined) {
      allLogData.data.value.time_breakdown = [{ value: 0, name: "No Data" }];
    }

    // sort allLogData.data.value.time_breakdown by their values descending
    // allLogData.data.value.time_breakdown = allLogData.data.value.time_breakdown.sort(
    //   function(a, b) {
    //     return b.value - a.value;
    //   }
    // );
    // issue: does not retain colors

    const option = ref({
      title: {
        text: "Time Breakdown",
        left: "center",
        show: true,
        textStyle: { color: props.theme === "dark" ? "white" : "black" },
      },
      tooltip: {
        trigger: "item",
        // formatter: "{b}: {c} hrs ({d}%)"
        formatter: function(params) {
          // convert params.value, which is originally a decimal hour value (such as 0.33)
          // into a string of hours:minutes, such as "0:20", as .33 is 1/3 of an hour, which has 60 minutes
          // other examples: 1.5 -> 1:30, 2.20 -> 2.12, 5.75 -> 5:45
          const hours = Math.floor(params.value);
          var minutes = Math.round((params.value - hours) * 60);

          // now ensure that minutes are always shown to the tens place, so that it is always 2 digits
          // example: 0:20 -> 0:20, 0:10 -> 0:10, 0:0 -> 0:00
          minutes = minutes < 10 ? "0" + minutes : minutes;
          return `${params.marker}<span class='mr-3 ml-1'>${params.name}</span><strong>${hours}h ${minutes}m (${params.percent}%)</strong>`;
        },
      },
      legend: {
        right: "0%",
        orient: "vertical",
        type: "scroll",
        pageIconColor: props.theme === "dark" ? "#fff" : "#000",
        pageTextStyle: {
          color: props.theme === "dark" ? "#fff" : "#000",
        },
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
      color: [
        "#5470c6",
        "#91cc75",
        "#fac858",
        "#ee6666",
        "#73c0de",
        "#3ba272",
        "#fc8452",
        "#9a60b4",
        "#E8BEAC", // new
        "#ea7ccc",
        "#B87333", // new
        "#778899", // new
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
