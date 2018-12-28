$(document).ready(function(){

    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    // 添加商品
    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            //发起a_jax请求
            $.post("/changeshoppingcar/0/", {'productid': pid}, function(data){
                if (data.status == "success"){
                    // 添加成功，把中间的span的innerHTML变成当前的数量
                    // 修改商品数量
                    document.getElementById(pid).innerHTML = data.data
                    // 修改该商品的总价
                    document.getElementById(pid+"price").innerHTML = "￥"+data.price
                    // 修改订单总价
                    document.getElementById("totalprice").innerHTML = data.sum
                }
            })
        }, false)
        }

    // 减小商品
    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            // 发起a_jax请求
            $.post("/changeshoppingcar/1/", {'productid': pid}, function(data){
                if (data.status == "success"){
                    // 减小成功，把中间的span的innerHTML变成当前的数量
                    // 修改商品数量
                    document.getElementById(pid).innerHTML = data.data
                    // 修改该商品的总价
                    document.getElementById(pid+"price").innerHTML = "￥"+data.price
                    // 修改订单总价
                    document.getElementById("totalprice").innerHTML = data.sum
                    // 减小到零自动删除
                    if (data.data == 0){
                        // 下面的方法起不了作用
                        // window.location.href = "/shoppingcar/"
                        var li = document.getElementById(pid+"li")
                        // 删除指定节点及其所有下属节点，即删除显示该商品的标签
                        li.parentNode.removeChild(li)
                    }
                }
            })
        }, false)
        }



    // 取消打钩和添加加打钩
    var ischoses = document.getElementsByClassName("ischose")
    for (var j=0;j < ischoses.length; j++){
        ischose = ischoses[j]
        ischose.addEventListener("click", function(){
            pid = this.getAttribute("goodsid")
            $.post("/changeshoppingcar/2/", {'productid': pid}, function(data){
                if (data.status == "success"){
                    // 通过刷新
                    // window.location.href = "/shoppingcar/"
                    // 修改商品对应的钩
                    var s = document.getElementById(pid+"a")
                    s.innerHTML = data.data
                    // 修改全选项对应的钩
                    document.getElementById("allchose").innerHTML = data.all
                    // 修改订单总价
                    document.getElementById("totalprice").innerHTML = data.sum
                }
            })
        }, false)
    }

    // 全选钩
    var all = document.getElementById("all")

    all.addEventListener("click", function(){
        // 获取全选框中对应的内容（不用.value的原因在于内容不是一个值，而只是一个字符串）
        var allchose = document.getElementById("allchose").innerText
        //alert(allchose)，在页面上显示allchose的内容
        $.post("/changeshoppingcar/3/", {"allchose": allchose}, function(data){
            if (data.status == "success"){
                // 通过刷新
                // window.location.href = "/shoppingcar/"
                document.getElementById("allchose").innerHTML = data.data

                // 修改清单列表上的状态
                var ischoses = document.getElementsByClassName("ischose")
                for (var j=0;j < ischoses.length; j++){
                    ischose = ischoses[j]
                    pid = ischose.getAttribute("goodsid")
                    document.getElementById(pid+"a").innerHTML = data.data

                }
                // 修改订单总价
                document.getElementById("totalprice").innerHTML = data.sum
            }
        })
    }, false)

    // 提交订单
    var ok = document.getElementById("ok")
    ok.addEventListener("click", function(){
        // 页面弹出咨询窗口
        var f = confirm("是否确认下单？")
        if (f){
            $.post("/saveorder/", function(data){
                if (data.status == "success"){
                    // 重定向
                    window.location.href = "/shoppingcar/"
                }
            })
        }
    }, false)
})