function info(){

    const user = document.getElementById("n")
    const pass = document.getElementById("p")
    user.value = user.value.trim()
    pass.value = pass.value.trim()
    if(user.value=="" && pass.value==""){
        alert("❌ Please Enter Valid Input ❌")
    }else{
        alert("Logged In 🔐")
    }
}