$(document).ready(function(){

    var account = document.getElementById('account')
    var accounter = document.getElementById('accounter')
    var checker = document.getElementById('checker')


    var passwd = document.getElementById('passwd')
    var passer = document.getElementById('passer')


    var password = document.getElementById('password')
    var passworder = document.getElementById('passworder')

    var phone = document.getElementById('phone')
    var phonenum = document.getElementById('phonenum')

    // 验证账号，包括是否已注册和格式
    account.addEventListener("focus", function(){
        accounter.style.display = 'none'
        checker.style.display = 'none'
    }, false)
    account.addEventListener("blur", function(){
        instr = this.value
        // 如果账号长度小于6位或者大于12位，报错，并且提交按钮失效
        if (instr.length < 6 || instr.length > 12){
            accounter.style.display = 'block'
            $('.send').attr('disabled', true)
        }else{
            $('.send').attr('disabled', false)
        }
        // 判断用户是否已注册
        $.post("/checkuserid/", {"userid": instr}, function(data){
            if(data.status == 'error'){
                checker.style.display = 'block'
                $('.send').attr('disabled', true)
            }else{
                $('.send').attr('disabled', false)
            }
        })
    }, false)

    // 验证密码，主要是格式
    passwd.addEventListener("focus", function(){
        passer.style.display = 'none'
    }, false)
    passwd.addEventListener("blur", function(){
        instr = this.value
        // 如果账号长度小于6位或者大于16位，报错，并且提交按钮失效
        if (instr.length < 6 || instr.length > 16){
            passer.style.display = 'block'
            $('.send').attr('disabled', true)
        }else{
            $('.send').attr('disabled', false)
        }
    }, false)

    // 验证再次输入的密码是否正确
    password.addEventListener("focus", function(){
        passworder.style.display = 'none'
    }, false)
    password.addEventListener("blur", function(){
        instr = this.value
        // 与第一次输入的密码不一样，报错
        if (instr != passwd.value){
            passworder.style.display = 'block'
            $('.send').attr('disabled', true)
        }else{
            $('.send').attr('disabled', false)
        }
    }, false)

    // 验证手机号码格式
    phone.addEventListener("focus", function(){
        phonenum.style.display = 'none'
    }, false)

    phone.addEventListener("blur", function(){
        instr = this.value
        var reg=/^1[3|4|5|6|7|8|9][0-9]{9}$/
        if (instr.length != 11 | reg.test(instr) == false){
            phonenum.style.display = 'block'
            $('.send').attr('disabled', true)
        }else{
            $('.send').attr('disabled', false)
        }
    }, false)
})