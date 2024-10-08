function generatereport(){
    const st = document.getElementById("start")
    const end =document.getElementById("end")
    const ven = document.getElementById("vendor")
    Data = `${st.value} ${end.value} ${ven.value}`
    fetch("http://127.0.0.1:5000/genreport",{method:"POST","headers":{'Content-Type': 'application/json'},body:JSON.stringify(Data)})
        .then(response => response.json())
        .then(data => alert(data))
        .catch(err => redirect())
}