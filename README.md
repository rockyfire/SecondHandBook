# SecondHandBook
二手书交易平台开发(毕业设计)

### 对于有出售二手书需求的同学，有多种渠道可以解决二手书的出售问题。

1. 第一个渠道是可以通过该平台快速**发布**想要出售的二手书信息，发布之后其他用户可以通过**浏览**网站或者通过**特定条件的搜索**可以查找到已发布的书籍信息，并进行**购买**；
2. 第二个渠道是可以通过浏览**“征书墙”**上其他用户发布的**求购信息**，找到有相应需求的用户信息进行出售；
3. 第三个渠道是可以发布**竞拍(一口价)**，设定一定的时间段和价格起点等，等待用户竞价。

### 对于有购买需求的同学，同样有多种渠道可以获取到需要的书籍：

- 发布求购，
- 浏览书城，
- 参与竞拍。

### 该网站对每一个用户维持一个信用积分，用户根据信用积分具有相应的功能，

例如信用积分低的用户可以发售的书籍数量少，信用积分高的用户可以发售的书籍数量多等等。
根据**成功交易的次数、恶意竞拍**等行为进行信用积分的增减。

### 网站具有相应权限的管理和分配，

管理员可以把“用户管理”等权限分配给相应用户，使这些用户成为具有一定权限的管理者，共同维护网站。

### 网站还具有**即时通讯**的功能，买家和卖家可以在线沟通协调关于商品的信息。


## 环境搭建


生成requirements.txt文件
```
pip freeze > requirements.txt                
```
安装requirements.txt依赖
```
pip install -r requirements.txt

-r --requirement <file> 
Install from the given requirements file.This option can be used multiple times
从给定的需求文件安装。此选项可以多次使用
```

使用豆瓣镜像下载

```
pip install -i https://pypi.douban.com/simple -r requirements.txt
```

(Window 下Python包)[https://www.lfd.uci.edu/~gohlke/pythonlibs/]


### 依赖详解

- xadmin
    - django-crispy-forms
    - django-reversion
    - django-formtools
    - future
    - httplib2
    - six

- 生成excel文件
    - xlwt
    - xlsxwriter