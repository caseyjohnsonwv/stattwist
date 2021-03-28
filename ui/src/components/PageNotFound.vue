<template>
  <div class="container d-flex justify-content-center">
    <div class="row text-center align-items-center" style="height:100vh;">
      <div class="col">
        <img src="../../assets/tornado.png" style="width:150px;">
        <h1 style="margin: 10px 0px;">Whoops!</h1>
        <p style="margin-bottom: 30px">I have a feeling we're not in Kansas anymore...</p>
        <p>(This page doesn't exist.)</p>
        <button v-on:click="goHome" type="button" class="btn btn-large btn-primary">
          <p style="margin: auto; padding: 5px; font-weight: bold;">
            Take Me Home
          </p>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageNotFound',
  data() {
    return {};
  },
  methods: {
    goHome() {
      this.$router.push({ name: 'Dashboard' });
    },
  },
};
</script>
