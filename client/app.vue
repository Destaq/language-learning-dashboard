<template>
  <div class="grid grid-cols-12">
    <LeftSidebar @setupAction="eventData = $event" class="col-span-2" />
    <MainHolder
      class="col-span-7"
      :log="eventData"
      :theme="theme"
    />
    <RightSidebar class="col-span-3" @newTheme="theme = $event" />
  </div>
</template>

<script>
import { useCookie } from "#app";

export default {
  setup() {
    const eventData = ref(null);

    const theme = useCookie("theme") || "garden";

    useMeta({
      htmlAttrs: {
        "data-theme": theme,
      },
    });

    return { eventData, theme };
  },
};
</script>

<style>
@import "./assets/tailwind.css";

@font-face {
  font-family: "Ma Shan Zheng";
  src: local("Ma Shan Zheng"),
    url("/fonts/FZKai.ttf") format("truetype");
}

.chinese {
  font-family: "Ma Shan Zheng";
}
</style>
