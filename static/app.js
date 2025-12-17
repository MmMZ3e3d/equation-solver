let chart;

async function solveEquation(){
    const eq = document.getElementById("equationInput").value.trim();
    if(!eq) return alert("لطفاً یک معادله وارد کنید.");

    document.getElementById("equation").innerText = "معادله: " + eq;

    const res = await fetch("/solve",{
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({equation: eq})
    });

    const data = await res.json();
    if(data.error) return alert(data.error);

    document.getElementById("roots").innerText =
        "ریشه‌ها: " + data.roots.join(" , ");

    drawChart(data.x, data.y);
}

function drawChart(x,y){
    if(chart) chart.destroy();
    chart = new Chart(document.getElementById("chart"),{
        type:"line",
        data:{
            labels:x,
            datasets:[{data:y,borderWidth:2}]
        }
    });
}
