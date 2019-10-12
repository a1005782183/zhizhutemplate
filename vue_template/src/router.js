import VueRouter from 'vue-router'

// 导入对应的路由组件
import index from './components/index.vue'
import not_vip_temp from './components/not_vip_temp.vue'
import vip_temp from './components/vip_temp.vue'
import add_vip from './components/add_vip.vue'
import success_vip from './components/success_vip.vue'
import detail from './components/detail.vue'
import download from './components/download.vue'
import user_detail from './components/user_detail.vue'
import Admin from './components/admin/admin.vue'
import query_user from './components/admin/query_user/query_user.vue'
import query_template from './components/admin/query_template/query_template.vue'
import upload_file from './components/admin/upload_file/upload_file.vue'
import check_file from './components/admin/check_file/check_file.vue'
import user_upload_file from './components/user_detail/user_upload_file.vue'
import user_detail_temp from './components/user_detail/user_detail_temp.vue'

var router = new VueRouter({
	routes: [	// 配置路由规则的
		{ path: '/', redirect: '/index' },
		{ path: '/index', component: index },
		{ path: '/index/:search', component: index },
		{ path: '/not_vip_temp', component: not_vip_temp },
		{ path: '/vip_temp', component: vip_temp },
		{ path: '/add_vip', component: add_vip },
		{ path: '/success_vip', component: success_vip },
		{ path: '/detail/:id', component: detail },
		{ path: '/download/:id', component: download },
		{ path: '/user_detail', component: user_detail, children: [
			{ path: '/user_upload_file', component: user_upload_file },
			{ path: '/user_detail_upload', component: user_detail_temp },
			{ path: '/user_detail_collect', component: user_detail_temp },
			{ path: '/user_detail_down', component: user_detail_temp },
		] },
		{ path: '/admin', component: Admin, children: [
			{ path: '/query_user', component: query_user },
			{ path: '/query_template', component: query_template },
			{ path: '/upload_file', component: upload_file },
			{ path: '/check_file', component: check_file },
		] },
	],
	linkActiveClass: 'mui-active' // 覆盖默认的路由高亮的类，默认的类叫做router-link-active
})

// 把路由对象暴露出去
export default router