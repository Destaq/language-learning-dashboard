<template>
  <div>
    <!-- Displays a graph of the users total hours -->
    <button
      class="btn btn-xs inline btn-primary"
      @click="fetchUserData('week', null)"
    >
      Week
    </button>
    <button
      class="btn btn-xs inline btn-primary"
      @click="fetchUserData('month', null)"
    >
      Month
    </button>
    <button
      class="btn btn-xs inline btn-primary"
      @click="fetchUserData('year', null)"
    >
      Year
    </button>
    <!-- left arrow -->
    <button class="inline btn btn-xs" @click="fetchUserData(null, -1)">
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M10 19l-7-7m0 0l7-7m-7 7h18"
        ></path>
      </svg>
    </button>
    <!-- right arrow -->
    <button class="btn btn-xs inline" @click="fetchUserData(null, 1)">
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M14 5l7 7m0 0l-7 7m7-7H3"
        ></path>
      </svg>
    </button>
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
import VChart, {
  LOADING_OPTIONS_KEY,
  THEME_KEY,
  UPDATE_OPTIONS_KEY,
} from "vue-echarts";
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
  name: "HistoryChart",
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

    const period = ref("week");
    const totalShift = ref(0);
    // set starting date to the closest elapsed monday
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

    // NOTE: options: 'week', 'month', 'year'
    const allLogData = await useAsyncData("allUserData", () =>
      $fetch(
        `http://127.0.0.1:5000/hours-by-period?period=${period.value}&starting_date=${starting_date.value}`
      )
    );

    async function fetchUserData(
      newPeriodValue = null,
      startingValueShift = null
    ) {
      // updates if new period value is passed in
      if (newPeriodValue) {
        period.value = newPeriodValue;
        totalShift.value = 0;
      }
      if (period.value === "week") {
        starting_date.value = new Date(
          new Date().setDate(
            new Date().getDate() -
              new Date().getDay() +
              (new Date().getDay() === 0 ? -6 : 1)
          )
        )
          .toISOString()
          .slice(0, 10);
      } else if (period.value === "month") {
        // set the value of starting_date to the first day of the month
        starting_date.value = new Date(new Date().setDate(1))
          .toISOString()
          .slice(0, 10);
      } else if (period.value === "year") {
        // set the value of starting_date to the first day of the first month of the current year
        starting_date.value = new Date(new Date().setMonth(0, 1))
          .toISOString()
          .slice(0, 10);
      }

      // updates if a left-right button is pressed
      if (startingValueShift) {
        totalShift.value += startingValueShift;
        startingValueShift = totalShift.value;
        if (period.value === "week") {
          // move starting_date by startingValueShift weeks
          starting_date.value = new Date(
            new Date(starting_date.value).setDate(
              new Date(starting_date.value).getDate() + startingValueShift * 7
            )
          )
            .toISOString()
            .slice(0, 10);
        } else if (period.value === "month") {
          // move starting_date by startingValueShift months
          starting_date.value = new Date(
            new Date(starting_date.value).setMonth(
              new Date(starting_date.value).getMonth() + startingValueShift
            )
          )
            .toISOString()
            .slice(0, 10);
        } else if (period.value === "year") {
          // move starting_date by startingValueShift years
          starting_date.value = new Date(
            new Date(starting_date.value).setFullYear(
              new Date(starting_date.value).getFullYear() + startingValueShift
            )
          )
            .toISOString()
            .slice(0, 10);
        }
      }
      fetch(
        `http://127.0.0.1:5000/hours-by-period?period=${period.value}&starting_date=${starting_date.value}`
      )
        .then((res) => res.json())
        .then((data) => {
          allLogData.data.value = data;
          const cumulativeDataSum = prepareOptions();

          option.value = {
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
              data: [
                "Reading",
                "Listening",
                "Writing",
                "Speaking",
                "Other",
                "Cumulative Sum",
              ],
            },
            xAxis: [
              {
                type: "category",
                data: allLogData.data.value.dates,
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
                max: Math.max(...allLogData.data.value.information.Total),
                interval:
                  Math.max(...allLogData.data.value.information.Total) / 5,
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
                data: allLogData.data.value.information.Reading,
              },
              {
                name: "Listening",
                type: "bar",
                stack: "total",
                emphasis: {
                  focus: "series",
                },
                data: allLogData.data.value.information.Listening,
              },
              {
                name: "Speaking",
                type: "bar",
                stack: "total",
                emphasis: {
                  focus: "series",
                },
                data: allLogData.data.value.information.Speaking,
              },
              {
                name: "Writing",
                type: "bar",
                stack: "total",
                emphasis: {
                  focus: "series",
                },
                data: allLogData.data.value.information.Writing,
              },
              {
                name: "Other",
                type: "bar",
                stack: "total",
                emphasis: {
                  focus: "series",
                },
                data: allLogData.data.value.information.Other,
              },
            ],
          };
        });
    }

    function prepareOptions() {
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

      Object.keys(allLogData.data.value.information).forEach((key) => {
        cumulativeDataSum[key] = findCumulativeSum(
          allLogData.data.value.information[key]
        );
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

      allLogData.data.value.information.Total = allLogData.data.value.information.Reading.map(
        (reading, i) => {
          return (
            reading +
            allLogData.data.value.information.Speaking[i] +
            allLogData.data.value.information.Listening[i] +
            allLogData.data.value.information.Writing[i] +
            allLogData.data.value.information.Other[i]
          );
        }
      );

      return cumulativeDataSum;
    }

    const cumulativeDataSum = prepareOptions();

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
        data: [
          "Reading",
          "Listening",
          "Writing",
          "Speaking",
          "Other",
          "Cumulative Sum",
        ],
      },
      xAxis: [
        {
          type: "category",
          data: allLogData.data.value.dates,
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
          max: Math.max(...allLogData.data.value.information.Total),
          interval: Math.max(...allLogData.data.value.information.Total) / 5,
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
          data: allLogData.data.value.information.Reading,
        },
        {
          name: "Listening",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.data.value.information.Listening,
        },
        {
          name: "Speaking",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.data.value.information.Speaking,
        },
        {
          name: "Writing",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.data.value.information.Writing,
        },
        {
          name: "Other",
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.data.value.information.Other,
        },
      ],
    });

    return { option, fetchUserData, starting_date, period, allLogData, totalShift };
  },
});
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>
