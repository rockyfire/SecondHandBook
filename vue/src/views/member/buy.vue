<template>
    <div class="my_nala_centre ilizi_centre">
        <div class="ilizi cle">
            <div class="box">
                <div class="box_1">
                    <div class="userCenterBox boxCenterList clearfix" style="_height:1%;">
                        <h5><span>求购的二手书籍信息</span></h5>
                        <div class="blank"></div>
                        <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
                            <tr align="center">
                                <td>书籍名称</td>
                                <td>书籍分类</td>
                                <td>书籍价格</td>
                                <td>书籍数量</td>
                                <td>下架时间</td>
                                <td>书籍详情</td>
                                <td>操作</td>
                            </tr>
                            <tr v-for="item in cbooks">
                                <td align="left" bgcolor="#ffffff">{{item.name}}</td>
                                <td align="left" bgcolor="#ffffff">{{item.category}}</td>
                                <td align="left" bgcolor="#ffffff">{{item.price}}</td>
                                <td align="left" bgcolor="#ffffff">{{item.nums}}</td>
                                <td align="left" bgcolor="#ffffff">{{item.revoke}}</td>
                                <td align="center" bgcolor="#ffffff"><router-link :to="'/app/home/productDetail/'+item.id"  :title="item.name" target = _blank><button class="bnt_blue_look">详情(浏览)</button></router-link></td>
                                <td align="center" bgcolor="#ffffff"><button class="bnt_blue_del" @click="deleteInfo(item.id)">删除(下架)</button></td>
                            </tr>
                        </table>
                        <Page pre-text="上一页" next-text="下一页" end-show="false" :page="curPage" :total-page='totalPage' @pagefn="pagefn"></Page>
                        <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
                            <tbody>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">书籍分类</td>
                                    <td align="left" bgcolor="#ffffff">
                                    　　<select class="choice" v-on:change="indexSelect" v-model="categoryId">
                                            <option v-for="(item,index) in allMenuLabel" v-bind:value="item.id">{{item.name}}</option>
                                    　　</select>
                                        <select class="choice" v-model="category">
                                            <option v-for="(item,index) in secMenuLabel.sub_cat" v-bind:value="item.id">{{item.name}}</option>
                                    　　</select>
                                        <span :class = "{error:category==''}">(必填)</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">书籍名称</td>
                                    <td align="left" bgcolor="#ffffff">
                                        <input name="consignee" type="text" class="inputBg" id="consignee_0" v-model="name">
                                        <span :class = "{error:name==''}">(必填)</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">出版社：</td>
                                    <td align="left" bgcolor="#ffffff">
                                        <input name="address" type="text" class="inputBg" id="address_0" v-model="press">
                                    </td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">书籍作者</td>
                                    <td align="left" bgcolor="#ffffff">
                                        <input name="mobile" type="text" class="inputBg" id="mobile_0" v-model="author">
                                    </td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">收购价格</td>
                                    <td align="left" bgcolor="#ffffff">
                                        <input name="mobile" type="text" class="inputBg" id="mobile_0" v-model="price">
                                        <span :class = "{error:price==''}">(必填)</span></td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">书籍图片</td>
                                    <td align="left" bgcolor="#ffffff">
                                        <input type="file" name="message_img" size="45" class="inputBg" @change="preview"/>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">书籍描述信息</td>
                                    <td align="left" bgcolor="#ffffff">
                                        <!--
                                        <div id="app">
                                             <VueUEditor @ready="editorReady"></VueUEditor>
                                        </div>
                                        -->
                                        <textarea></textarea>
                                        <span :class = "{error:desc==''}">(必填)</span></td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">下架时间</td>
                                    <td align="left" bgcolor="#ffffff">
                                        <datepicker language="ch"  v-model="revoke"></datepicker>
                                        <span :class = "{error:revoke==''}">(必填)</span></td>
                                </tr>
                                <tr>
                                    <td align="right" bgcolor="#ffffff">&nbsp;</td>
                                    <td colspan="3" align="center" bgcolor="#ffffff">
                                        <button class="bnt_blue_2" @click="addInfo">添加</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table> 
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import VDistpicker from 'v-distpicker'
import {getCreateBooksDetail,deleteCreateBooks,addCreateBook,getCreateBooks,getCategory} from '../../api/api'
import {getGoods} from '../../api/api'
import {formatDate} from '../../static/js/formatDate.js'
import datepicker from 'vue-date'
// 翻页
import page from '../list/page/page';
    export default {
        data () {
            return {
                cbooks:[],
                cbooksEmpty:{},
                category: '',
                name: '',
                press: '',
                author: '',
                price: '',
                revoke: '',
                file: '',
                desc: '',
                allMenuLabel:[],//菜单
                secMenuLabel:[],//二级菜单
                categoryId:'',
                curPage: 1, // 页码
                proNum : 1,
            };
        },
        props: {

        },
        components: {
            'v-distpicker': VDistpicker,
            datepicker,
            'Page': page,
        },
        created () {
            this.getBookList();
            this.getMenu();
        },
        watch: {

        },
        computed: {
            datepicker,
            totalPage(){
                return  Math.ceil(this.proNum/4)
            }
        },
        methods: {
            preview (e) {
                this.file  = e.target.files[0]; //获取文件资源
            },

            getBookList(){
                getGoods({
                    status : 2, //当前模块   
                    book_user:this.$store.state.userInfo.name, //当前用户创建
                    page: this.curPage, //当前页码
                }).then((response) =>{
                    this.cbooks=response.data.results
                }).catch(function(error){
                   console.log(error) 
                });
            },
            editorReady(editorInstance){
                editorInstance.setContent("hello world ")
                editorInstance.addListener('contentChange',()=>{
                    console.log('编辑器内容发生了变化',editorInstance.getContent())
                })
            },
            addInfo () { //提交收获信息
                const formData = new FormData();
                formData.append('category',this.category);
                formData.append('name',this.name);
                formData.append('press',this.press);
                formData.append('author',this.author);
                formData.append('price',this.price);
                formData.append('photo',this.file);
                formData.append('revoke',this.revoke);
                formData.append('status',2);
                addCreateBook(formData).then((response)=> {
                    alert('添加成功');
                    // 重置新的
                    this.getBookList();
                    // this.cbooksEmpty = Object.assign({});

                }).catch(function (error) {
                    console.log(error);
                });
            },
            getMenu(){//获取菜单
                getCategory({
                    params:{}
                }).then((response)=> {
                    this.allMenuLabel = response.data
                }).catch(function (error) {
                    console.log(error);
                });
            },
            indexSelect(){ //获取二级菜单
                getCategory({
                    id:this.categoryId,
                }).then((response)=> {
                    this.secMenuLabel = response.data
                }).catch(function (error) {
                    console.log(error);
                });
            },
            // confirmUpdate (id, index) { // 更新收获信息
            //     updateAddress(id, this.receiveInfoArr[index]).then((response)=> {
            //         alert('修改成功');
            //         this.getReceiveInfo();
            //     }).catch(function (error) {
            //         console.log(error);
            //     });

            // },
            deleteInfo (booksId) { // 删除（下架）
                deleteCreateBooks(booksId).then((response)=> {
                    alert('删除成功');
                    this.getBookList();
                }).catch(function (error) {
                    console.log(error);
                });
            },
            pagefn(value){//点击分页
                this.curPage = value.page;
                this.getBookList()
            }
        }
    }
