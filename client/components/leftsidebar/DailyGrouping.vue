<template>
  <div>
    <p>Daily Actions</p>
    <div v-for="daily in dailies" :key="daily" class="card">
      <div class="card-body font-semibold">
        <!-- all with different colors, randomly chosen from fixed list -->
        <div class="text-lg">{{ daily.title }}</div>
        <hr class="text-gray-500" />
        <div>
          <div class="text-sm inline">{{ daily.description }}</div>
        </div>
        <!-- The below is for the number of minutes -->
        <div class="form-control">
          <label for="minutes">Minutes:</label>
          <input type="number" id="minutes" name="minutes" min="1" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async setup() {
    // a bunch of cards, since these are just things that can be repeated
    const { data } = await useAsyncData("dailies", () =>
      $fetch("http://localhost:5000/possible-daily-actions")
    );

    return {
      dailies: data.dailies,
    };
  },
};
</script>
