<template>
  <div style="margin: 30px 10px;">
    <p class="text-center">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Callback',
  data() {
    return {
      message: '',
    };
  },
  methods: {
    completeOAuth() {
      const path = `${process.env.VUE_APP_API_BASE_URL}/auth/callback`;
      const request_token = this.$session.get('request_token');
      const verifier = this.$route.query.oauth_verifier;
      axios.post(path, {
        request_token, verifier,
      }).then((res) => {
        this.$cookie.set('access_token', res.data.access_token, { expires: '12h' });
        this.$cookie.set('access_token_secret', res.data.access_token_secret, { expires: '12h' });
        this.$session.remove('request_token');
        this.message = 'Redirecting...';
        this.$router.push({ name: 'Dashboard' });
      }).catch(() => {
        this.$router.push({ name: 'PageNotFound' });
      });
    },
  },
  created() {
    this.completeOAuth();
  },
};
</script>
