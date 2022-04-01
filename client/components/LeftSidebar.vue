<template>
  <div class="h-screen relative">
    <LeftsidebarDailyGrouping @setupAction="emitFurther" />
    <!-- <img src="@/assets/thoughts.svg" class="absolute bottom-0" /> -->
  </div>
</template>

<script>
export default {
  setup(_, { emit }) {
    function emitFurther($event) {
      emit("setupAction", $event);
    }

    return {
      emitFurther,
    };
  },
};
</script>
