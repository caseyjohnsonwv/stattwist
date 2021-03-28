<template>
  <div style="margin: 30px 10px;">
    <div v-if="pending">
      <div class="d-flex justify-content-center">
        <div class="spinner-border text-primary" style="height: 5em; width: 5em;" role="status">
        </div>
      </div>
      <div class="d-flex justify-content-center text-center" style="margin: 30px 0px 10px 0px;">
        <h3>Fetching tweets... this may take a moment.</h3>
      </div>
      <div class="d-flex justify-content-center text-center">
        <p>This page will automatically refresh.</p>
      </div>
    </div>
    <div v-else>
      <h1 class="text-center">Your Top Tweets</h1>
      <Tweet v-for="id in tweetIds"
             v-bind:key="id"
             v-bind:id="id"
             v-bind:options="{ align: 'center' }">
      <div class="d-flex justify-content-center" style="margin: 10px 0px;">
        <div class="spinner-border text-primary" role="status"></div>
      </div>
      </Tweet>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Tweet } from 'vue-tweet-embed';

export default {
  name: 'Dashboard',
  components: {
    Tweet,
  },
  data() {
    return {
      pending: true,
      display: '',
      tweetIds: [],
    };
  },
  methods: {
    async getTweetIds() {
      const access_token = this.$cookie.get('access_token');
      const access_token_secret = this.$cookie.get('access_token_secret');
      if (access_token === null || access_token_secret === null) {
        this.$router.push({ name: 'Landing' });
      }
      const most_retweeted_ids = this.$cookie.get('most_retweeted_ids');
      const most_liked_ids = this.$cookie.get('most_liked_ids');
      if (most_retweeted_ids === null || most_liked_ids === null) {
        const path = `${process.env.VUE_APP_API_BASE_URL}/dashboard/load`;
        const response = await axios.post(path, { access_token, access_token_secret });
        this.$cookie.set('most_retweeted_ids', JSON.stringify(response.data.most_retweeted_ids), { expires: '12h' });
        this.$cookie.set('most_liked_ids', JSON.stringify(response.data.most_liked_ids), { expires: '12h' });
      }
    },
    async renderTweets(type) {
      this.pending = true;
      this.display = type;
      this.tweetIds = (type === 'retweets')
        ? JSON.parse(this.$cookie.get('most_retweeted_ids'))
        : JSON.parse(this.$cookie.get('most_liked_ids'));
      this.pending = false;
    },
    async swapTweets() {
      return true;
    },
  },
  async created() {
    await this.getTweetIds();
    await this.renderTweets('retweets');
  },
};
</script>
