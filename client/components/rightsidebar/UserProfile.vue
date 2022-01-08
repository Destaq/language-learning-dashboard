<template>
  <div
    class="grid items-center p-4 place-items-center flex-shrink-0 col-span-3 row-span-3"
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
        class="stat w-full p-0 border-none mt-2 select-none"
        v-for="statistic in statistics"
        :key="statistic.value"
      >
        <div class="stat-title text-sm text-center border-none">
          {{ statistic.name }}
          <span
            v-if="
              statistic.name === 'Vocab Size (Words)' ||
                statistic.name === 'Vocab Size (Chars)'
            "
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 inline my-auto mb-0.5 cursor-pointer"
              @click="flipCharsAndWords"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                d="M8 5a1 1 0 100 2h5.586l-1.293 1.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L13.586 5H8zM12 15a1 1 0 100-2H6.414l1.293-1.293a1 1 0 10-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L6.414 15H12z"
              /></svg
          ></span>
        </div>
        <div class="stat-value text-2xl text-center border-none">
          {{ formatStatistic(statistic.name, statistic.value) }}
        </div>
        <!-- <div class="stat-desc text-success text-center font-extrabold">+{{ Math.round(Math.random() * 1000) }}</div> -->
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
    const character_vocab_size = data.value.character_vocab_size;
    const onWords = ref(true);

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

    function flipCharsAndWords() {
      if (onWords.value === true) {
        onWords.value = false;
        statistics[2].value = character_vocab_size;
        statistics[2].name = "Vocab Size (Chars)";

        // duplicate array and reset it to be picked up by engine
        const new_statistics = [...statistics];
        statistics.value = new_statistics;
      } else {
        onWords.value = true;
        statistics[2].value = data.value.word_vocab_size;
        statistics[2].name = "Vocab Size (Words)";

        // duplicate array and reset it to be picked up by engine
        const new_statistics = [...statistics];
        statistics.value = new_statistics;
      }
    }

    function formatStatistic(name, some_number) {
      // if the number is less than one thousand, return the number
      // otherwise, format it to be a decimal with the indicator of degree
      // for example, 1427 = 1.43K, 55000 = 55.0K, 32431000 = 3.24M, etc.
      // go up to the billions
      // always display with three figures, regardless of decimal point placement
      // it will always be rounded to three significant figures
      if (name === "Total Study Time" || name === "Daily Average") {
        // this is an hour value, such as 3.5 -> 3h 30m
        // return formatted as hours and minutes
        const hours = Math.floor(some_number);
        const minutes = Math.floor((some_number - hours) * 60);
        return `${hours}h ${minutes}m`;
      }

      if (some_number < 1000) {
        return some_number;
      } else if (some_number < 1000000) {
        return (some_number / 1000).toPrecision(3) + "K";
      } else if (some_number < 1000000000) {
        return (some_number / 1000000).toPrecision(3) + "M";
      } else if (some_number < 1000000000000) {
        return (some_number / 1000000000).toPrecision(3) + "B";
      } else {
        return (some_number / 1000000000000).toPrecision(3) + "T";
      }
    }

    return {
      statistics,
      character_vocab_size,
      flipCharsAndWords,
      onWords,
      formatStatistic,
    };
  },
});
</script>
