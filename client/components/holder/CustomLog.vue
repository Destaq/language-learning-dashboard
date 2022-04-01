<template>
  <div class="card shadow-lg bg-base-100 rounded-md">
    <div
      class="form-control grid grid-cols-2 gap-x-4 card-body rounded-md py-4 px-4"
    >
      <div class="grid grid-rows-2 items-center gap-2">
        <input
          type="text"
          class="input input-bordered w-full input-xs"
          placeholder="Log Title"
          v-model="logTitle"
        />
        <input
          type="date"
          v-model="logDate"
          class="input input-bordered input-xs w-full inline-block"
          :id="theme === 'dark' ? 'invertIcon' : ''"
        />
      </div>
      <div class="grid grid-rows-2 gap-2 items-center">
        <div class="grid grid-cols-2 gap-2 items-center">
          <select
            class="inline select select-xs select-bordered w-full max-w-xs"
            v-model="logType"
          >
            <option disabled="disabled" selected="selected">Type</option>
            <option>Reading</option>
            <option>Writing</option>
            <option>Speaking</option>
            <option>Listening</option>
            <option>Flashcards</option>
            <option>Other</option>
          </select>
          <input
            type="number"
            name="minutes"
            id="minutes"
            v-model="logLength"
            class="inline input input-bordered input-xs"
          />
        </div>
        <button
          type="submit"
          class="btn btn-primary btn-xs w-full flex mx-auto text-center rounded-lg text-primary-content"
          @click="submitCustomLog"
        >
          Submit Custom Log
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { watch, defineComponent } from "vue";

export default defineComponent({
  props: {
    // the data for the custom log
    log: {
      type: Array,
      required: false,
    },
    // the theme for the custom log
    theme: {
      type: String,
      required: false,
      default: "garden",
    },
  },
  async setup(props, { emit }) {
    // create the submitCustomLog function, sending the above data to the 127.0.0.1:5000/submit-custom-log route
    var logTitle = ref("");
    var logType = ref("Type");
    var logLength = ref(0);
    var logDate = ref(new Date().toISOString().slice(0, 10));
    var toggler = ref(true);

    watch(
      () => props.log,
      (value) => {
        if (value) {
          try {
            logTitle.value = value[0].title;
            logType.value =
              value[0].type[0].toUpperCase() + value[0].type.slice(1);
            logLength.value = value[0].length;
            logDate.value = new Date().toISOString().slice(0, 10);
          } catch (error) {
            // Cannot read properties of null (reading 'title')
            // ignore here to let app run smoothly
          }
        }
      }
    );

    async function submitCustomLog() {
      fetch("http://127.0.0.1:5000/submit-custom-log", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: logTitle.value,
          type: logType.value,
          length: logLength.value,
          date: logDate.value,
        }),
      })
        .then(() => {
          // clear all values
          logTitle.value = "";
          logType.value = "";
          logLength.value = "";
          logDate.value = new Date().toISOString().slice(0, 10);

          // emit the event to refresh the charts
          toggler.value = !toggler.value;
          emit("refreshCharts", toggler.value);
        })
        .catch((err) => {
          console.log(err);
        });
    }

    return {
      submitCustomLog,
      logTitle,
      logType,
      logLength,
      logDate,
      toggler,
    };
  },
});
</script>

<style scoped>
input#invertIcon::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
</style>
