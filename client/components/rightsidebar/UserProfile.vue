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
      <li>Reading: {{ levels.reading }} [edit]</li>
      <li>Listening: {{ levels.listening }} [edit]</li>
      <li>Speaking: {{ levels.speaking }} [edit]</li>
      <li>Writing: {{ levels.writing }} [edit]</li>
    </ul>
  </div>
</template>

<script>
export default {
  async setup() {
    const { data } = await useAsyncData("fetchlevels", () =>
      $fetch("http://127.0.0.1:5000/fetch-levels")
    );

    if (data.value == undefined) {
      return {
        levels: {
          reading: "",
          listening: "",
          speaking: "",
          writing: "",
        },
      };
    }

    return {
      levels: data.levels,
    };
  },
};
</script>
