<template>
  <div class="border-t border-b border-opacity-50 border-base-200 px-6 py-4">
    <div class="grid grid-cols-3">
      <p class="font-semibold font-lg inline-flex items-center col-span-2">
        Log Data from File
        <span
          data-tip="Export Pleco flashcards or use custom format"
          class="tooltip tooltip-top font-normal ml-1 inline-block"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
              clip-rule="evenodd"
            />
          </svg>
        </span>
      </p>

      <input
        type="file"
        class="btn btn-sm lowercase hidden"
        @change="handleFileUpload()"
        id="customFile"
        ref="file"
      />
      <input
        type="button"
        value="Browse..."
        class="btn btn-sm"
        onclick="document.getElementById('customFile').click();"
      />
    </div>
  </div>
</template>
<script>
import { ref } from "vue";

export default {
  async setup(_, { emit }) {
    const file = ref(null);

    const handleFileUpload = async () => {
      let formData = new FormData();
      formData.append("file", document.getElementById("customFile").files[0]);
      await fetch("http://127.0.0.1:5000/upload-log-file", {
        method: "POST",
        body: formData,
      });

      document.getElementById("customFile").value = "";

      emit("refreshStats");
    };

    return {
      handleFileUpload,
      file,
    };
  },
};
</script>