</script>
<style scoped>
.error{
  color:#fa8341;
}
table {
    margin-bottom: 20px;
}
select {
    min-width: 80px;
}

.my_nala_main h3.my_nala {
    height:60px;
    border:1px solid #e7e7e7;
    border-bottom:0
}
.my_nala_main h3.my_nala a {
    display:block;
    height:60px;
    font-size:22px;
    text-align:center;
    line-height:60px;
    overflow:hidden
}
.my_nala_main h3.my_nala a:hover {
    text-decoration:none
}

.my_nala_centre {
    float:right;
    width:970px;
    background-color:#fff
}
.my_nala_centre .trade_mod .h301 a.more {
    font-size:14px;
    color:#666;
    font-weight:normal
}
.my_nala_centre .trade_mod .h301 a.more:hover {
    color:#09c762
}
.my_nala_centre .something_interesting {
    margin-top:10px
}
.my_nala_centre .something_interesting ul {
    margin-left:20px
}
.my_nala_centre .something_interesting li {
    width:130px;
    text-align:center;
    float:left
}
.my_nala_centre .something_interesting b {
    font-weight:normal
}
.my_nala_centre .something_interesting em {
    font-size:12px;
    font-weight:bold;
    color:#09c762
}
.my_nala_centre .relate_goods {
    border:1px solid #e4e4e4;
    border-top:0
}
.my_nala_centre .pagenav {
    padding:15px 10px;
    border-top:1px solid #e4e4e4
}


.ilizi_centre {
    background:0
}

.ilizi {
    border:1px solid #e4e4e4;
    padding:16px 18px;
    margin-bottom:10px;
    background:#fff
}
.ilizi .face,.iface .face {
    display:block;
    float:left;
    width:100px;
    height:100px;
    position:relative
}
.ilizi .edit_face,.iface .edit_face {
    position:absolute;
    height:20px;
    line-height:20px;
    width:100px;
    display:block;
    background:rgba(0,0,0,0.5);
    text-align:center;
    color:#fff;
    left:1px;
    bottom:-1px;
    _bottom:0;
    filter:progid:DXImageTransform.Microsoft.gradient(enabled='true',startColorstr='#77000000',endColorstr='#77000000');
    visibility:hidden;
    margin:0
}
.ilizi .face img,.iface .face img {
    width:100px;
    height:100px;
    border:1px solid #e4e4e4
}
.ilizi .ilizi_info {
    width:800px;
    float:right;
    height:100px
}
.bnt_blue_1,.bnt_blue,.bnt_bonus,.bnt_blue_2 {
    display:inline-block;
    padding:4px 12px;
    height:24px;
    line-height:16px;
    _line-height:18px;
    border:1px solid #1e9246;
    border-radius:3px;
    font-size:100%;
    color:#fff;
    background-color:#09c762;
    overflow:hidden;
    vertical-align:middle;
    cursor:pointer
}

.bnt_blue_look {
    display:inline-block;
    padding:4px 12px;
    height:24px;
    line-height:16px;
    _line-height:18px;
    border:1px solid #1e2392;
    border-radius:3px;
    font-size:100%;
    color:#fff;
    background-color:#35458c;
    overflow:hidden;
    vertical-align:middle;
    cursor:pointer
}

.bnt_blue_del {
    display:inline-block;
    padding:4px 12px;
    height:24px;
    line-height:16px;
    _line-height:18px;
    border:1px solid #d61860;
    border-radius:3px;
    font-size:100%;
    color:#fff;
    background-color:#ca1010;
    overflow:hidden;
    vertical-align:middle;
    cursor:pointer
}

</style>
<style type="text/css">
    .addr .address {
        height: 35px;
    }
    .addr .address select{
        height: inherit;
        font-size: inherit;
        border-radius: initial;
        width: 130px;
        padding:0
    }
</style>
