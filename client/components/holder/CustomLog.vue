<template>
  <div>
    <p>Custom Log</p>
    <div class="form-control">
      <label class="label">
        <span class="label-text">Title</span>
      </label>
      <input type="text" class="input input-bordered" v-model="logTitle" />
      <label class="label">
        <span class="label-text">Description</span>
      </label>
      <textarea
        class="input input-bordered h-20"
        cols="30"
        rows="10"
        v-model="logDescription"
      ></textarea>
      <select class="select select-bordered w-full max-w-xs" v-model="logType">
        <option disabled selected>Type</option>
        <option>Reading</option>
        <option>Writing</option>
        <option>Speaking</option>
        <option>Listening</option>
      </select>

      <label for="minutes">Length: </label>
      <input type="number" name="minutes" id="minutes" v-model="logLength" />
      <button type="submit" class="btn btn-success" @click="submitCustomLog">
        Submit
      </button>
    </div>
  </div>
</template>

<script>
export default {
  async setup() {
    // create the submitCustomLog function, sending the above data to the 127.0.0.1:5000/submit-custom-log route
    var logTitle = ref("");
    var logDescription = ref("");
    var logType = ref("");
    var logLength = ref("");

    async function submitCustomLog() {
      fetch("http://127.0.0.1:5000/submit-custom-log", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          logTitle: logTitle.value,
          logDescription: logDescription.value,
          logType: logType.value,
          logLength: logLength.value,
        }),
      })
        .then(() => {
          // clear all values
          logTitle.value = "";
          logDescription.value = "";
          logType.value = "";
          logLength.value = "";
        })
        .catch((err) => {
          console.log(err);
        });
    }

    return {
      submitCustomLog,
      logTitle,
      logDescription,
      logType,
      logLength,
    };
  },
};
</script>
