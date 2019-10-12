<template>
    <div id="upload_file">
        <form method="post" enctype="multipart/form-data" autocomplete="off" @submit.prevent="onSubmit">
            
            <div id="imgs" class="col-md-3">
                <div id="bg_img"></div>
                <input id="fileImgName" name="fileImgName" type="text" class="form-control" readonly="readonly">
                <a href="javascript:;" class="file">选择图片
                    <input id="fileImg" type="file" name="fileImg">
                </a>
            </div>

            <div class="col-md-5">
                <input id="fileName" name="fileName" type="text" class="form-control" readonly="readonly">
                <a href="javascript:;" class="file">选择文件压缩包
                    <input id="fileField" type="file" name="file">
                </a>
                <div class="form-group">
                    <label for="inputEmail3" class="col-sm-3 control-label">标题</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" id="title" placeholder="标题">
                    </div>
                </div>
                <div class="form-group">
                    <label for="inputEmail3" class="col-sm-3 control-label">内容</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" id="content" placeholder="内容">
                    </div>
                </div>
                <div class="form-group">
                    <label for="inputEmail3" class="col-sm-3 control-label">下载类型</label>
                    <div class="col-sm-9">
                      <input type="radio" name="radios" value=0 checked>免费
                      <input type="radio" name="radios" value=1>VIP
                    </div>
                </div>
                <input class="btn btn-default col-sm-6" type="submit" value="提交" @click="request_file">
            </div>
        </form>
    </div>  
</template>

<script>

export default {
    data(){
        return{
        }
    },
    // 判断路由
    mounted() {
        $('#fileField').on('change', function () {
            var name = document.getElementById('fileField').files[0].name;
            $('#fileName').val(name);
        });
        $('#fileImg').on('change', function () {
            var name = document.getElementById('fileImg').files[0].name;
            $('#fileImgName').val(name);
        });
        
    },
    methods: {
        request_file: function() {
            // 获取图片
            let fileImg = $('#fileImg').get(0).files[0];
            // 获取标题
            let title = $('#title').val();
            // 获取内容
            let content = $('#content').val();
            // 获取是否VIP值
            let is_vip = $('input:radio:checked').val();
            // 获取文件对象
            let fileField = $('#fileField').get(0).files[0];
            let formdata = new FormData;
            formdata.append('fileField', fileField);
            formdata.append('fileImg', fileImg);
            formdata.append('title', title);
            formdata.append('content', content);
            formdata.append('is_vip', is_vip);
            let headers = {headers: {"Content-Type": "multipart/form-data"}};
            this.$axios.post("/upload_file", formdata, headers)
            .then((res)=>{
                console.log(res.data.errmsg);
            })
            .catch((error)=>{
                  console.log('上传文件过大！');
            });
        },
        // 阻止form表单提交
        onSubmit(){return false;}
    }

}
</script>

<style>
#imgs {
    width: 200px;
    height: 90px;
}
#bg_img {
    width: 100%;
    height: 100%;
    background:url(../../assets/aa.jpg);
    background-size:100% 100%;
}
#upload_file {
    margin-top: 20px;
}

.file {
    position: relative;
    display: inline-block;
    background: #D0EEFF;
    border: 1px solid #99D3F5;
    border-radius: 4px;
    padding: 4px 12px;
    overflow: hidden;
    color: #1E88C7;
    text-decoration: none;
    text-indent: 0;
    line-height: 24px;
}
.file input {
    position: absolute;
    font-size: 100px;
    right: 0;
    top: 0;
    opacity: 0;
}
.file:hover {
    background: #AADFFD;
    border-color: #78C3F3;
    color: #004974;
    text-decoration: none;
}
#imgs .form-control {
    width: 51.7%;
    float: left;
}
.form-control {
    width: 300px;
    float: left;
}
</style>
