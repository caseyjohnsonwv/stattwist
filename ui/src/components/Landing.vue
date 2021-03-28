<template>
  <div class="container d-flex justify-content-center">
    <div class="row text-center align-items-center" style="height:100vh;">
      <div class="col">
        <img src="../../assets/tornado.png" style="width:50%;">
        <h1 style="margin: 10px 0px 30px 0px;">StatTwist</h1>
        <button v-on:click="initiateOAuth" type="button" class="btn btn-large btn-primary">
          <p style="margin: auto; padding: 5px; font-weight: bold;">
            Login with Twitter
          </p>
        </button>
        <p style="margin: 30px 0px 10px 0px">
          Made <a href="http://github.com/caseyjohnsonwv/stattwist" target="_blank">with love</a> in Pittsburgh.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Landing',
  data() {
    return {};
  },
  methods: {
    initiateOAuth() {
      const path = `${process.env.VUE_APP_API_BASE_URL}/auth`;
      const access_token = this.$cookie.get('access_token');
      const access_token_secret = this.$cookie.get('access_token_secret');
      if (access_token === null || access_token_secret === null) {
        axios.get(path)
          .then((res) => {
            this.$session.set('request_token', res.data.request_token);
            window.location.href = res.data.redirect_url;
          });
      } else {
        this.$router.push({ name: 'Dashboard' });
      }
    },
  },
};
</script>
