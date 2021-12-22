<template>
  <div>
    <p>Quick Actions</p>
    <div v-for="(action, index) in actions" :key="index" class="card mb-4">
      <button class="btn btn-primary" @click="setupAction(action)">
        {{ action.title }}
      </button>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  async setup(props, { emit }) {
    // a bunch of cards, since these are just things that can be repeated and must be read manually
    const { data } = await useAsyncData("actions", () =>
      $fetch("http://127.0.0.1:5000/possible-daily-actions")
    );

    // create the setupaction emit function
    function setupAction(action,) {
      emit("setupAction", action);
    }

    return {
      actions: data.value.actions,
      setupAction,
    };
  },
});
</script>
