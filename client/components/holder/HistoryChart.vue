<template>
  <div>
    <div class="grid grid-cols-2">
      <div class="btn-group">
        <!-- left arrow -->
        <button
          class="inline btn btn-xs w-10"
          @click="fetchUserData(null, -1, null)"
        >
          <svg
            class="w-4 h-4 mx-auto"
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
        <!-- right arrow -->
        <button class="btn btn-xs inline w-10" @click="fetchUserData(null, 1)">
          <svg
            class="w-4 h-4 mx-auto"
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
      <button
        class="btn btn-xs btn-secondary w-32 justify-self-end"
        @click="
          isDefaultView = !isDefaultView;
          fetchUserData(null, null, isDefaultView);
        "
      >
        <!-- display by title instead -->
        Switch View
      </button>
    </div>
    <client-only>
      <v-chart
        class="chart mt-2"
        :option="option"
        ref="chart"
        :update-options="{ notMerge: true }"
      />
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
import VChart from "vue-echarts";
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
  props: {
    toggler: {
      type: Boolean,
      required: false,
    },
    theme: {
      type: String,
      required: true,
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
      () => [props.toggler, props.theme],
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
            (new Date().getDay() === 0 ? -6 : 1) // NOTE: changeable here (to -1 for Saturday start; 0=Sunday)
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
              (new Date().getDay() === 0 ? -6 : 1) // NOTE: changeable here (to -1 for Saturday start; 0=Sunday)
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

          emit("updateCorrectKeys", theKeys);

          let temp = prepareOptions(theKeys);

          const cumulativeDataSum = temp[0];
          var cumulativeDataSumSeries = temp[1];
          const allLogDataFinal = temp[2];

          if (cumulativeDataSum.Total.length === 0) {
            // if there is no data, set the total to 0
            cumulativeDataSum.Total = [0, 0, 0, 0, 0, 0, 0];
          }

          // totalShift.value = 0;

          option.value = {
            tooltip: {
              trigger: "axis",
              formatter: function(params) {
                // convert params.value, which is originally a decimal hour value (such as 0.33)
                // into a string of hours:minutes, such as "0:20", as .33 is 1/3 of an hour, which has 60 minutes
                // other examples: 1.5 -> 1:30, 2.20 -> 2.12, 5.75 -> 5:45
                var finalString = `<p class='h-2'>${params[0].axisValueLabel}</p><br>`;
                // loop through element of params
                for (var i = 0; i < params.length; i++) {
                  const hours = Math.floor(params[i].value);
                  var minutes = Math.round((params[i].value - hours) * 60);
                  // now ensure that minutes are always shown to the tens place, so that it is always 2 digits
                  // example: 0:20 -> 0:20, 0:10 -> 0:10, 0:0 -> 0:00
                  minutes = minutes < 10 ? "0" + minutes : minutes;
                  if (params[i].value > 0) {
                    finalString += `${params[i].marker}<span class='mr-16 ml-1'>${params[i].seriesName}</span><strong class="absolute right-2">${hours}h ${minutes}m</strong><br>`;
                  }
                }
                return finalString;
              },
              axisPointer: {
                type: "cross",
                crossStyle: {
                  color: "#999",
                },
              },
            },
            legend: {
              type: "scroll",
              width: "87.5%",
              pageIconColor: props.theme === "dark" ? "#fff" : "#000",
              pageTextStyle: {
                color: props.theme === "dark" ? "#fff" : "#000",
              },
              data: [...theKeys.filter((item) => item !== "Total"), "Sum"],
              textStyle: {
                color: props.theme === "dark" ? "white" : "black",
              },
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
                max: Math.ceil(
                  Math.max(...allLogDataFinal.data.value.information.Total)
                ),
                // automatic does it best
                // interval: Math.ceil(
                //   Math.max(
                //     ...allLogDataFinal.data.value.information.Total
                //   )
                // ) / 5,
                axisLabel: {
                  formatter: "{value} h",
                },
                splitLine: {
                  show: true,
                  lineStyle: {
                    width: 0.5,
                  },
                },
              },
              {
                type: "value",
                name: "Cumulative Hours",
                min: 0,
                max: Math.ceil(
                  parseFloat(cumulativeDataSum.Total.at(-1).toFixed(2))
                ),
                axisLabel: {
                  formatter: "{value} h",
                },
                splitLine: {
                  show: false,
                  lineStyle: {
                    width: 0.5,
                  },
                },
              },
            ],
            series: [
              ...cumulativeDataSumSeries,
              {
                name: "Sum",
                type: "line",
                yAxisIndex: 1,
                data: cumulativeDataSum.Total.map((item) =>
                  parseFloat(item).toFixed(2)
                ),
                smooth: true,
                color: props.theme === "dark" ? "white" : "gray",
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
          };
        });
    }

    // watch correct_keys for changes, and emit those changes
    watch(
      () => theKeys,
      (newValue, oldValue) => {
        if (newValue !== oldValue) {
          emit("updateCorrectKeys", newValue);
        }
      }
    );

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

      // round every item in cumulative data sum to 2 decimal places
      for (const key of correct_keys) {
        cumulativeDataSum[key] = cumulativeDataSum[key].map((item) =>
          parseFloat(item.toFixed(2))
        );
      }

      // same thing for the .data attribute on every element in cumulativeDataSumSeries
      for (const key of correct_keys) {
        cumulativeDataSumSeries.forEach((series) => {
          series.data = series.data.map((item) => parseFloat(item.toFixed(2)));
        });
      }

      return [cumulativeDataSum, cumulativeDataSumSeries, allLogData];
    }

    let response = prepareOptions(theKeys);

    const cumulativeDataSum = response[0];
    const cumulativeDataSumSeries = response[1];
    const allLogDataFinal = response[2];

    emit("updateCorrectKeys", theKeys);

    const option = ref({
      notMerge: true,
      tooltip: {
        trigger: "axis",
        formatter: function(params) {
          // convert params.value, which is originally a decimal hour value (such as 0.33)
          // into a string of hours:minutes, such as "0:20", as .33 is 1/3 of an hour, which has 60 minutes
          // other examples: 1.5 -> 1:30, 2.20 -> 2.12, 5.75 -> 5:45
          var finalString = `<p class='h-2'>${params[0].axisValueLabel}</p><br>`;
          // loop through element of params
          for (var i = 0; i < params.length; i++) {
            const hours = Math.floor(params[i].value);
            var minutes = Math.round((params[i].value - hours) * 60);
            // now ensure that minutes are always shown to the tens place, so that it is always 2 digits
            // example: 0:20 -> 0:20, 0:10 -> 0:10, 0:0 -> 0:00
            minutes = minutes < 10 ? "0" + minutes : minutes;

            if (params[i].value > 0) {
              finalString += `${params[i].marker}<span class='mr-16 ml-1'>${params[i].seriesName}</span><strong class="absolute right-2">${hours}h ${minutes}m</strong><br>`;
            }
          }
          return finalString;
        },
        axisPointer: {
          type: "cross",
          crossStyle: {
            color: "#999",
          },
        },
      },
      legend: {
        type: "scroll",
        width: "87.5%",
        pageIconColor: props.theme === "dark" ? "#fff" : "#000",
        pageTextStyle: {
          color: props.theme === "dark" ? "#fff" : "#000",
        },
        data: [...theKeys.filter((item) => item !== "Total"), "Sum"],
        textStyle: {
          color: props.theme === "dark" ? "white" : "black",
        },
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
          max: Math.ceil(
            Math.max(...allLogDataFinal.data.value.information.Total)
          ),
          // interval: 1,
          axisLabel: {
            formatter: "{value} h",
          },
          splitLine: {
            show: true,
            lineStyle: {
              width: 0.5,
            },
          },
        },
        {
          type: "value",
          name: "Cumulative Hours",
          min: 0,
          max: Math.ceil(parseFloat(cumulativeDataSum.Total.at(-1).toFixed(2))),
          axisLabel: {
            formatter: "{value} h",
          },
          splitLine: {
            show: false,
            lineStyle: {
              width: 0.5,
            },
          },
        },
      ],
      series: [
        ...cumulativeDataSumSeries,
        {
          name: "Sum",
          type: "line",
          yAxisIndex: 1,
          data: cumulativeDataSum.Total.map((item) =>
            parseFloat(item.toFixed(2))
          ),
          smooth: true,
          color: props.theme === "dark" ? "white" : "gray",
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
