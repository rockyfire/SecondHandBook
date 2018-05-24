<template>
    <div class="my_nala_centre ilizi_centre">
        <div class="ilizi cle">
            <div class="box">
                <h5><span>订单状态</span></h5>
                <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
                    <tbody>
                        <tr>
                            <td width="15%" align="right" bgcolor="#ffffff">订单号：</td>
                            <td align="left" bgcolor="#ffffff">{{orderInfo.order.order_sn}}
                            </td>
                        </tr>
                        <tr>
                            <td align="right" bgcolor="#ffffff">订单状态：</td>
                            <td v-if="orderInfo.order.pay_status == 'PAYING' " align="left" bgcolor="#ffffff">待支付</td>
                            <td v-if="orderInfo.order.pay_status == 'TRADE_SUCCESS' " align="left" bgcolor="#ffffff">已支付</td>
                        </tr>
                        <tr>
                            <td align="right" bgcolor="#ffffff">下单/支付时间：</td>
                            <td v-if="orderInfo.order.pay_status == 'PAYING' " align="left" bgcolor="#ffffff">{{orderInfo.order.pay_time}}</td>
                            <td v-if="orderInfo.order.pay_status == 'TRADE_SUCCESS' " align="left" bgcolor="#ffffff">{{orderInfo.order.add_time}}</td>
                        </tr>
                    </tbody>
                </table>
                <table></table>

                <h5><span>商品列表</span></h5>
                <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
                    <tbody>
                        <tr>
                            <th width="30%" align="center" bgcolor="#ffffff">商品名称</th>
                            <th width="19%" align="center" bgcolor="#ffffff">商品价格</th>
                            <th width="9%" align="center" bgcolor="#ffffff">购买数量</th>
                            <th width="20%" align="center" bgcolor="#ffffff">小计</th>
                        </tr>
                        <tr>
                            <td bgcolor="#ffffff">
                                <router-link  :to="'/app/home/productDetail/'+orderInfo.books.id" class="f6">{{orderInfo.books.name}}</router-link>
                            </td>
                            <td align="center" bgcolor="#ffffff">￥{{orderInfo.books.price}}元</td>
                            <td align="center" bgcolor="#ffffff">{{orderInfo.books_num}}</td>
                            <td align="center" bgcolor="#ffffff">￥{{orderInfo.books.price*orderInfo.books_num}}元</td>
                        </tr>
                    </tbody>
                </table>

                <h5><span>收货人信息</span></h5>
                <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
                    <tbody>
                        <tr>
                            <td width="15%" align="right" bgcolor="#ffffff">收货人姓名： </td>
                            <td width="35%" align="left" bgcolor="#ffffff">
                            {{orderInfo.order.signer_name}}
                            </td>
                            <td width="15%" align="right" bgcolor="#ffffff">收货地址： </td>
                            <td width="35%" align="left" bgcolor="#ffffff">
                            {{orderInfo.order.signer_address}}
                            </td>
                        </tr>
                        <tr>
                            <td align="right" bgcolor="#ffffff">联系电话： </td>
                            <td align="left" bgcolor="#ffffff">
                            {{orderInfo.order.singer_mobile}}
                            </td>
                        </tr>
                    </tbody>
                </table>

                <h5><span>购买者信息</span></h5>
                <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
                    <tbody>
                        <tr>
                            <td width="15%" align="right" bgcolor="#ffffff">顾客姓名： </td>
                            <td width="35%" align="left" bgcolor="#ffffff">
                            {{orderInfo.order.user.username}}
                            </td>
                            <td width="15%" align="right" bgcolor="#ffffff">顾客电话： </td>
                            <td width="35%" align="left" bgcolor="#ffffff">
                            {{orderInfo.order.user.mobile}}
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
  import { getOrderDetail,getSoldDetail } from '../../api/api'
  export default {
        data () {
            return {
                orderId: '',
                orderInfo: {
                },
            };
        },
        components: {

        },
        props: {

        },
        created () {
            this.soldId = this.$route.params.soldId;
            this.goSoldDetail();
        },
        watch: {

        },
        computed: {

        },
        methods: {
            goSoldDetail(){
                getSoldDetail(this.soldId).then((response)=>{
                    this.orderInfo=response.data;
                }).catch(function (error) {
                    console.log(error);
                });
            },
        }
    }
</script>
<style>

.my_nala_centre {
    float: right;
    width: 970px;
    background-color: #fff;
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


</style>

