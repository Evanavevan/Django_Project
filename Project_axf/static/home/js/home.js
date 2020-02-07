$(function(){

    setTimeout(function(){
        swiper1()
        swiper2()
    }, 100)

    // 修改购物车，通过点击首页里商品的按钮增加商品数量以修改购物车
    // 获取类的属性，得到的是一个列表的属性，一般html有for循环就要用getElementsByClassName
    var addShoppings = document.getElementsByClassName("addShopping")

    // 添加商品
    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function(){
            // getAttribute() 方法返回指定属性名的属性值
            // this固定指向运行时的当前对象
            pid = this.getAttribute("ga")
            // 发起a_jax请求, $.post(URL,data,callback), callback 参数是请求成功后所执行的函数名
            $.post("/changeshoppingcar/0/", {'productid': pid}, function(data){
                if (data.status !== "success"){
                    if (data.data === -1){
                        // 页面跳转，表示用户未登录
                        window.location.href = "/login/"
                    }
                }
            })
        })
        }

})

// 自动轮播
function swiper1(){

    var mySwiper1 = new Swiper("#topSwiper", {
        direction: 'horizontal',
        loop: true,
        speed: 500,
        autoplay: 2000,
        pagination:".swiper-pagination",
        control: true,
    });
};

// 手动轮播
function swiper2(){

    var mySwiper2 = new Swiper("#swiperMenu", {
        slidesPerView: 3,
        paginationClickable: true,
        spaceBetween: 2,
        loop: false,
    });
};