<template>
  <div>
    <div v-for="(activity, index) in activities" :key="index">
      {{ activity }}
    </div>
  </div>
</template>

<script>
export default {
  async setup() {
    const { data } = await useAsyncData("fetchactivities", () =>
      $fetch("http://127.0.0.1:5000/fetch-activities")
    );

    return {
      activities: data.activities,
    };
  },
};
</script>
