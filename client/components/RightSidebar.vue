<template>
  <div>
    <p class="chinese btn">
      <!-- chinese flag svg -->
      <img src="@/assets/ChineseFlag.svg" width="20" height="20" />
      <span class="text-xl">中文</span>
      <!-- switch icon svg -->
      <svg
        class="w-5 h-5 inline"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
        ></path>
      </svg>
    </p>
    <!-- the below has stats too -->
    <RightSidebarUserProfile />
    <RightSidebarStatisticLog />
    <RightSidebarAllMilestones />
    <!-- image? -->
  </div>
</template>
