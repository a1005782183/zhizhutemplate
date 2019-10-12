<template>
  <div id="app">
    <div class="row" v-if="!(router_list.indexOf(path) != -1)">
		<ul class="navbar navbar-inverse navbar-default navbar-fixed-top">
			<router-link to="/index" class="btn btn-primary btn-lg col-md-1" role="button">首页</router-link>
			<router-link to="/not_vip_temp"class="btn btn-default btn-lg col-md-1" role="button">免费模板</router-link>
			<router-link to="/vip_temp" class="btn btn-default btn-lg col-md-1" role="button">VIP模板</router-link>
			<router-link to="/add_vip" class="btn btn-default btn-lg col-md-1" role="button" v-if="is_vip==0">加入VIP</router-link>
			<router-link to="/success_vip" class="btn btn-default btn-lg col-md-1" role="button" v-else>加入VIP</router-link>
		</ul>
		<ul class="register" v-if="username == ''">
			<li class="col-md-2" data-target="#register_Modal" data-toggle="modal"><a>注册</a></li>
			<li class="col-md-2" data-target="#login_Modal" data-toggle="modal"><a>登录</a></li>
		</ul>
		<ul class="register col-md-2" v-else>
			<li class="col-md-2"><router-link to="/user_detail">{{ username }}</router-link></li>
		</ul>
		<div class="input-group col-md-3">
	         <input type="text" class="form-control" v-model="search" @keyup.enter="click_search" />
	         <a @click="click_search" class="input-group-addon"><i class="glyphicon glyphicon-search"></i></a>
	    </div>
		<!-- 注册模态框 -->
	    <div class="modal fade" id="register_Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		    <div class="modal-dialog">
		        <div class="modal-content">
		            <div class="modal-header">
		                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
		                <h4 class="modal-title" id="myModalLabel">注册页面</h4>
		            </div>
		            <div class="modal-body">
						<div style="width: 200px;margin: 0 auto;">
					        <form>
								  <div class="form-group">
								    <label for="register_username">用户名：</label>
								    <input type="text" class="form-control" id="register_username" placeholder="username">
								  </div>
								  <div class="form-group">
								    <label for="register_password">密码：</label>
								    <input type="password" class="form-control" id="register_password" placeholder="password">
								  </div>
								  <button type="submit" class="btn btn-default" @click='register'>提交</button>
							</form>
			    		</div>	
		            </div>
		            <div class="modal-footer">
		                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
		            </div>
		        </div>
		    </div>
		</div>
		<!-- 登录模态框 -->
	    <div class="modal fade" id="login_Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		    <div class="modal-dialog">
		        <div class="modal-content">
		            <div class="modal-header">
		                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
		                <h4 class="modal-title" id="myModalLabel">登录页面</h4>
		            </div>
		            <div class="modal-body">
						<div style="width: 200px;margin: 0 auto;">
					        <form>
								  <div class="form-group">
								    <label for="login_username">用户名：</label>
								    <input type="text" class="form-control" id="login_username" placeholder="username">
								  </div>
								  <div class="form-group">
								    <label for="login_password">密码：</label>
								    <input type="password" class="form-control" id="login_password" placeholder="password">
								  </div>
								  <button type="submit" class="btn btn-default" @click='login'>提交</button>
							</form>
			    		</div>	
		            </div>
		            <div class="modal-footer">
		                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
		            </div>
		        </div>
		    </div>
		</div>
    </div>

	<div style="height:50px;" v-if="!(router_list.indexOf(path) != -1)"></div>

	<!-- 中间的 路由 router-view 区域 -->
	<router-view v-if="IsRouterAlive"></router-view>

  </div>

</template>

<script>
	$(function (){
		$(".navbar a").click(function () {
			$(".navbar a").attr("class", "btn btn-default btn-lg col-md-1")
			$(this).attr("class", "btn btn-primary btn-lg col-md-1")
		});
	})

	 export default {
        name: 'App',
        // 刷新组件
	    provide() {
	        return{
	            reload:this.reload,
	        }
	    },
        data(){
            return{
                path:'',
                qcode: 'https://login.weixin.qq.com/qrcode/',
                username: '',
                IsRouterAlive: true,
                router_list : ['/admin', '/query_user', '/query_template', '/upload_file', '/check_file'],
                search: '',
                is_vip: '',
            }
        },
        // 判断路由
        mounted() {
          this.path = this.$route.path;
          console.log(this.$route.path);
          // 请求判断用户有没有登录
          this.$axios.get("/get_session")
			.then((res)=>{
			    if (res.data.errno == 0) {
			    	console.log(res);
			    	this.username = res.data.username;
			    	this.is_vip = res.data.is_vip;
				} else {
					console.log(res);
				}
			});	

        },
        methods: {
        	login: function(){
        		let username = $('#login_username').val();
        		let password = $('#login_password').val();
        		let data = {'username': username, 'password': password};
        		let formdata = JSON.stringify(data);
        		this.$axios.post("/login", formdata)
	            .then((res)=>{
	            	if (res.data.errno == 0) {
	                	alert(res.data.errmsg);
	                	$('.close').trigger('click');
	                	this.username = res.data.username;
	            	} else {
	            		alert(res.data.errmsg);
	            	}
	            });	
	            this.reload();
        	},
        	register: function(){
        		let username = $('#register_username').val();
        		let password = $('#register_password').val();
        		let data = {'username': username, 'password': password};
        		let formdata = JSON.stringify(data);
        		this.$axios.post("/register", formdata)
	            .then((res)=>{
	                if (res.data.errno == 0) {
	                	alert(res.data.errmsg);
	                	$('.close').trigger('click');
	            	} else {
	            		alert(res.data.errmsg);
	            	}
	            });	
        	},
        	reload() {
	            this.IsRouterAlive = false;
	            this.$nextTick(function () {
	                this.IsRouterAlive = true;
	            })
	        },
	        click_search() {
	        	this.$router.replace('/index/'+this.search);
	        	this.reload();
			}
        },
        watch:{
            $route(to,from){
                this.path = to.path
            }
        }
    }
</script>

<style>
	.navbar-inverse {
		z-index: 1;
	}
	.navbar a {
		margin: 3px;
	}
	.input-group {
		margin: 10px;
		position: fixed;
		right: 20px;
		z-index: 2;
	}
	.register {
		list-style: none;
		position: fixed;
		right: 300px;
		z-index: 2;
	}
	.register li {
		margin: 10px;
		margin-right: 20px;
	}
	.register a {
		text-decoration: none;
	    display: inline-block;
	    width: 54px;
	    height: 26px;
	    text-align: center;
	    line-height: 26px;
	    color: #DDD;
	    font-size: 18px;
	    cursor:pointer;
	}
	.register a:hover {
		color: #AAA;
	}

</style>
