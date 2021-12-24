<template>
  <div
    class="grid items-center p-4 shadow-xl place-items-center flex-shrink-0 col-span-3 row-span-3"
  >
    <div class="avatar mx-auto online">
      <div
        class="w-20 h-20 p-px mask mask-squircle bg-base-content bg-opacity-10"
      >
        <img
          src="https://i.ibb.co/X85vC9M/prof.jpg"
          class="mask mask-squircle"
        />
      </div>
    </div>

    <p class="mx-auto font-bold">Mythaar</p>
    <ul>
      <li v-for="statistic in statistics" :key="statistic.value">
        <span class="text-gray-600">{{ statistic.name }}</span>
        <span class="text-gray-600">{{ statistic.value }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { watch } from "vue";

export default defineComponent({
  props: {
    refreshIt: {
      type: Boolean,
      required: false,
    },
  },
  async setup(props) {
    const { data } = await useAsyncData("fetchstats", () =>
      $fetch("http://127.0.0.1:5000/fetch-statistics")
    );
    const statistics = data.value.statistics;

    watch(
      () => props.refreshIt,
      () => {
        fetch("http://127.0.0.1:5000/fetch-statistics")
          .then((res) => res.json())
          .then((new_info) => {
            for (const i in new_info.statistics) {
              statistics[i].value = new_info.statistics[i].value;
            }
          });
      }
    );

    return {
      statistics,
    };
  },
});
</script>
