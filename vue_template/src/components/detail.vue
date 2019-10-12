<template>
  <div class="detail">
    <div class="panel panel-default" :style="'display: '+dis_show">
    <!-- List group -->
      <ul class="list-group">
        <li class="list-group-item">{{ data.name }}</li>
        <li class="list-group-item"><img :src="http+data.file_name+'/'+data.img" style="width: 800px; height:600px;"></li>
        <li class="list-group-item">{{ data.content }}</li>
        <li id="item" class="list-group-item">
          <div id="all_div">
            <div class="div_btn">
              <button type="button" class="btn btn-primary" @click="iframe_display(data)"><i class="glyphicon glyphicon-eye-open"></i>查看演示</button>
              <p><i class="glyphicon glyphicon-eye-open"></i>{{ data.view_num }}</p>
            </div>
            <div class="div_btn">
              <button v-if='coll_list.indexOf(data.id) != -1' type="button" class="btn btn-warning" @click="collect(data)"><i class="glyphicon glyphicon-star"></i>加入收藏</button>
              <button v-else type="button" class="btn btn-warning" @click="collect(data)"><i class="glyphicon glyphicon-star-empty"></i>加入收藏</button>
              <p><i class="glyphicon glyphicon-star"></i>{{ data.collect_num }}</p>
            </div>
            <div class="div_btn">
              <router-link :to="'/download/'+data.id" class="btn btn-success"><i class="glyphicon glyphicon-download-alt"></i>下载资源</router-link>
              <p><i class="glyphicon glyphicon-download-alt"></i>{{ data.down_num }}</p>
            </div>
          </div>
        </li>
      </ul>
  </div>
  <iframe id="iframes" :style="'display: '+dis_show2"></iframe>
  <button class="btn btn-info col-md-12" type="button" :style="'display: '+dis_show2" @click="change_iframe">返回</button>
  </div>
</template>

<script>
export default {
    inject: ['reload'],
    data(){
        return{
          data: '',
          http: 'http://127.0.0.1:5000/',
          coll_list : [],
          dis_show : '',
          dis_show2 : 'none',
        }
    },
    // 判断路由
    mounted() {
        let id = this.$route.params.id;
        this.$axios.get("/detail?id="+id)
        .then((res)=>{
          this.data = res.data.data;
          console.log(res.data.data);
        });

        // 判断用户收藏模板
        this.$axios.get("/query_coll")
        .then((res)=>{
            this.coll_list = res.data.coll_list;
            console.log(this.coll_list);
        });
    },
    methods: {
        // 收藏模板
        collect: function(data){
            console.log('调用');
            this.$axios.get("/collect?id="+data.id)
            .then((res)=>{
                if (res.data.errno == 0) {
                    console.log(res.data);
                } else {
                    console.log(res.data)
                }
                // 刷新组件
                this.reload();
            }).catch(resp =>{
                alert("请先登录");
            });
        },
        // 设置iframe页面
        iframe_display: function(data){
            this.$axios.get("/get_session")
            .then((res)=>{
                if (res.data.errno == 0) {
                    let src = this.http + data.file_name+'/'+data.file_name+'/index.html';
                    $("#iframes").attr('src', src);
                    document.getElementById('iframes').style.height = window.screen.height +"px"; 
                    document.getElementById('iframes').style.width = window.screen.width+"px"; 
                    $('#iframes').attr('scrolling', 'auto');
                    this.dis_show = 'none';
                    this.dis_show2 = '';
                } else {
                    alert("请先登录");
                }
            }); 
        },
        // 判断显示模板还是iframe
        change_iframe: function(){
            this.dis_show = '';
            this.dis_show2 = 'none';
        },
    }

}
</script>

<style>
.list-group {
  text-align: center;
}
#all_div {
  margin: 0 auto;
}
.div_btn {
  display: inline-block;
  margin: 0 30px;
}
</style>