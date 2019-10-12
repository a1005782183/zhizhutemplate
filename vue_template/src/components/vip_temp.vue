<template>
  <div class="vip_temp">
    <div :style="'display: '+dis_show">
      <ul class="items">
        <li class="item" v-for="data in datas">
            <div class="pic">
                <router-link :to="'/detail/'+data.id"><img :src="http+data.file_name+'/'+data.img"></router-link>
                <a v-if='coll_list.indexOf(data.id) != -1' class="item-collect" @click="collect(data)"><i class="glyphicon glyphicon-star"></i>收藏</a>
                <a v-else class="item-collect" @click="collect(data)"><i class="glyphicon glyphicon-star-empty"></i>收藏</a>
                <router-link :to="'/download/'+data.id" class="item-down"><i class="glyphicon glyphicon-download-alt"></i>下载</router-link>
                <a class="item-show" @click="iframe_display(data)"><i class="glyphicon glyphicon-eye-open"></i>预览</a>
            </div>
            <div class="pic2">
                <router-link :to="'/detail/'+data.id" href="">{{ data.name }}</router-link>
                <span class="show-num"><i class="glyphicon glyphicon-eye-open"></i>{{ data.view_num }}</span>
            </div>
        </li>
      </ul>
      <!-- 清除浮动 -->
      <div style="clear:both"></div>
        <!-- 分页 -->
        <nav aria-label="Page navigation" class="page">
          <ul class="pagination">
            <li><span>当前页:{{ paginate.page }}</span></li>
            <li v-if='paginate.has_prev'>
              <a aria-label="Previous"  @click="get_pages(paginate.prev_num)">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>

            <li v-for='iter in paginate.iter_pages' v-if="iter != '...'">
                <a @click="get_pages(iter)">{{iter}}</a>
            </li>
            <li v-else>
                <span>{{iter}}</span>
            </li>
            
            <li v-if='paginate.has_next'>
              <a aria-label="Next" @click="get_pages(paginate.next_num)">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
            <li><span>总页数:{{ paginate.pages }}</span></li>
            <li>
                <input type="text" class="col-md-1" style='height:34px;' v-model='skip' v-on:keyup.enter="get_pages(skip)">
                <button class="btn btn-default col-md-2" type="button" @click="get_pages(skip)">跳转</button>
            </li>
          </ul>
        </nav>
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
            http: 'http://127.0.0.1:5000/',
            datas: '',
            paginate: '',
            skip: '',
            dis_show : '',
            dis_show2 : 'none',
            coll_list : [],
        }
    },
    // 判断路由
    mounted() {
        this.$axios.get("/query_vip_temp")
        .then((res)=>{
            this.datas = res.data.data;
            this.paginate = res.data.paginate;
            console.log(this.datas);
        });
        // 判断用户收藏模板
        this.$axios.get("/query_coll")
        .then((res)=>{
            this.coll_list = res.data.coll_list;
            console.log(this.coll_list);
        });
    },
    methods: {
        // 请求模板数据
        get_pages: function(iter) {
            this.$axios.get("/query_all_temp?page="+iter)
            .then((res)=>{
                this.datas = res.data.data;
                this.paginate = res.data.paginate;
                // 跳转框等于当前页
                this.skip = iter;
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
        // 收藏模板
        collect: function(data){
            console.log('调用');
            this.$axios.get("/collect?id="+data.id)
            .then((res)=>{
                if (res.data.errno == 0) {
                    console.log(res.data);
                } else {
                    alert('请先登录');
                }
                // 刷新组件
                this.reload();
            }).catch(resp =>{
                alert("请先登录");
            });
        }
    }

}
</script>

<style>
    li {
        list-style: none;
    }

    a {
        text-decoration: none;
    }

    .items li {
        background: #fff;
        border: 1px #d9d9d9 solid;
        float: left;
        padding: 10px 11px 0;
        margin: 10px 30px 15px 0;
    }

    .items li i {
        margin: 0 3px;
    }

    .items li img{
        width: 270px;
        height: 230px;
    }

    .pic {
        position: relative;
        text-align: center;
    }

    .item-show {
        width: 62px;
        height: 32px;
        line-height: 32px;
        background: #f6f6f6;
        position: absolute;
        right: 0;
        bottom: 0px;
        color: #05920a;
        cursor:pointer;
    }
    .item-collect {
        width: 62px;
        height: 32px;
        line-height: 32px;
        background: #f6f6f6;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0px;
        color: #05920a;
        cursor:pointer;
    }
    .item-down {
        width: 62px;
        height: 32px;
        line-height: 32px;
        background: #f6f6f6;
        position: absolute;
        left: 0;
        bottom: 0px;
        color: #05920a;
        cursor:pointer;
    }
    .item-down:hover, .item-show:hover, .item-collect:hover  {
        background-color: #0B0;
    }

    .pic2 {
        position: relative;
        height: 30px;
    }

    .show-num {
        line-height: 32px;
        position: absolute;
        right: 0px;
    }
    .pic2 a {
        line-height: 32px;
        text-decoration: none;
        color: #000;
        cursor:pointer;
    }
    .pic a {
        text-decoration: none;
    }
    .pic2 a:hover {
        color: blue;
    }
    .page {
        margin:0px auto;
        text-align: center;
    }

    .pagination li a {
        text-align: center;
        width: 50px;
    }

</style>
