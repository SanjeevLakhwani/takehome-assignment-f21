<template>
  <div>
    <p>Count: {{ init }}</p>
    <button v-on:click="init++">+</button>
    <button v-on:click="init--">-</button>
  </div>
</template>

<script>
export default {
  props: { init: Number }
};
</script>

<style></style>
