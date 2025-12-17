let chart;

function previewImage(){
    const file = document.getElementById("imageInput").files[0];
    if(!file) return;
    const img = document.getElementById("preview");
    img.src = URL.createObjectURL(file);
    img.style.display = "block";
}

async function processImage(){
    const file = document.getElementById("imageInput").files[0];
    if(!file) return alert("لطفاً یک عکس انتخاب کنید.");

    const result = await Tesseract.recognize(file, 'eng');
    let raw = result.data.text;

    let equation = normalizeEquation(raw);
    document.getElementById("equation").innerText =
        "معادله تشخیص داده شده: " + equation;

    solveEquation(equation);
}

function normalizeEquation(text){
    // اعداد فارسی → انگلیسی
    const fa = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
    fa.forEach((n,i)=> text = text.replaceAll(n,i));

    // اصلاحات OCR معمول
    text = text.replace(/O/g,'0')
               .replace(/×/g,'*')
               .replace(/÷/g,'/')
               .replace(/−/g,'-');

    // توان‌ها و ضرب مخفی
    text = text.replace(/x\s*2/g,'x^2')
               .replace(/x\s*3/g,'x^3')
               .replace(/x\s*4/g,'x^4')
               .replace(/(\d)x/g,'$1*x')
               .replace(/\)\(/g,')*(');

    // حذف فاصله‌ها و مساوی
    text = text.replace(/\s+/g,'').replace(/=/g,'=0');

    return text;
}

async function solveEquation(eq){
    const res = await fetch("/solve",{
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({equation:eq})
    });

    const data = await res.json();
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

function toggleDark(){
    document.body.classList.toggle("dark");
}

document.getElementById("imageInput").addEventListener("change", previewImage);
