let chart;

function previewImage(){
    const file = document.getElementById("imageInput").files[0];
    if(!file) return;
    const img = document.getElementById("preview");
    img.src = URL.createObjectURL(file);
    img.style.display = "block";
}

async function uploadImage(){
    const file = document.getElementById("imageInput").files[0];
    if(!file) return alert("لطفاً یک عکس انتخاب کنید.");

    const formData = new FormData();
    formData.append("image", file);

    const res = await fetch("/solve",{
        method:"POST",
        body: formData
    });

    const data = await res.json();
    if(data.error) return alert(data.error);

    document.getElementById("equation").innerText =
        "معادله تشخیص داده شده: " + data.equation;
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

document.getElementById("imageInput").addEventListener("change", previewImage);
