<template>
  <div>
    <table class="table">
      <thead>
        <tr>
          <th>Debtor</th>
          <th>Debtee</th>
          <th>Amount</th>
          <th>Reason</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction of transactions" :key="transaction.id">
          <td>{{ transaction.debtor }}</td>
          <td>{{ transaction.debtee }}</td>
          <td>{{ transaction.amount }}</td>
          <td>{{ transaction.reason }}</td>
          <td>
            <span v-if="transaction.is_repaid" class="tag is-primary is-medium"
              >Paid</span
            >
            <span v-else>
              <button @click="markPaid(transaction)" class="button">Pay</button>
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { SnackbarProgrammatic as Snackbar } from "buefy";

export default {
  name: "AppTransactions",
  props: {
    username: String,
  },
  async mounted() {
    const response = await axios.get("http://localhost:8000/get_transactions", {
      params: { username: this.username },
    });
    this.transactions = response.data.data.transactions;
  },
  methods: {
    async markPaid(transaction) {
      const params = new URLSearchParams();
      params.append("transaction_id", transaction.id);
      const response = await axios.post(
        "http://localhost:8000/mark_paid",
        params
      );
      if (response.data.status === "success") {
        Snackbar.open({
          message: "Transaction is paid off",
        });
        transaction.is_repaid = true;
      }
    },
  },
  data() {
    return {
      transactions: [],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
