<template>
    <div class="query_template">
        <div class="list-group col-md-2">
            <span class="list-group-item active">模板名称</span>
            <span class="list-group-item active">模板内容</span>
            <span class="list-group-item active">观看次数</span>
            <span class="list-group-item active">是否VIP</span>
            <span class="list-group-item active">下载次数</span>
            <span class="list-group-item active">图片</span>
            <span class="list-group-item active">上传文件名</span>
            <span class="list-group-item active">文件类型</span>
            <span class="list-group-item active">用户</span>
            <span class="list-group-item active">修改</span>
        </div>
        <div class="list-group col-md-2" v-for="(data, i) in datas" :key="i">
            <input type="text" class="list-group-item" v-model="datas[i].name"></input>
            <input type="text" class="list-group-item" v-model="datas[i].content"></input>
            <input type="text" class="list-group-item" v-model="datas[i].view_num"></input>
            <input type="text" class="list-group-item" v-model="datas[i].is_vip"></input>
            <input type="text" class="list-group-item" v-model="datas[i].down_num"></input>
            <input type="text" class="list-group-item" v-model="datas[i].img"></input>
            <input type="text" class="list-group-item" v-model="datas[i].file_name"></input>
            <input type="text" class="list-group-item" v-model="datas[i].file_type"></input>
            <span type="text" class="list-group-item">{{ data.username }}</span>
            <a href="#" class="list-group-item" @click="modify(i)">修改</a>
        </div>
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
                <button class="btn btn-default" type="button" @click="get_pages(skip)">跳转</button>
            </li>
          </ul>
        </nav>
    </div>
</template>

<script>
export default {
    data(){
        return{
            datas: '',
            name : '',
            paginate: '',
            skip: '',
        }
    },
    // 判断路由
    mounted() {
        // 获取文件数据
        this.$axios.get("/query_template")
        .then((res)=>{
            this.datas = res.data.data;
            this.paginate = res.data.paginate;
        });
    },
    methods: {
        modify: function(i) {
            let json_data = JSON.stringify(this.datas[i])
            this.$axios.post("/modify", json_data)
            .then((res)=>{
                console.log(res);
            });   
        },
        get_pages: function(iter) {
            this.$axios.get("/query_template?page="+iter)
            .then((res)=>{
                this.datas = res.data.data;
                this.paginate = res.data.paginate;
                // 跳转框等于当前页
                this.skip = iter;
            });
        },
    }

}
</script>

<style>
.query_template div{
    margin: 0;
    padding: 0;
    margin-top:20px;
}
.page {
    position: absolute;
    bottom: -80px;
    left: auto;
}
input.list-group-item {
    text-align: center;
}
.list-group input{
    height: 50px;
}
.list-group a, .list-group span {
    width: 202px;
}
</style>
