<template>
  <div class="container is-max-desktop">
    <h1 class="title">Lending Tool</h1>
    <div v-if="!username">
      <div class="field">
        <label class="label">Username</label>
        <div class="control">
          <input class="input" type="text" v-model="loginInput.username" />
        </div>
      </div>
      <div class="field">
        <label class="label">Password</label>
        <div class="control">
          <input class="input" type="password" v-model="loginInput.password" />
        </div>
      </div>
      <div class="field">
        <div class="control">
          <button @click="login" class="button is-link is-fullwidth">
            Submit
          </button>
        </div>
      </div>
    </div>
    <div v-else>
      <Transactions :username="username" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Buefy from "buefy";
import { SnackbarProgrammatic as Snackbar } from "buefy";
import Vue from "vue";
import "buefy/dist/buefy.css";

import Transactions from "./components/Transactions.vue";

Vue.use(Buefy);

export default {
  name: "App",
  components: {
    Transactions,
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
  methods: {
    async login() {
      const params = new URLSearchParams();
      params.append("username", this.loginInput.username);
      params.append("password", this.loginInput.password);
      const response = await axios.post("http://localhost:8000/login", params);
      if (response.data.status === "fail") {
        Snackbar.open({
          message: "Could not login",
          type: "is-danger",
        });
      } else {
        this.username = this.loginInput.username;
      }
    },
  },
};
</script>
