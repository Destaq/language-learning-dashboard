<template>
  <div>
    <div v-for="(milestone, index) in milestones" :key="index">
      {{ milestone }}
    </div>
  </div>
</template>

<script>
export default {
  async setup() {
    const { data } = await useAsyncData("fetchmilestones", () =>
      $fetch("http://127.0.0.1:5000/fetch-milestones")
    );

    return {
      milestones: data.milestones,
    };
  },
};
</script>
