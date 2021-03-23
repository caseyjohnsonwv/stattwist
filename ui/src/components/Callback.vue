<template>
  <div class="container">
    <p>Working...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Callback',
  data() {
    return {};
  },
  methods: {
    completeOAuth() {
      const path = `${process.env.VUE_APP_API_BASE_URL}/auth/callback`;
      const request_token = this.$session.get('request_token');
      const verifier = this.$route.query.oauth_verifier;
      axios.post(path, {
        request_token, verifier,
      }).then((res) => {
        this.$cookie.set('access_token', res.data.access_token, { expires: '1h' });
        this.$cookie.set('access_token_secret', res.data.access_token_secret, { expires: '1h' });
        this.$session.remove('request_token');
        this.$router.push({ name: 'Home' });
      });
    },
  },
  created() {
    this.completeOAuth();
  },
};
</script>
