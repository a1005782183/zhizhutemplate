<template>
  <div class="download">
    <div>
      <div class="down">
        <a><img src="../assets/aa.jpg"></a>
        <p>
          <button type="bottom" v-if='data.is_vip != 1' class="btn btn-primary btn-lg" @click='down_temp'>免费下载</button>
          <button type="bottom" v-else class="btn btn-default btn-lg" @click='down_temp'>VIP下载</button>
        </p>
      </div>
      <a id="vip" download="down"></a>
    </div>
  </div>
</template>

<script>
export default {
    inject: ['reload'],
    data(){
        return{
          data: '',
          http: 'http://127.0.0.1:5000/',
          id: '',
        }
    },
    // 判断路由
    mounted() {
        this.id = this.$route.params.id;
        this.$axios.get("/detail?id="+this.id)
        .then((res)=>{
          this.data = res.data.data;
          console.log(res.data.data);
        });
    },
    methods: {
        down_temp: function(){
          // 添加下载次数
          this.$axios.get("/add_down_num?id="+this.id)
          .then((res)=>{
            if (res.data.errno == 0) {
              alert(res.data.errmsg);
              // 获取用户是否vip并下载
              this.$axios.get("/get_user_vip")
              .then((res)=>{
                $("#vip").attr('href', this.http+this.data.file_name+'/'+this.data.file_name+this.data.file_type);
                if (res.data.errno == 1) {
                  alert(res.data.errmsg);
                  return;
                }
                let user_vip = res.data.user_vip;
                if (this.data.is_vip != 1) {
                  document.getElementById("vip").click();
                } else {
                  if (user_vip != 1) {
                    alert('请先成为VIP');
                    return;
                  }
                  document.getElementById("vip").click();
                }
                $("#vip").attr('href', '');
                
              });
            } else {
              alert(res.data.errmsg);
            }
            
          }).catch(resp =>{
              alert("请先登录");
          });
        }
    }

}
</script>

<style>
.down {
  text-align: center;
  margin: 10%;
}
.down a img{
    width: 270px;
    height: 230px;
    margin-bottom: 20px;
}
</style>