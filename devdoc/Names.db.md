## 命名规定

所有数据库的命名以及, 数据库表格内的命名参照此文档。  
加有标志[main]的表示主键, 主键在每一张表内恒唯一.

str: 字符串.
double: IEEE 64位浮点数. 数据库内类型为Double.
bool: 布尔值. 数据库内类型为Yes/No.

* users 用户
    * [main] mail: str: 注册邮箱
    * name: str: 用户名
	* password: str: 密码 (密文)
    * rankTimes: int: 历史评分次数
    * rank: double: 评分
    * valid: bool: 是否通过审核
* houses 房屋
    * [main] id: str: ID [使用时间顺序递增赋值(待商定)]
    * address: str: 地址(任意填写)
    * title: str: 标题
    * description: str: 房屋简介
    * master: str: 户主(邮箱)
    * rank: double: 房屋评级
    * picture: str: 图片文件夹. 文件夹下每一个图片索引至一个uri. 
    * value: double: 显示价格
    * valid: bool: 是否通过
* orders 订单
    * [main] id: str: ID [使用时间顺序递增赋值(待商定)]
	* time: str: 发布时间 [按天计(待商定). 使用sqlite自带的时间处理函数把字符串转成Data或其它数据类型进行运算.]
    * value: double: 订单价格
    * customer: str: 发起人(租用者)的id(邮箱)
    * owner: str: 承接人(房屋持有人)的id(邮箱)
    * house: str: 关联房屋的id [一个订单有且仅有一个房屋]
    * passed: bool: 审核状态 [true: 审核通过. false: 审核未通过]
    * done: bool: 交易状态 [true: 交易完成. false: 审核完毕, 交易中]
