<template>
    <div class="current-loc">
        <div class="breadcrumbs cle z-detail-box">
          <div class="menus">
            <a href="http://www.flycode.me:8000/index">首页</a>
            <code>&gt;</code>
            <!-- <a href="http://sx.web51.youxueshop.com/category.php?id=2">生鲜食品</a>
            <code>&gt;</code> -->
            <a href="">{{proDetail.category}}</a>
            <code>&gt;</code>
            {{proDetail.name}}
          </div>
      </div>
    
    </div>
  
</template>
<script>
  import { getGoodsDetail } from '../../../api/api';
  export default {
    data () {
        return {
            proDetail: {
            },
            productId:'',
        };
    },
    components: {
        
    },
    props: {
        
    },
    created () {
        this.productId = this.$route.params.productId;
        var productId = this.productId
        this.getDetails();
    },
    watch: {
        
    },
    computed: {

    },
    methods: {
        getDetails () { //  请求商品详情
          getGoodsDetail(this.productId)
            .then((response)=> {
                console.log(response.data);
                this.proDetail = response.data;
            }).catch(function (error) {
                console.log(error);
            });
        },
    }
}
</script>
<style  lang='scss'>
.cle:after{
    visibility:hidden;
    display:block;
    font-size:0;
    content:'\20';
    clear:both;
    height:0
}
.cle{
    *zoom:1
}

a {
    text-decoration:none;
    color:#333;
    -webkit-transition:color .2s;
    -moz-transition:color .2s;
    -o-transition:color .2s;
    -ms-transition:color .2s;
    transition:color .2s
}
a:hover {
    color:#09c762
}
a:focus,area:focus {
    outline:0
}

canvas {
    -ms-touch-action:double-tap-zoom
}

.breadcrumbs {
    padding:0 5px 0 0;
    line-height:38px;
    color:#666
}
.breadcrumbs .menus {
    float:left
}
.breadcrumbs .menus a {
    margin-right:6px
}
.breadcrumbs .right {
    float:right;
    color:#bbb
}
.breadcrumbs .right i {
    font-size:20px;
    margin-right:5px;
    vertical-align:-2px
}
.breadcrumbs .right .code {
    color:#fafafa;
    margin-right:30px;
    display:inline-block
}

</style>
