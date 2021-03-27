<template>
  <div v-if="pending" class="container">
    <p>Loading...</p>
  </div>
  <div v-else class="container">
    <h1>Most Retweeted</h1>
    <p><span v-for="tweet in most_retweeted_tweets" :key="tweet" v-html="tweet"></span></p>
    <h1>Most Liked</h1>
    <p><span v-for="tweet in most_liked_tweets" :key="tweet" v-html="tweet"></span></p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
  data() {
    return {
      pending: true,
      most_retweeted_tweets: [],
      most_liked_tweets: [],
    };
  },
  methods: {
    async getTweetIds() {
      const most_retweeted_ids = this.$cookie.get('most_retweeted_ids');
      const most_liked_ids = this.$cookie.get('most_liked_ids');
      if (most_retweeted_ids === null || most_liked_ids === null) {
        // eslint-disable-next-line
        console.log("API CALL");
        const path = `${process.env.VUE_APP_API_BASE_URL}/dashboard/load`;
        const access_token = this.$cookie.get('access_token');
        const access_token_secret = this.$cookie.get('access_token_secret');
        const response = await axios.post(path, { access_token, access_token_secret });
        this.$cookie.set('most_retweeted_ids', response.data.most_retweeted_ids, { expires: '4h' });
        this.$cookie.set('most_liked_ids', response.data.most_liked_ids, { expires: '4h' });
      }
    },
    async renderTweets() {
      const path = `${process.env.VUE_APP_API_BASE_URL}/dashboard/render`;
      const access_token = this.$cookie.get('access_token');
      const access_token_secret = this.$cookie.get('access_token_secret');
      const most_retweeted_ids = this.$cookie.get('most_retweeted_ids');
      const most_liked_ids = this.$cookie.get('most_liked_ids');
      const response = await axios.post(path, {
        access_token, access_token_secret, most_retweeted_ids, most_liked_ids,
      });
      this.most_retweeted_tweets = response.data.most_retweeted_cards;
      this.most_liked_tweets = response.data.most_liked_cards;
      this.pending = false;
    },
  },
  async created() {
    await this.getTweetIds();
    await this.renderTweets();
  },
};
</script>
