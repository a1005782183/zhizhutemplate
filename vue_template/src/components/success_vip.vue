<template>
  <div class="add_vip">
    恭喜您充值成功！
  </div>
</template>

<script>
export default {
    inject: ['reload'],
    data(){
        return{
        }
    },
    // 判断路由
    mounted() {
        console.log(this.$route.query);
        this.$axios.post("/success_vip", this.$route.query)
        .then((res)=>{
            if (res.data.errno == 0) {
                console.log(res.data.errmsg);
            } else {
                console.log(res.data.errmsg);
            }
        }); 
    },
    methods: {
        
    },
}
</script>

<style>

</style>
