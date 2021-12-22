<template>
  <div class="grid grid-cols-12">
    <LeftSidebar @setupAction="eventData = $event" class="col-span-2" />
    <MainHolder class="bg-gray-300 border-r border-l border-black col-span-7" :log="eventData"/>
    <RightSidebar class="col-span-3" />
  </div>
</template>

<script>
export default {
  setup() {
    const eventData = ref(null);

    useMeta({
      htmlAttrs: {
        "data-theme": "light",
      },
    });

    return { eventData };
  },
};
</script>

<style>
@import "./assets/tailwind.css";

@font-face {
  font-family: "Ma Shan Zheng";
  src: local("Ma Shan Zheng"),
    url("/fonts/HanyiSentyScholar.ttf") format("truetype");
}

.chinese {
  font-family: "Ma Shan Zheng";
}
</style>
