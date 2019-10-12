<template>
    <div id="user_detail_temp">
        <div>
            <ul class="items_detail">
                <li class="item" v-for="data in datas">
                    <div class="pic">
                        <router-link :to="'/detail/'+data.id"><img :src="http+data.file_name+'/'+data.img"></router-link>
                    </div>
                    <div class="pic2">
                        <router-link :to="'/detail/'+data.id" href="">{{ data.name }}</router-link>
                        <span class="show-num"><i class="glyphicon glyphicon-eye-open"></i>{{ data.view_num }}</span>
                    </div>
                </li>
            </ul>
        </div>
    </div>  
</template>

<script>

export default {
    inject: ['reload'],
    data(){
        return{
            path:'',
            datas: '',
            http: 'http://127.0.0.1:5000/',
        }
    },
    // 判断路由
    mounted() {
        this.path = this.$route.path;
        console.log(this.path);
        if (this.path == '/user_detail_collect') {
            this.$axios.get("/user_detail_collect")
            .then((res)=>{
                if (res.data.errno == 0) {
                    console.log(res.data);
                    this.datas = res.data.data;
                } else {
                    console.log(res.data);
                }
            }); 
        };
        if (this.path == '/user_detail_upload') {
            this.$axios.get("/user_detail_upload")
            .then((res)=>{
                if (res.data.errno == 0) {
                    console.log(res.data);
                    this.datas = res.data.data;
                } else {
                    console.log(res.data);
                }
            }); 
        };
        if (this.path == '/user_detail_down') {
            this.$axios.get("/user_detail_down")
            .then((res)=>{
                if (res.data.errno == 0) {
                    console.log(res.data);
                    this.datas = res.data.data;
                } else {
                    console.log(res.data);
                }
            }); 
        };
    },
    methods: {
        
    },
    watch:{
        $route(to,from){
            this.path = to.path;
            // 刷新组件
            this.reload();
        }
    }

}
</script>

<style>
#user_detail_temp {
    margin-top: 20px;
}
li {
    list-style: none;
}

a {
    text-decoration: none;
}

.items_detail li {
    background: #fff;
    border: 1px #d9d9d9 solid;
    float: left;
    padding: 10px 11px 0;
    margin: 10px 30px 15px 0;
}

.items_detail li i {
    margin: 0 3px;
}

.items_detail li img{
    width: 170px;
    height: 130px;
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
</style>
