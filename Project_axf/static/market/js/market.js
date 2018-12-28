$(document).ready(function(){
    // 获取id属性
    var alltypebtn = document.getElementById('alltypebtn')
    var showsortbtn = document.getElementById('showsortbtn')

    var typediv = document.getElementById('typediv')
    var sortdiv = document.getElementById('sortdiv')

    // 不显示
    typediv.style.display = 'none'
    sortdiv.style.display = 'none'

    // 给“全部类型”添加点击事件
    alltypebtn.addEventListener("click", function(){
       typediv.style.display = 'block'
       sortdiv.style.display = 'none'
    }, false)
    // 给“综合排序”添加点击事件
    showsortbtn.addEventListener("click", function(){
       typediv.style.display = 'none'
       sortdiv.style.display = 'block'
    }, false)
    // 给全部类型所属的那个div添加点击事件，点击div外的任何一部分，div收起
    typediv.addEventListener("click", function(){
       typediv.style.display = 'none'
    }, false)
    // 给综合排序所属的那个div添加点击事件，点击div外的任何一部分，div收起
    sortdiv.addEventListener("click", function(){
       sortdiv.style.display = 'none'
    }, false)




    // 修改购物车，通过点击超市里商品的按钮增添减小商品数量以修改购物车
    // 获取类的属性，得到的是一个列表的属性，一般html有for循环就要用getElementsByClassName
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    // 添加商品
    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function(){
            // getAttribute() 方法返回指定属性名的属性值
            // this固定指向运行时的当前对象
            pid = this.getAttribute("ga")
            // 发起a_jax请求, $.post(URL,data,callback), callback 参数是请求成功后所执行的函数名
            $.post("/changeshoppingcar/0/", {'productid': pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                }
                else {
                    if (data.data == -1){
                        // 页面跳转，表示用户未登录
                        window.location.href = "/login/"
                    }
                }
            })
        })
        }

    // 减小商品
    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            //发起a_jax请求
            $.post("/changeshoppingcar/1/", {'productid': pid}, function(data){
                if (data.status == "success"){
                    //减小成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                } else {
                    if (data.data == -1){
                        window.location.href = "/login/"
                    }
                }
            })
        })
        }

})