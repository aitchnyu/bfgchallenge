<template>
  <div class="container">
    <h1 class="title">Lending Tool</h1>
    <div v-if="!username">
      login screen
    </div>
    <HelloWorld msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
import Buefy from "buefy";
import Vue from "vue";
import "buefy/dist/buefy.css";

import HelloWorld from "./components/HelloWorld.vue";

Vue.use(Buefy);

export default {
  name: "App",
  components: {
    HelloWorld,
  },
  data() {
    return {
      username: null,
      transactions: null,
      loginInput: {
        username: "",
        password: "",
      },
    };
  },
  methods: {},
};
</script>
