<template>
    <div class="check_file">
        <div class="list-group col-md-2">
            <span class="list-group-item active">模板名</span>
            <span class="list-group-item active">内容</span>
            <span class="list-group-item active">是否VIP</span>
            <span class="list-group-item active">图片</span>
            <span class="list-group-item active">文件名</span>
            <span class="list-group-item active">用户</span>
            <span class="list-group-item active">同意</span>
            <span class="list-group-item active">不同意</span>
        </div>
        <div class="list-group col-md-2" v-for="data in datas">
            <span class="list-group-item">{{data.name}}</span>
            <span class="list-group-item">{{data.content}}</span>
            <span class="list-group-item">{{data.down_type}}</span>
            <span class="list-group-item">{{data.img}}</span>
            <span class="list-group-item">{{data.file_name}}</span>
            <span class="list-group-item">{{data.username}}</span>
            <a class="list-group-item" @click='agree_file'>同意</a>
            <a class="list-group-item" @click='no_agree_file'>不同意</a>
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
    inject: ['reload'],
    data(){
        return{
            datas: '',
            paginate: '',
            skip: '',
        }
    },
    mounted() {
        // 获取文件数据
        this.$axios.get("/query_file")
        .then((res)=>{
            console.log(res.data);
            this.datas = res.data.data;
            this.paginate = res.data.paginate;
        });
    },
    methods: {
        // 同意文件上传
        agree_file: function() {
            this.$axios.post("/agree_file", this.datas)
            .then((res)=>{
                console.log(res.data.errmsg);
                // 刷新组件
                this.reload();
            });
        },
        // 不同意文件上传
        no_agree_file: function() {
            this.$axios.post("/no_agree_file", this.datas)
            .then((res)=>{
                console.log(res.data.errmsg);
                // 刷新组件
                this.reload();
            });
        },
        // 分页
        get_pages: function(iter) {
            this.$axios.get("/query_file?page="+iter)
            .then((res)=>{
                this.datas = res.data.data;
                this.paginate = res.data.paginate;
                // 跳转框等于当前页
                this.skip = iter;
            });
        },
    },
}
</script>

<style>
.check_file div{
    margin: 0;
    padding: 0;
    margin-top:20px;
}
.page {
    position: absolute;
    bottom: -80px;
    left: auto;
}

</style>
