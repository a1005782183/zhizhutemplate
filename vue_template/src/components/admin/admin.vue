<template>
    <div id="admin">
        <div class="list-group col-md-2">
            <a href="#" class="list-group-item active">后台管理</a>
            <router-link to="/upload_file" class="list-group-item">上传模板</router-link>
            <router-link to="/query_template" class="list-group-item">查询模板</router-link>
            <router-link to="/query_user" class="list-group-item">查询用户</router-link>
            <router-link to="/check_file" class="list-group-item">审核上传文件</router-link>
        </div>

        <!-- 中间的 路由 router-view 区域 -->

        <router-view class="col-md-10" v-if="IsRouterAlive"></router-view>
    </div>
</template>

<script>
export default {
    // 刷新组件
    provide() {
        return{
            reload:this.reload
        }
    },
    data() {
        return {
            style:'',
            IsRouterAlive: true
        }
    },
    methods:{
        reload() {
            this.IsRouterAlive = false;
            this.$nextTick(function () {
                this.IsRouterAlive = true;
            })
        }
    }
}

</script>

<style>
.list-group {
     margin-top: 20px;
}
.list-group a, .list-group span {
    height: 50px;
    text-align: center;
}
</style>
