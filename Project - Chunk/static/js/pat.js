var counter = 0
var Arr = ["pat_name","long","contact_info","age_det","gender_info","long1","head_info","dis","date"]     
var warn = []
var info = {}
var total = []
var head_Details = {}
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function sendRequest(String){
    var d = ""
    const url = 'http://127.0.0.1:5000/getvendor'; // Replace with your Flask app's URL
    const response = await fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(String)
    })
   d = await response.json()
   return d
  
}
function add(){
  const sl1 = document.getElementById("sl")
  const sl2 = document.getElementById("sl1")
  counter++
  const ele = document.getElementById("List")
  const p = document.createElement("p")
  const btn = document.createElement("button")
  const inpt = document.createElement("input")
  const inp3 = document.createElement("input")
  const btn2 = document.createElement("button")
  btn2.setAttribute("class","app")
  btn2.setAttribute("id",counter)
  btn2.setAttribute("onclick","elem(event)")
  inp3.setAttribute("class","inpt_box")
  inp3.setAttribute("id",`inp3-${counter}`)
  inpt.setAttribute("class","inpt_box")
  inpt.setAttribute("placeholder","Enter the Account Head")

  inp3.setAttribute("placeholder","cost")
  inpt.setAttribute("id",`inp-${counter}`)
  btn.setAttribute("onclick","elm(event )")
  btn.setAttribute("class","app")
  btn2.textContent = " ➕ " 
  btn.textContent = "❌"
  const sp = document.createElement("button")
  sp.setAttribute("id",counter)
  sp.setAttribute("class","app")
  sp.textContent = sl1.value
  const sp2 = document.createElement("button")
  sp2.textContent = sl2.value
  sp2.setAttribute("id",`v-${counter}`)
  sp2.setAttribute("class","app")
  p.appendChild(sp)
  p.appendChild(sp2)
  p.appendChild(inpt)
  p.appendChild(inp3)
  p.appendChild(btn)
  p.appendChild(btn2)
  ele.appendChild(p)

}
function elm(event){
    total.splice(event.target.id,1)
event.target.parentElement.remove() //#FF0033
console.log(total)


}
async function elem(event){
    let count = event.target.id
    const textt = document.getElementById(`inp-${count}`).value
    const test = document.getElementById(count).textContent
    const cost = document.getElementById(`inp3-${count}`)
    const vendor_det = document.getElementById(`v-${count}`)
    let isCost = false

    String = `acchead ${textt} ${test} ${vendor_det.textContent}`    
    let res = await sendRequest(String)
    if(res == 0){
        if(cost.value.trim()==""){
            alert(`Plz Enter the Cost of the test ${test}`)
            await sleep(10000)
            elem(event)
        }else{
            String =`acchead ${textt} ${test} ${cost.value} ${vendor_det.textContent}`
            sendRequest(String)
            
        }
    }else{
        if(res !="added"){
            cost.value = res
            alert(res)
            total.push(res)
            console.log(total)
        }
        
    }
   
}
function clear_form(){
        var ack =confirm("Do you Want to Clear the Form ? ⚠️")
        if(ack){ 
            for(var j=0;j<Arr.length;j++){
                document.getElementById(Arr[j]).style.boxShadow = "None"
                document.getElementById(Arr[j]).value = ""
            }
        }
        warn = []
        info = {}
        total = []
        clearList = document.getElementById("List").innerHTML = ""
        counter = 0
}
async function eq(){
    let cal = 0
    if(counter == 0){
    alert("  ❌ Not Vendor or Test Added 🚨")
    }else{
    for(var i=1;i<=counter;i++){
    try{
        var test = document.getElementById(i)
        var ven = document.getElementById(`v-${i}`)
        test = test.textContent.toLowerCase()
        ven = ven.textContent.toLowerCase()
        String = `${test} ${ven}`
        alert(test)
        const url = 'http://127.0.0.1:5000/getvendor'; // Replace with your Flask app's URL
        fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(String)
        })
        .then(response => response.json())
        .then(data => {
            let flag =0
            let Data = data
            console.log(data)
            for(j in Data){
                if(Data[j].includes(test)){
                    flag = 1
                    cal+=Number(Data[j][1])
                }
            }
            if(flag == 0){
                Amount = prompt(`Enter the Amounter for ${test}`)
                cal+=Number(Amount)
                String = `Add ${test} ${ven} ${Amount}`
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(String)
                })
            }   
        // Handle the response data here
        })
        .catch(error => {
            console.error('Error:', error);

        });

        }catch{

        }
    }
await sleep(1000)
const dis = document.getElementById("dis")
if(total.length == 0){

}else{
    for(i in total){
        cal+=Number(total[i])
    }
}
let discount = document.getElementById("head_info").value
if(Number(discount) == 0 || Number(discount) > 100){
    dis.value = "Rs ."+ cal
}else{
    alert("Amounte : " + cal)
    dis.value = "Rs . " + (cal - discount)
}

}}
function Bruteforce(){
    alert(counter)
    for(var i=1;i<=counter;i++){
        const test = document.getElementById(i)
        const head  = document.getElementById(`inp-${i}`)
        const cost = document.getElementById(`inp3-${i}`)
        try{
            // alert(test.textContent)
            // alert(head.value)
            // alert(cost.value)
            if(head.value in head_Details){
                head_Details[head.value] += `${test.textContent}`+","+`${cost.value},`
            }else{
                head_Details[head.value] = `${test.textContent}`+","+`${cost.value},`
            }
        }catch{
          
        }
      
    }
    return head_Details
}
function action(){

    
    for(var i=0;i<Arr.length;i++){
        if(document.getElementById(Arr[i]).value.trim() == ""){
            
            
            document.getElementById(Arr[i]).style.boxShadow = "0px 0px 20px red"
            if(!warn.includes(Arr[i])){
                warn.push(Arr[i])
            }
            
        }else{
            info[Arr[i]] = document.getElementById(Arr[i]).value
            if(warn.includes(Arr[i])){
                document.getElementById(Arr[i]).style.boxShadow = "None"
                warn[warn.indexOf(Arr[i])] = ""

            }
        }
    }

    flag = 0
    for(var i in warn){
        
        if(warn[i].trim() != ""){
            flag = 1  
        }
    }
    if(flag == 1){
        alert(" ❌ Not submited")
    }else{
        alert(" 📌 ✅ Commit Request SuccessFull [ ! ]")
        let det = Bruteforce()
        info["header"] = det
        let xhr = new XMLHttpRequest()
        xhr.open('POST', '/info', true)
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.send(JSON.stringify(info));
    }
    
}