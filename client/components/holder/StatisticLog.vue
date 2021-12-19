<template>
  <input ref="file" v-on:change="handleFileUpload()" type="file" id="customFile" />
</template>
<script>
import { ref } from "vue";

export default {
  async setup() {
    const file = ref(null);

    const handleFileUpload = async () => {
      let formData = new FormData();
      formData.append("file", document.getElementById("customFile").files[0]);
      await fetch("http://127.0.0.1:5000/upload-log-file", {
        method: "POST",
        body: formData,
      });
    };

    return {
      handleFileUpload,
      file,
    };
  },
};
</script>
