<template>
  <div>
    <div class="avatar">
      <div class="mb-2 rounded-btn w-24 h-24">
        <img
          src="http://daisyui.com/tailwind-css-component-profile-1@94w.png"
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
