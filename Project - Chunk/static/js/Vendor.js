function add(){
    let ops = "insert"
    const cost = document.getElementById("Coster")
    const Name = document.getElementById("TestName")
    const opt = document.getElementById("optionsgpt")
    alert(opt.value)
    if(cost.value.trim()!="" && Name.value.trim()!=""){
        let Data = `${ops} ${Name.value} ${cost.value} ${opt.value}`
        serverInfo(Data)
    }else{
        alert(getEmoji()+" Empty Input")
    }
}
function getEmoji(){
    let Arr = ["🤯","👽","🤷‍♀️","😑","🙄","😴","🤨","😨"]
    let num = Math.floor(Math.random() * 8)
    if(num < Arr.length){
        return Arr[num]
    }else{
        getEmoji()
    }
}
function redirect(){
    alert("❌ Error Occured Retry Enter the Name Again ❌")
    window.location.href = "http://127.0.0.1:5000/"
}

function update(){
    let ops="update"
    const Name = document.getElementById("up")
    const cost = document.getElementById("up1")
    const opt = document.getElementById("gpts")
    if(cost.value.trim()!="" && Name.value.trim()!=""){
        let Data = `${ops} ${Name.value} ${cost.value} ${opt.value}`
        serverInfo(Data)
    }else{
        alert(getEmoji() + " Empty Input")
    }

}
function vendor(){
    let ops = "create"
    const Name = document.getElementById("vend")
    if(Name.value.trim()!=""){
        let Data = `${ops} ${Name.value}`
        serverInfo(Data)
        
    }else{
        alert(getEmoji() + " Empty Input")
    }
}

function serverInfo(Data){
    fetch("http://127.0.0.1:5000/crud",{method:"POST","headers":{'Content-Type': 'application/json'},body:JSON.stringify(Data)})
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(err => redirect())
}