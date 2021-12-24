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

    <p class="mx-auto font-bold mt-2 text-xl mb-2">Mythaar</p>
    <div class="grid grid-cols-2 w-full">
      <div
        class="stat w-full p-0 border-none mt-2"
        v-for="statistic in statistics"
        :key="statistic.value"
      >
        <div class="stat-title text-sm text-center border-none">{{ statistic.name }}</div>
        <div class="stat-value text-2xl text-center border-none">{{ statistic.value }}</div>
      </div>
    </div>
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
