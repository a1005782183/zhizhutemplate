<template>
  <div class="add_vip">
    <button type="button" class="btn btn-primary" @click="add_vip">200元加入VIP</button>
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
        
    },
    methods: {
        add_vip: function(){
                this.$axios.get("/add_vip")
                .then((res)=>{
                    if (res.data.errno == 0) {
                        location.href = res.data.data;
                    } else {
                        console.log(res.data.errmsg);
                    }
                }); 
                this.reload();
            },
    }
}
</script>

<style>

</style>
