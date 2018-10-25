#### 将js中的 一些api 可以看一下



[api文档](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects)

- list.push()  往数组中添加
- list.splice()  往数组中删除,添加
- list.some()    遍历数组,并调用回调函数  返回true则立刻结束
- list.findIndex()   遍历数组   调用回调函数  返回ture则 立刻结束 并返回停止位置在数组中的位置
- list.forEach()  遍历数组  调用回调函数  
- list.filter()  遍历数组  调用回调函数
- string.indexOf()    返回字符串中查询字符串的位置  如果没有 返回-1
- string.includes()     字符串中是否包含字符串  返回true 或 false
- string.padStart(2,'0')    缺失补全   



#### 过滤器

```html
//使用方法
  <div id="app">
    <p>{{ msg | msgFormat('疯狂+1', '123') | test }}</p>
  </div>

//全局过滤器
  <script>
    Vue.filter('msgFormat', function (msg, arg, arg2) {
      // 字符串的  replace 方法，第一个参数，除了可写一个 字符串之外，还可以定义一个正则
      return msg.replace(/单纯/g, arg + arg2)
    })
 </script>
//局部过滤器  只有vm实例可以使用
   var vm = new Vue({
      el: '#app',
      data: {
        msg: '曾经，我也是一个单纯的少年'
      },
      methods: {},
	filters: {
  		capitalize: function (value) {
   			 if (!value) return ''
    			value = value.toString()
    			return value.charAt(0).toUpperCase() + value.slice(1)
 	 }
    });

```



#### 按键修饰符



#### 生命周期函数



#### vue-resource 





