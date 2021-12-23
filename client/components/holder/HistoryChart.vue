<template>
  <div>
    <div>
      <!-- Displays a graph of the users total hours -->
      <button
        class="btn btn-xs inline btn-primary"
        @click="fetchUserData('week', null, null)"
      >
        Week
      </button>
      <button
        class="btn btn-xs inline btn-primary"
        @click="fetchUserData('month', null, null)"
      >
        Month
      </button>
      <button
        class="btn btn-xs inline btn-primary"
        @click="fetchUserData('year', null, null)"
      >
        Year
      </button>
      <button
        class="btn btn-xs inline btn-secondary"
        @click="
          isDefaultView = !isDefaultView;
          fetchUserData(null, null, isDefaultView);
        "
      >
        <!-- display by title instead -->
        Switch View
      </button>
      <!-- left arrow -->
      <button class="inline btn btn-xs" @click="fetchUserData(null, -1, null)">
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
    </div>
    <client-only>
      <v-chart class="chart mt-4" :option="option" ref="chart" :update-options="{ notMerge: true }" />
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
import { ref, defineComponent, watch } from "vue";

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
  props: {
    toggler: {
      type: Boolean,
      required: false,
    },
  },
  async setup(props, { emit }) {
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

    watch(
      () => props.toggler,
      (_value) => {
        // there was a new log uploaded
        // refresh this data accordingly
        fetchUserData();
      }
    );

    const chart = ref(null);
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
    const isDefaultView = ref(true); // showing the types (e.g. listening, speaking), instead of the titles

    // NOTE: options: 'week', 'month', 'year'
    const allLogData = await useAsyncData("allUserData", () =>
      $fetch(
        `http://127.0.0.1:5000/hours-by-period?period=${period.value}&starting_date=${starting_date.value}&default_view=${isDefaultView.value}`
      )
    );

    // get all the keys (e.g. listening, speaking) from allLogData
    var theKeys = Object.keys(allLogData.data.value.information);

    async function fetchUserData(
      newPeriodValue = null,
      startingValueShift = null,
      newIsDefaultView = null
    ) {
      if (newIsDefaultView !== null) {
        isDefaultView.value = newIsDefaultView;
      }

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

      emit("updateStartingDate", starting_date.value);
      emit("updatePeriod", period.value);
      emit("updateDefaultView", isDefaultView.value);

      fetch(
        `http://127.0.0.1:5000/hours-by-period?period=${period.value}&starting_date=${starting_date.value}&default_view=${isDefaultView.value}`
      )
        .then((res) => res.json())
        .then((data) => {
          allLogData.data.value = data;

          var theKeys = Object.keys(allLogData.data.value.information);
          let temp = prepareOptions(theKeys);

          const cumulativeDataSum = temp[0];
          var cumulativeDataSumSeries = temp[1];
          const allLogDataFinal = temp[2];

          if (cumulativeDataSum.Total.length === 0) {
            // if there is no data, set the total to 0
            cumulativeDataSum.Total = [0, 0, 0, 0, 0, 0, 0];
          }

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
                ...theKeys.filter((item) => item !== "Total"),
                "Cumulative Sum",
              ],
            },
            xAxis: [
              {
                type: "category",
                data: allLogDataFinal.data.value.dates,
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
                max: parseFloat(
                  Math.max(
                    ...allLogDataFinal.data.value.information.Total
                  ).toFixed(3)
                ),
                interval: parseFloat(
                  (
                    parseFloat(
                      Math.max(
                        ...allLogDataFinal.data.value.information.Total
                      ).toFixed(3)
                    ) / 5
                  ).toFixed(3)
                ),
                axisLabel: {
                  formatter: "{value} h",
                },
              },
              {
                type: "value",
                name: "Cumulative Hours",
                min: 0,
                max: parseFloat(cumulativeDataSum.Total.at(-1).toFixed(3)),
                interval: parseFloat(
                  (
                    parseFloat(cumulativeDataSum.Total.at(-1).toFixed(3)) / 5
                  ).toFixed(3)
                ),
                axisLabel: {
                  formatter: "{value} h",
                },
              },
            ],
            series: [
              ...cumulativeDataSumSeries,
              {
                name: "Cumulative Sum",
                type: "line",
                yAxisIndex: 1,
                data: cumulativeDataSum.Total,
              },
            ],
          };
          // const newSeries = [
          //   ...cumulativeDataSumSeries,
          //   {
          //     name: "Cumulative Sum",
          //     type: "line",
          //     yAxisIndex: 1,
          //     data: cumulativeDataSum.Total,
          //   },
          // ];
          // chart.setOption({series: newSeries}, { replaceMerge: ['series']});
        });
    }

    function prepareOptions(correct_keys) {
      // create a cumulative sum of reading, speaking, listening, writing, and other from the above data
      // in the format: {
      //   Reading: [5, 8, 9, 12.5, 14.5],
      //   Speaking: [5, 8, 10, 12, 15],
      //   ...
      // }
      const cumulativeDataSum = {
        Total: [],
      };

      for (const key of correct_keys) {
        cumulativeDataSum[key] = [];
      }

      /* 
      Create list of below such objects:
      {
        name: Key,
        type: "bar",
        stack: "total",
        emphasis: {
          focus: "series",
        },
          data: allLogData.data.value.information.Key,
      }
      for every key in correct_keys
      */
      var cumulativeDataSumSeries = correct_keys.map((key) => {
        return {
          name: key,
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series",
          },
          data: allLogData.data.value.information[key],
        };
      });

      // remove whichever object in cumulativeDataSumSeries that has a name of "Total"
      cumulativeDataSumSeries = cumulativeDataSumSeries.filter(
        (series) => series.name !== "Total"
      );

      Object.keys(allLogData.data.value.information).forEach((key) => {
        cumulativeDataSum[key] = findCumulativeSum(
          allLogData.data.value.information[key]
        );
      });

      // now get the total for each day
      // e.g. [5, 8, 10, 12, 15], [5, 8, 10, 12, 15] -> [10, 18, 20, 24, 30]
      /*
      We start with an object like this:
      {
        key1: [5, 8, 9, 12.5, 14.5],
        key2: [5, 8, 10, 12, 15],
        ...
      }

      We want to add up all arrays in the object into one array
      [10, 16, 19, 24.5, 29.5]

      The output array should be the same length as the input ones!
      */
      function sumArrays(...arrays) {
        try {
          const n = arrays.reduce((max, xs) => Math.max(max, xs.length), 0);
          const result = Array.from({ length: n });
          return result.map((_, i) =>
            arrays.map((xs) => xs[i] || 0).reduce((sum, x) => sum + x, 0)
          );
        } catch {
          return [];
        }
      }

      let inputArrays = [];
      for (const key of correct_keys.filter((item) => item !== "Total")) {
        inputArrays.push(cumulativeDataSum[key]);
      }

      cumulativeDataSum.Total = sumArrays(...inputArrays);

      // clear inputArrays
      inputArrays = [];
      // repeat for allLogData.data.value.information
      for (const key of correct_keys.filter((item) => item !== "Total")) {
        inputArrays.push(allLogData.data.value.information[key]);
      }

      allLogData.data.value.information.Total = sumArrays(...inputArrays);

      return [cumulativeDataSum, cumulativeDataSumSeries, allLogData];
    }

    let response = prepareOptions(theKeys);

    const cumulativeDataSum = response[0];
    const cumulativeDataSumSeries = response[1];
    const allLogDataFinal = response[2];

    const option = ref({
      notMerge: true,
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
        data: [...theKeys.filter((item) => item !== "Total"), "Cumulative Sum"],
      },
      xAxis: [
        {
          type: "category",
          data: allLogDataFinal.data.value.dates,
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
          max: parseFloat(
            Math.max(...allLogDataFinal.data.value.information.Total).toFixed(3)
          ),
          interval:
            Math.max(...allLogDataFinal.data.value.information.Total).toFixed(
              2
            ) / 5,
          axisLabel: {
            formatter: "{value} h",
          },
        },
        {
          type: "value",
          name: "Cumulative Hours",
          min: 0,
          max: parseFloat(cumulativeDataSum.Total.at(-1).toFixed(3)),
          interval: parseFloat(
            (parseFloat(cumulativeDataSum.Total.at(-1).toFixed(3)) / 5).toFixed(
              3
            )
          ),
          axisLabel: {
            formatter: "{value} h",
          },
        },
      ],
      series: [
        ...cumulativeDataSumSeries,
        {
          name: "Cumulative Sum",
          type: "line",
          yAxisIndex: 1,
          data: cumulativeDataSum.Total,
        },
      ],
    });

    return {
      option,
      fetchUserData,
      starting_date,
      period,
      allLogData,
      totalShift,
      isDefaultView,
      chart,
    };
  },
});
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>
