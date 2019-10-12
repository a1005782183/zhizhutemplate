<template>
    <div id="user_detail">
        <div class="list-group col-md-2 user_group">
            <span href="#" class="list-group-item active">个人信息</span>
            <router-link to="/user_detail_upload" class="list-group-item">我的上传</router-link>
            <router-link to="/user_detail_collect" class="list-group-item">我的收藏</router-link>
            <router-link to="/user_detail_down" class="list-group-item">我的下载</router-link>
            <router-link to="/user_upload_file" class="list-group-item">上传文件</router-link>
            <a class="list-group-item" @click='del_session'>退出用户</a>
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
        },
        del_session() {
            this.$axios.get("/del_session")
            .then((res)=>{
                console.log(res.data.errmsg);
                 window.location.replace("/"); 
            }); 

        }
    }
}

</script>

<style>
.list-group {
     margin-top: 20px;
}
.user_group a, .user_group span {
    padding: 20px;
    text-align: center;
}
</style>
