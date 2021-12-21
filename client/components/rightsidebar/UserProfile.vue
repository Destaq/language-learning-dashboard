<template>
  <div>
    <div class="avatar">
      <div class="mb-2 rounded-btn w-24 h-24">
        <img
          src="https://i.pinimg.com/736x/64/e0/3c/64e03c70778b113427fb39c4bdbf3b59.jpg"
        />
      </div>
    </div>
    <p>Mythaar</p>
    <ul>
      <li v-for="(statistic, index) in statistics">
        <span class="text-gray-600">{{ statistic.name }}</span>
        <span class="text-gray-600">{{ statistic.value }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  async setup() {
    const { data } = await useAsyncData("fetchlevels", () =>
      $fetch("http://127.0.0.1:5000/fetch-levels")
    );

    if (data.statistics == undefined) {
      return {
        statistics: [],
      };
    }

    return {
      statistics: data.statistics,
    };
  },
};
</script>
