<template>
  <div style="margin: 30px 10px;">
    <div v-if="pending">
      <div class="container d-flex justify-content-center" style="height:100vh;">
        <div class="row text-center align-items-center">
          <div class="col">
            <div class="spinner-border text-primary" style="height: 5vh; width: 5vh;" role="status">
            </div>
            <h1 style="margin: 30px 0px 10px 0px;">Fetching tweets...</h1>
            <p>{{ loadMessages[0] }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="container d-flex justify-content-center">
        <div class="row text-center">
          <div class="col text-dark">
            <h1 style="font-weight: bold; margin-bottom: 0px;">Your Top Tweets</h1>
            <p>from the last 365 days.</p>
          </div>
        </div>
      </div>
      <hr style="margin: 0 auto 20px auto; width: 80%; border-color: #ccc;"/>
      <div class="d-flex justify-content-center">
        <div class="row text-center align-items-center">
          <div class="col" style="width: 30%;">
            <button type="button" class="btn" v-on:click="swapTweets('retweets')"
                    v-bind:class="display === 'retweets' ? 'btn-primary' : 'btn-link'"
                    style="height:40px; width: 150px;">
              <font-awesome-icon icon="retweet" aria-hidden="true"/>
              <span style="font-weight:bold;"> Retweets</span>
            </button>
          </div>
          <div class="col">
            <button type="button" class="btn" v-on:click="swapTweets('likes')"
                    v-bind:class="display === 'likes' ? 'btn-primary' : 'btn-link'"
                    style="height:40px; width: 150px;">
              <font-awesome-icon icon="heart" aria-hidden="true"/>
              <span style="font-weight:bold;"> Likes</span>
            </button>
          </div>
        </div>
      </div>
      <div class="container">
        <Tweet v-for="id in tweetIds"
               v-bind:key="id"
               v-bind:id="id"
               v-bind:options="{ align: 'center' }">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"
               style="height: 5vh; width: 5vh; margin-top: 20px;">
          </div>
        </div>
        </Tweet>
      </div>
      <hr style="margin: 20px auto; width: 80%; border-color: #ccc;"/>
      <div class="d-flex justify-content-center" style="font-size:16px;">
        <div class="row align-items-center align-middle"
             style="width: 100%; margin: auto;">
          <div class="col text-right" style="border-right: 1px solid #ccc;">
            <a href="http://github.com/caseyjohnsonwv/stattwist" target="_blank"
               class="text-dark">
              <font-awesome-icon v-bind:icon="['fab', 'github']"/>
              <span style="margin: 0px 10px;">StatTwist</span>
              <img src="../../assets/tornado.png" style="height:1em;">
            </a>
          </div>
          <div class="col text-left" style="border-left: 1px solid #ccc;">
            <a href="http://twitter.com/caseyjohnsonwv/" target="_blank"
               class="text-dark">
              <span style="margin-right: 10px;">Casey J</span>
              <font-awesome-icon v-bind:icon=" ['fab', 'twitter']" class="text-primary"/>
            </a>
          </div>
        </div>
      </div>
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
        'First time loading may take a minute.',
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
    async swapTweets(type) {
      this.display = type;
      await this.renderTweets(this.display);
    },
    updateLoadMessage() {
      const first = this.loadMessages.shift();
      this.loadMessages = this.loadMessages.concat(first);
    },
  },
  async created() {
    await this.getTweetIds();
    await this.renderTweets('retweets');
  },
};
</script>
