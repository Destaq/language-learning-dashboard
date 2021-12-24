<template>
  <div class="h-screen font-serif">
    <div
      class="flex items-center bg-cover card bg-base-200 h-full rounded-none justify-evenly"
      id="parent"
    >
      <p class="text-2xl font-serif text-gray-200 font-semibold -mt-3">Quick Actions</p>
      <div
        v-for="(action, index) in actions"
        :key="index"
        class="card glass lg:card-side text-neutral-content shadow-none w-3/4 cursor-pointer"
        @click="setupAction(action)"
      >
        <div class="max-w-md card-body">
          <h2 class="card-title text-center">
            <p>
              {{ action.title }}
            </p>
          </h2>
        </div>
      </div>
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
    function setupAction(action) {
      emit("setupAction", action);
    }

    return {
      actions: data.value.actions,
      setupAction,
    };
  },
});
</script>

<style scoped>
#parent {
  background-image: url("https://www.artranked.com/images/33/333d3d76cb1d93e3844b0a4ee1b0ef95.jpg");
}
</style>
