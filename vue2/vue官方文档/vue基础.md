#### vue 基本的代码结构

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
  <!-- 导入Vue的包 -->
  <script src="./lib/vue-2.4.0.js"></script>
</head>

<body>
   <!--被控制的容器-->
  <div id="app">
    <a>{{ msg }}</a>
    <input type="button" value="浪起来" @click="lang">
  </div>
  
  <script>
    //控制该容器的vm对象
    var vm = new Vue({
      el: '#app',  
      //这个vm的数据
      data: { 
        msg: '欢迎学习Vue' 
      },
      //这个vm实例可用的函数
      methods:{
        lang(){
          //调用数据时 要加 this
          console.log(this.msg)
        }
      }
    })
  </script>
</body>

</html>
```

#### 插值表达式

- v-cloak  和 v-text

  ```html
      <!-- 使用 v-cloak 能够解决 插值表达式闪烁的问题 -->
      <p v-cloak>++++++++ {{ msg }} ----------</p>
      <h4 v-text="msg">==================</h4>
      <!-- 默认 v-text 是没有闪烁问题的 -->
      <!-- v-text会覆盖元素中原本的内容，但是 插值表达式  只会替换自己的这个占位符，不会把 整个元素的内容清空 -->
  ```

- v-html

  ```html
  <div v-html="<h1>哈哈，我是一个大大的H1， 我大，我骄傲</h1>">1212112</div>
  ```

- v-bind 单向绑定数据 从m 绑定到 v   和 v-on     绑定事件

  ```html
       //v-bind: 是 Vue中，提供的用于绑定属性的指令 
       <input type="button" value="按钮" v-bind:title="mytitle + '123'"> 
       //注意： v-bind: 指令可以被简写为 :要绑定的属性 
       //v-bind 中，可以写合法的JS表达式 

  	 <!-- Vue 中提供了 v-on: 事件绑定机制 -->
      <input type="button" value="按钮" :title="mytitle + '123'" v-on:click="alert('hello')"> 
      <input type="button" value="按钮" @click="show">
  ```

- v-model  用来双向绑定数据

  ```html
  <!-- 注意： v-model 只能运用在 表单元素中 -->
  <input type="text" style="width:100%;" v-model="msg">
  ```

- v-for   可以循环 普通数组  对象数组     对象 以及迭代数字

  ```html
  //普通数组
  //直接循环
  <p v-for="item in list">{{item}}</p>
  // 值和索引
  <p v-for="(item, i) in list">索引值：{{i}} --- 每一项：{{item}}</p>

  //对象数组
  <p v-for="(user, i) in list">Id：{{ user.id }} --- 名字：{{ user.name }} --- 索引：{{i}}</p>

  //对象
  <p v-for="(val, key, i) in user">值是： {{ val }} --- 键是： {{key}} -- 索引： {{i}}</p>

  //迭代数字
  <p v-for="count in 10">这是第 {{ count }} 次循环</p>

  //在一些特殊情况   v-for循环时  需要指定key的值  str 或者 number
      <p v-for="item in list" :key="item.id">
        <input type="checkbox">{{item.id}} --- {{item.name}}
      </p>
  ```

- v-if 和 v-show

  ```html
   <!-- v-if 的特点：每次都会重新删除或创建元素 -->
   <!-- v-show 的特点： 每次不会重新进行DOM的删除和创建操作，只是切换了元素的 display:none 样式 -->    
  <h3 v-if="flag">这是用v-if控制的元素</h3>
  <h3 v-show="flag">这是用v-show控制的元素</h3>
  ```

#### 事件修饰符

```html
    <!-- 使用  .stop  阻止冒泡 -->
     <div class="inner" @click="div1Handler">
      <input type="button" value="戳他" @click.stop="btnHandler">
    </div> 

    <!-- 使用 .prevent 阻止默认行为 例如 a 标签就不会跳转  -->  
    <a href="http://www.baidu.com" @click.prevent="linkClick">有问题，先去百度</a> 

    <!-- 使用  .capture 实现捕获触发事件的机制  从外到里 触发时间 -->
    <div class="inner" @click.capture="div1Handler">
      <input type="button" value="戳他" @click="btnHandler">
    </div> 

    <!-- 使用 .self 实现只有点击当前元素时候，才会触发事件处理函数 -->
     <div class="inner" @click="div1Handler">
      <input type="button" value="戳他" @click="btnHandler">
    </div>

    <!-- 使用 .once 只触发一次事件处理函数 -->
     <a href="http://www.baidu.com" @click.prevent.once="linkClick">有问题，先去百度</a> 


    <!-- 演示： .stop 和 .self 的区别 -->
     <div class="outer" @click="div2Handler">
      <div class="inner" @click="div1Handler">
        <input type="button" value="戳他" @click.stop="btnHandler">
      </div>
    </div> 

    <!-- .self 只会阻止自己身上冒泡行为的触发，并不会真正阻止 冒泡的行为 -->
     <div class="outer" @click="div2Handler">
      <div class="inner" @click.self="div1Handler">
        <input type="button" value="戳他" @click="btnHandler">
      </div>
    </div> 
```

#### 绑定样式的方式

- 绑定class

  ```html
  <head>  
    <style>
      .red {
        color: red;
      }
      .thin {
        font-weight: 200;
      }
      .italic {
        font-style: italic;
      }
      .active {
        letter-spacing: 0.5em;
      }
    </style>
  </head>


  <body>
    <div id="app">
      // 普通的绑定
       <h1 class="red thin">这是一个很大很大的H1，大到你无法想象！！！</h1> 
  	//v-bind 做数据绑定
      <!-- 第一种使用方式，直接传递一个数组，注意： 这里的 class 需要使用  v-bind 做数据绑定 -->
       <h1 :class="['thin', 'italic']">这是一个很大很大的H1，大到你无法想象！！！</h1> 

      <!-- 在数组中使用三元表达式 -->
       <h1 :class="['thin', 'italic', flag?'active':'']">这是一个很大很大的H1，大到你无法想象！！！</h1> 

      <!-- 在数组中使用 对象来代替三元表达式，提高代码的可读性 -->
       <h1 :class="['thin', 'italic', {'active':flag} ]">这是一个很大很大的H1，大到你无法想象！！！</h1> 

      <!-- 在为 class 使用 v-bind 绑定 对象的时候，对象的属性是类名，由于 对象的属性可带引号，也可不带引号，所以 这里我没写引号；  属性的值 是一个标识符 -->
      <h1 :class="classObj">这是一个很大很大的H1，大到你无法想象！！！</h1>

    </div>
    <script>
      // 创建 Vue 实例，得到 ViewModel
      var vm = new Vue({
        el: '#app',
        data: {
          flag: true,
          classObj: { red: true, thin: true, italic: false, active: false }
        },
        methods: {}
      });
    </script>
  </body>
  ```

- 绑定style

  ```html
  <body>
    <div id="app">
      <!-- 对象就是无序键值对的集合 -->
      <h1 :style="styleObj1">这是一个h1</h1> 

      <h1 :style="[ styleObj1, styleObj2 ]">这是一个h1</h1>
    </div>

    <script>
      // 创建 Vue 实例，得到 ViewModel
      var vm = new Vue({
        el: '#app',
        data: {
          styleObj1: { 'color': 'red', 'font-weight': 200 },
          styleObj2: { 'font-style': 'italic' }
        },
        methods: {}
      });
    </script>
  </body>
  ```

  ​