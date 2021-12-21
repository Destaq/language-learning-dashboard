<template>
  <div>
    <p>Quick Actions</p>
    <div v-for="(action, index) in actions" :key="index" class="card mb-4">
      <div class="card-body font-semibold">
        <!-- all with different colors, randomly chosen from fixed list -->
        <div class="text-lg">{{ action.title }}</div>
        <hr class="text-gray-500" />
        <div>
          <div class="text-sm inline">{{ action.text }}</div>
        </div>
      </div>
      <button class="btn btn-primary" @click="setupAction(action)">
        Set
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
