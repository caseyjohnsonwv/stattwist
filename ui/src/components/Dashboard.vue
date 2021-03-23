<template>
  <div v-if="pending" class="container">
    <p>Loading...</p>
  </div>
  <div v-else class="container">
    <p>{{ data }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
  data() {
    return {
      pending: true,
      data: null,
    };
  },
  methods: {
    async loadTweets() {
      const path = `${process.env.VUE_APP_API_BASE_URL}/dashboard/load`;
      const access_token = this.$cookie.get('access_token');
      const access_token_secret = this.$cookie.get('access_token_secret');
      const response = await axios.post(path, { access_token, access_token_secret });
      // eslint-disable-next-line
      console.log(response.data);
      this.pending = false;
      this.data = response.data;
    },
  },
  async created() {
    await this.loadTweets();
  },
};
</script>
