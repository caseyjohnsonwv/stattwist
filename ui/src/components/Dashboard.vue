<template>
  <div style="margin: 30px 10px;">
    <div v-if="pending">
      <div class="d-flex justify-content-center">
        <div class="spinner-border text-primary" style="height: 5em; width: 5em;" role="status">
        </div>
      </div>
      <div class="d-flex justify-content-center text-center" style="margin: 30px 0px 10px 0px;">
        <h3>Fetching tweets...</h3>
      </div>
      <div class="d-flex justify-content-center text-center">
        <p>{{ loadMessages[0] }}</p>
      </div>
    </div>
    <div v-else>
      <div class="container text-center">
        <div class="row justify-content-center">
          <div v-on:click="swapTweets('retweets')" class="col btn .btn-block">
            <h1 v-bind:class="display === 'retweets' ? 'text-primary' : ''">RTs</h1>
          </div>
          <div v-on:click="swapTweets('likes')" class="col btn .btn-block">
            <h1 v-bind:class="display === 'likes' ? 'text-primary' : ''">Likes</h1>
          </div>
        </div>
      </div>
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
      loadMessages: [
        'This page will automatically refresh.',
        'Almost there - thanks for waiting.',
      ],
      display: '',
      tweetIds: [],
    };
  },
  mounted() {
    window.setInterval(() => {
      this.updateLoadMessage();
    }, 10000);
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
      this.display = this.display === 'retweets' ? 'likes' : 'retweets';
      await this.renderTweets(this.display);
    },
    updateLoadMessage() {
      const first = this.loadMessages.shift();
      this.loadMessages = this.loadMessages.concat(first);
    },
  },
  async created() {
    this.updateLoadMessage();
    await this.getTweetIds();
    await this.renderTweets('retweets');
  },
};
</script>
