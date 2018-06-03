import axios from 'axios';

let host = 'http://www.flycode.me:8000';
// let host = 'http://127.0.0.1:8000';


//获取书籍类别信息
export const queryCategorygoods = params => { return axios.get(`${host}/indexmodule/`) }

//获取首页中的新品
export const newGoods = params => { return axios.get(`${host}/newgoods/`) }

//获取轮播图
export const bannerGoods = params => { return axios.get(`${host}/banner/`) }

//获取书籍类别信息
export const getCategory = params => {
  if('id' in params){
    return axios.get(`${host}/bookscategory/`+params.id+'/');
  }
  else {
    return axios.get(`${host}/bookscategory/`, params);
  }
};


//获取热门搜索关键词
export const getHotSearch = params => { return axios.get(`${host}/hotsearchs/`) }

//获取书籍列表
export const getGoods = params => { return axios.get(`${host}/books/`, { params: params }) }

//书籍详情
export const getGoodsDetail = booksid => { return axios.get(`${host}/books/${booksid}`+'/') }

// 获取当前用户创建书籍列表
export const getCreateBooks = params => { return axios.get(`${host}/bookscreate/`, { params: params }) }

// 获取当前用户创建书籍详情
export const getCreateBooksDetail = booksid => { return axios.get(`${host}/bookscreate/${booksid}`+'/') }

// 当前用户创建书籍
export const addCreateBook = params => { return axios.post(`${host}/bookscreate/`,params) }

// 删除（下架）当前用户创建的书籍
export const deleteCreateBooks = booksid => { return axios.delete(`${host}/bookscreate/`+booksid+'/') }
//获取购物车书籍
export const getShopCarts = params => { return axios.get(`${host}/shoppingcart/`) }
// 添加书籍到购物车
export const addShopCart = params => { return axios.post(`${host}/shoppingcart/`, params) }
//更新购物车书籍信息
export const updateShopCart = (booksId, params) => { return axios.patch(`${host}/shoppingcart/`+booksId+'/', params) }
//删除某个书籍的购物记录
export const deleteShopCart = booksId => { return axios.delete(`${host}/shoppingcart/`+booksId+'/') }


//登录
export const login = params => {
  return axios.post(`${host}/login/`, params)
}

//注册

export const register = parmas => { return axios.post(`${host}/users/`, parmas) }

//短信
export const getMessage = parmas => { return axios.post(`${host}/sendmessage/`, parmas) }


//获取用户信息
export const getUserDetail = () => { return axios.get(`${host}/users/1/`) }

//修改用户信息
export const updateUserInfo = params => { return axios.patch(`${host}/users/1/`, params) }


//获取订单
export const getOrders = () => { return axios.get(`${host}/order/`) }
//删除订单
export const delOrder = orderId => { return axios.delete(`${host}/order/`+orderId+'/') }
//添加订单
export const createOrder = params => {return axios.post(`${host}/order/`, params)}
//获取订单详情
export const getOrderDetail = orderId => {return axios.get(`${host}/order/`+orderId+'/')}

//获取已卖出书籍
export const getSolds = () => { return axios.get(`${host}/sold/`) }
//删除已卖出书籍
export const delSold = soldId => { return axios.delete(`${host}/sold/`+soldId+'/') }
//获取已卖出书籍详情
export const getSoldDetail = soldId => {return axios.get(`${host}/sold/`+soldId+'/')}


//收藏 
export const addFav = params => { return axios.post(`${host}/userfavs/`, params) }

//取消收藏 
export const delFav = booksId => { return axios.delete(`${host}/userfavs/`+booksId+'/') }

// 获取所有收藏 显示在个人列表中 
export const getAllFavs = () => { return axios.get(`${host}/userfavs/`) }

//判断是否收藏 
export const getFav = booksId => { return axios.get(`${host}/userfavs/`+booksId+'/') }

//获取留言
export const getMessages = () => {return axios.get(`${host}/userleavingmessage/`)}

//添加留言
export const addMessage = params => {return axios.post(`${host}/userleavingmessage/`, params, {headers:{ 'Content-Type': 'multipart/form-data' }})}

//删除留言
export const delMessages = messageId => {return axios.delete(`${host}/userleavingmessage/`+messageId+'/')}

//添加收货地址
export const addAddress = params => {return axios.post(`${host}/useraddress/`, params)}

//删除收货地址
export const delAddress = addressId => {return axios.delete(`${host}/useraddress/`+addressId+'/')}

//修改收货地址
export const updateAddress = (addressId, params) => {return axios.patch(`${host}/useraddress/`+addressId+'/', params)}

//获取收货地址
export const getAddress = () => {return axios.get(`${host}/useraddress/`)}

//添加评论
export const addComment = params => {return axios.post(`${host}/comment/`, params)}

//删除评论
export const delComment = commentId => {return axios.delete(`${host}/comment/`+commentId+'/')}