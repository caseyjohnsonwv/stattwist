<template>
  <div class="container">
    <button v-on:click="initiateOAuth" type="button" class="btn btn-primary">
      Login with Twitter
    </button>
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
