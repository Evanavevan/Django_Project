$(document).ready(function(){

    var phone = document.getElementById('phone')
    var phonenum = document.getElementById('phonenum')

    // 给手机号码框添加一个聚焦事件
    phone.addEventListener("focus", function(){
        phonenum.style.display = 'none'
    }, false)

    // 当输入域失去焦点 (blur) 后检测手机号码的格式要求
    phone.addEventListener("blur", function(){
        // 取手机号码
        instr = this.value
        // 正则
        var reg=/^1[3|4|5|6|7|8|9][0-9]{9}$/
        // 检测输入长度是否为11位并且符合格式要求
        if (instr.length != 11 | reg.test(instr) == false){
            // 长度不符或者格式要求不对，显示错误
            phonenum.style.display = 'block'
            // 并且让提交按钮无效
            $('.send').attr('disabled', true)
        }else{
        // 如果重新输入符合格式要求，则将按钮激活（一定要注意加上此操作，否则按钮一直处于失活状态）
        $('.send').attr('disabled', false)
        }
    }, false)
})