<template>
  <div class="grid grid-cols-12">
    <LeftSidebar @setupAction="eventData = $event; eventDataToggler = !eventDataToggler" class="col-span-2" />
    <MainHolder
      class="col-span-7"
      :log="[eventData, eventDataToggler]"
      :theme="theme"
      @refreshCharts="statUpdateToggler = !statUpdateToggler"
    />
    <RightSidebar class="col-span-3" @newTheme="theme = $event" :refreshIt="statUpdateToggler" />
  </div>
</template>

<script>
import { useCookie } from "#app";

export default {
  setup() {
    const eventData = ref(null);
    var eventDataToggler = ref(false);

    const theme = useCookie("theme");
    if (theme.value === undefined) {
      theme.value = "garden";
    }
    const statUpdateToggler = ref(true);

    useMeta({
      htmlAttrs: {
        "data-theme": theme,
      },
      title: "Chinese Learning Dashboard"
    });

    return { eventData, theme, statUpdateToggler, eventDataToggler };
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
