<template>
  <div class="h-64 overflow-y-auto">
    <p class="text-lg font-semibold text-center mt-2">Goals</p>
    <div v-for="(goal, index) in goals" :key="index" class="card rounded-none">
      <div
        class="card-body font-semibold py-1 rounded-none grid grid-cols-12"
        :class="
          new Date(goal.deadline) < new Date()
            ? 'alert alert-error bg-base-100'
            : ''
        "
      >
        <!-- strikethrough and increase opacity if completed -->
        <div
          class="form-control col-span-11 grid grid-cols-12"
          :class="goal.completed ? 'line-through' : ''"
        >
          <input
            type="checkbox"
            class="checkbox checkbox-sm self-end"
            @change="editGoalMessage(goal)"
            v-model="goal.completed"
          />
          <div class="grid col-span-11 self-end grid-cols-4">
            <span
              class="label-text inline ml-3 col-span-3 truncate whitespace-nowrap"
              >{{ goal.description }}</span
            >
            <div class="text-sm inline-flex">
              <span class="inline-block font-normal ml-2">{{
                new Date(goal.deadline).toLocaleString("default", {
                  month: "short",
                }) +
                  " " +
                  new Date(goal.deadline).getDate()
              }}</span>
            </div>
          </div>
        </div>
        <label
          :for="'manage-goal-modal-' + goal.id"
          class="modal-button inline cursor-pointer ml-4 text-base-content"
          ><svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 inline"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
            /></svg
        ></label>
        <input
          type="checkbox"
          :id="'manage-goal-modal-' + goal.id"
          class="modal-toggle inline"
        />
        <div class="modal">
          <div class="modal-box">
            <div class="form-control">
              <label class="label">
                <span class="label-text font-normal">Description</span>
              </label>
              <input
                type="text"
                placeholder="...some goal"
                v-model="goal.tempDescription"
                class="input input-bordered"
              />
              <label class="label">
                <span class="label-text font-normal">Deadline</span>
              </label>
              <input
                type="date"
                id="start"
                name="trip-start"
                v-model="goal.tempDeadline"
                class="input input-bordered"
                :class="theme === 'dark' ? 'invertIconModal' : ''"
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
    <label
      for="new-goal-modal"
      class="btn btn-primary modal-button text-white absolute bottom-0 btn-sm w-3/12 rounded-none"
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5 mr-1.5"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
          clip-rule="evenodd"
        /></svg
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
          <label class="label">
            <span class="label-text">Deadline</span>
          </label>
          <input
            type="date"
            v-model="newGoalDeadline"
            class="input input-bordered w-full inline-block"
            :class="theme === 'dark' ? 'invertIconModal' : ''"
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
          <label
            for="new-goal-modal"
            class="btn"
            @click="
              newGoalDeadline = '';
              newGoalDescription = '';
            "
            >Cancel</label
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    theme: {
      type: String,
      required: true,
    },
  },
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
          emit("refreshStats");
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
              newGoalDeadline.value = "";
              newGoalDescription.value = "";
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

<style scoped>
input.invertIconModal::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
</style>
