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
import VChart from "vue-echarts";
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
  props: {
    theme: {
      type: String,
      required: true,
    },
  },
  async setup(props) {
    watch(
      () => props.theme,
      (value) => {
        option.value.title.textStyle.color = value === "dark" ? "#fff" : "#000";
        option.value.legend.textStyle.color =
          value === "dark" ? "#fff" : "#000";
      }
    );

    const option = ref({
      title: {
        text: "Ability Breakdown",
        left: "center",
        show: true,
        top: "0%",
        textStyle: {
          color: props.theme === "dark" ? "#fff" : "#000",
        },
      },
      tooltip: {
        trigger: "axis",
      },
      legend: {
        data: ["Current", "End of 2021", "End of 2020"],
        right: "0%",
        orient: "vertical",
        textStyle: {
          color: props.theme === "dark" ? "#fff" : "#000",
        },
      },
      radar: [
        {
          indicator: [
            { text: "Reading", max: 100 },
            { text: "Listening", max: 100 },
            { text: "Speaking", max: 100 },
            { text: "Writing", max: 100 },
          ],
          radius: "66%",
          center: ["50%", "55%"],
          axisName: {
            padding: [-6, -6, -6, -6], // move closer to the graph
            color: "#888",
          },
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
                /* all in CEFR levels, C2 = 6
                HSK 3 - 1 - A1
                HSK 4 - 2 - A2
                HSK 5 - 3 - B1
                HSK 6 - 4 - B2
                      - 5 - C1
                      - 6 - C2
                */
                Math.round((4.50/ 6) * 100), // reading
                Math.round((4.05 / 6) * 100), // listening
                Math.round((3.25 / 6) * 100), // speaking
                Math.round((2.75 / 6) * 100), // writing (digital)
              ],
              name: "Current",
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
                Math.round((3.8 / 6) * 100),
                Math.round((3.6 / 6) * 100),
                Math.round((2.8 / 6) * 100),
                Math.round((1.9 / 6) * 100),
              ],
              name: "End of 2021",
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
                Math.round((2.2 / 6) * 100),
                Math.round((1.9 / 6) * 100),
                Math.round((1.4 / 6) * 100),
                Math.round((1.2 / 6) * 100),
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
  height: 29vh;
}
</style>
