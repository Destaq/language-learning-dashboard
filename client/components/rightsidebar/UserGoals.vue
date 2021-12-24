<template>
  <div>
    <p>Weekly Goals</p>
    <div v-for="(goal, index) in goals" :key="index" class="card">
      <div
        class="card-body font-semibold"
        :class="new Date(goal.deadline) < new Date() ? 'bg-red-500' : ''"
      >
        <!-- strikethrough and increase opacity if completed -->
        <div :class="goal.completed ? 'line-through' : ''">
          <input
            type="checkbox"
            class="checkbox checkbox-sm"
            @change="editGoalMessage(goal)"
            v-model="goal.completed"
          />
          <div class="text-sm inline">{{ goal.description }}</div>
          <div class="text-sm inline">
            {{ new Date(goal.deadline).toDateString() }}
          </div>
        </div>
        <label
          :for="'manage-goal-modal-' + goal.id"
          class="btn btn-primary modal-button"
          >Edit</label
        >
        <input
          type="checkbox"
          :id="'manage-goal-modal-' + goal.id"
          class="modal-toggle"
        />
        <div class="modal">
          <div class="modal-box">
            <div class="form-control">
              <label class="label">
                <span class="label-text">Description</span>
              </label>
              <input
                type="text"
                placeholder="...some goal"
                v-model="goal.tempDescription"
                class="input input-bordered"
              />
              <label for="start">Deadline:</label>
              <input
                type="date"
                id="start"
                name="trip-start"
                v-model="goal.tempDeadline"
                :min="new Date().toISOString().split('T')[0]"
              />
            </div>
            <div class="modal-action">
              <label
                :for="'manage-goal-modal-' + goal.id"
                class="btn btn-error"
                @click="deleteGoalMessage(goal)"
              >
                Delete</label
              >
              <label
                :for="'manage-goal-modal-' + goal.id"
                class="btn btn-primary"
                @click="editGoalMessage(goal)"
                >Edit</label
              >
              <label
                :for="'manage-goal-modal-' + goal.id"
                class="btn"
                @click="
                  goal.tempDeadline = goal.deadline;
                  goal.tempDescription = goal.description;
                "
                >Cancel</label
              >
            </div>
          </div>
        </div>
      </div>
    </div>
    <label for="new-goal-modal" class="btn btn-primary modal-button"
      >New Goal</label
    >
    <input type="checkbox" id="new-goal-modal" class="modal-toggle" />
    <div class="modal">
      <div class="modal-box">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Description</span>
          </label>
          <input
            type="text"
            placeholder="...some goal"
            v-model="newGoalDescription"
            class="input input-bordered"
          />
          <label for="start">Deadline:</label>
          <input
            type="date"
            id="start"
            name="trip-start"
            v-model="newGoalDeadline"
            :min="new Date().toISOString().split('T')[0]"
          />
        </div>
        <div class="modal-action">
          <label
            for="new-goal-modal"
            class="btn btn-primary"
            @click="createNewGoalMessage"
            >Create</label
          >
          <label for="new-goal-modal" class="btn">Cancel</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async setup(_, { emit }) {
    // probably going to be in checklist format
    const { data } = await useAsyncData("weeklychecklist", () =>
      $fetch("http://127.0.0.1:5000/weekly-goals")
    );

    if (data.value == undefined) {
      data.value = {
        goals: [],
      };
    }

    // sortUndone is a function that sorts the goals, setting those which have completed to be true to the at the bottom
    const sortUndone = (goals) => {
      for (const [key, value] of Object.entries(goals)) {
        goals[key].deadline = new Date(value.deadline)
          .toISOString()
          .split("T")[0];
        goals[key].tempDescription = value.description;
        goals[key].tempDeadline = value.deadline;
      }
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

    var goals = ref(sortUndone(Object.values(data.value.goals)));
    const newGoalDeadline = ref("");
    const newGoalDescription = ref("");

    async function editGoalMessage(goalObject) {
      fetch("http://127.0.0.1:5000/edit-goal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: goalObject.id,
          description: goalObject.tempDescription,
          deadline: goalObject.tempDeadline,
          completed: goalObject.completed,
        }),
      })
        .then(() => {
          goalObject.description = goalObject.tempDescription;
          goalObject.deadline = goalObject.tempDeadline;
          goals.value = sortUndone(Object.values(goals.value)); // rearrange if ticked

          // update user profile
          emit("refreshStats")
        })
        .catch((err) => {
          console.log(err);
        });
    }

    async function createNewGoalMessage() {
      fetch("http://127.0.0.1:5000/submit-new-goal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          description: newGoalDescription.value,
          deadline: newGoalDeadline.value,
        }),
      })
        .then(() => {
          fetch("http://127.0.0.1:5000/weekly-goals")
            .then((response) => response.json())
            .then((newInfo) => {
              goals.value = sortUndone(Object.values(newInfo.goals));
            });
        })
        .catch((err) => {
          console.log(err);
        });
    }

    async function deleteGoalMessage(goal) {
      fetch("http://127.0.0.1:5000/delete-goal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: goal.id,
        }),
      })
        .then(() => {
          goals.value = goals.value.filter(
            (innerGoal) => innerGoal.id !== goal.id
          );
        })
        .catch((err) => {
          console.log(err);
        });
    }

    return {
      goals,
      newGoalDeadline,
      newGoalDescription,
      createNewGoalMessage,
      editGoalMessage,
      deleteGoalMessage,
    };
  },
};
</script>
