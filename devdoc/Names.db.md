## 命名规定

所有数据库的命名以及, 数据库表格内的命名参照此文档。  
加有标志[main]的表示主键, 主键在每一张表内恒唯一.

str: 字符串
double: IEEE 64位浮点数
bool: 布尔值

* users 用户
    * [main] mail: str: 注册邮箱
    * name: str: 用户名
	* password: str: 密码 (密文)
    * rank: double: 评分
* houses 房屋
    * [main] id: str: ID
    * address: str: 地址(精确到城市, 任意填写)
    * title: str: 标题
    * master: str: 户主(邮箱)
    * rank: double: 评分
    * picture: str: 图片文件夹. 文件夹下每一个图片索引至一个uri. 
    * order: str: 关联订单
* orders 订单
    * [main] id: str: ID
	* time: str: 发布时间
    * customer: str: 发起人的id(邮箱)
    * owner: str: 承接人(房屋持有人)的id(邮箱)
    * passed: bool: 审核状态
    * state: str: 交易状态
