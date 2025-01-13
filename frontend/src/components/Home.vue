<template>
  <div>
    <h3>M1</h3>
    <div> {{ number }}</div>

    <form @submit="submit">
        <input v-model="number" type="number" name="m1" min="0" max="360"></input>
      <button pill v-on:Click="submit" id="button-1" type="submit" variant="dark">Submit</button>
    </form>
  </div>
</template>
<script>
import axios from 'axios';

export default{
  data(){
    return {
      number:0,
      api:{
        m1: 0,
    },
    };
  },
  methods:{
    submit:function(){
    const path = 'http://127.0.0.1:5000/api'
      axios.post(path, {
        m1:this.api.m1,
      }
      )
        .then(response => {
        console.log(response);
        })
        .catch(err =>{
        console.log(err);
        });
    },
  }
}


</script>