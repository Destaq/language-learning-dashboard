<template>
  <div>
    <p>Weekly Goals</p>
    <div v-for="(goal, index) in goals" :key="index" class="card">
      <div class="card-body font-semibold">
        <!-- strikethrough and increase opacity if completed -->
        <div :class="goal.completed ? 'line-through' : ''">
          <input type="checkbox" class="checkbox checkbox-sm" />
          <div class="text-sm inline">{{ goal.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async setup() {
    // probably going to be in checklist format
    const { data } = await useAsyncData("weeklychecklist", () =>
      $fetch("http://127.0.0.1:5000/weekly-goals")
    );

    if (data.goals === undefined) {
      data.goals = [];
    }
    // sortUndone is a function that sorts the goals, setting those which have completed to be true to the at the bottom
    const sortUndone = (goals) => {
      return goals.sort((a, b) => {
        if (a.completed === true && b.completed === false) {
          return 1;
        } else if (a.completed === false && b.completed === true) {
          return -1;
        } else {
          return 0;
        }
      });
    };

    return {
      goals: sortUndone(data.goals),
    };
  },
};
</script>
