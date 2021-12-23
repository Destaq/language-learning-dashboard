<template>
  <div>
    <div class="form-control grid grid-cols-3 gap-x-2">
      <div class="col-span-2">
        <input
          type="text"
          class="input input-bordered w-full input-sm"
          placeholder="Title"
          v-model="logTitle"
        />
        <input type="date" v-model="logDate" />
      </div>
      <div>
        <div class="grid grid-cols-2 gap-2 mt-1">
          <select
            class="inline select select-bordered w-full max-w-xs"
            v-model="logType"
          >
            <option disabled selected>Type</option>
            <option>Reading</option>
            <option>Writing</option>
            <option>Speaking</option>
            <option>Listening</option>
            <option>Other</option>
          </select>
          <input
            type="number"
            name="minutes"
            id="minutes"
            v-model="logLength"
            class="inline input input-bordered"
          />
        </div>
        <button
          type="submit"
          class="btn btn-success btn-sm w-full flex mx-auto text-center rounded-sm"
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
      type: Object,
      required: false,
    },
  },
  async setup(props, { emit }) {
    // create the submitCustomLog function, sending the above data to the 127.0.0.1:5000/submit-custom-log route
    var logTitle = ref("");
    var logType = ref("");
    var logLength = ref(0);
    var logDate = ref(new Date().toISOString().slice(0, 10));
    var toggler = ref(true);

    watch(
      () => props.log,
      (value) => {
        if (value) {
          logTitle.value = value.title;
          logType.value = value.type[0].toUpperCase() + value.type.slice(1);
          logLength.value = value.length;
          logDate.value = new Date().toISOString().slice(0, 10);
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
