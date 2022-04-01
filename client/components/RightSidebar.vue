<template>
  <div>
    <!-- switch theme icon svg -->
    <button
      class="btn btn-square btn-ghost absolute top-2 right-4"
      v-if="theme === 'garden'"
      @click="switchTheme('dark')"
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
        ></path>
      </svg>
    </button>
    <button
      class="btn btn-square btn-ghost absolute top-2 right-4"
      @click="switchTheme('garden')"
      v-else
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
        ></path>
      </svg>
    </button>
    <!-- sibling component communication -->
    <RightsidebarUserProfile :refreshIt="toggle" class="mt-7" />
    <!-- the below has stats -->
    <RightsidebarStatisticLog @refreshStats="toggle = !toggle" />
    <RightsidebarUserGoals @refreshStats="toggle = !toggle" :theme="theme" />
  </div>
</template>

<script>
import { useCookie } from "#app";
import { watch } from "vue";

export default {
  props: {
    refreshIt: {
      type: Boolean,
    }
  },
  setup(props, { emit }) {
    const toggle = ref(false);
    const theme = useCookie("theme") || "garden";
    function switchTheme(newTheme) {
      theme.value = newTheme;
      emit("newTheme", newTheme);
    }

    watch(
      () => props.refreshIt,
      (_newVal) => {
        toggle.value = !toggle.value;
      }
    );

    return { toggle, theme, switchTheme };
  },
};
</script>
