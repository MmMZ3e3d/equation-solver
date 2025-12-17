let stream;
let chart;

async function openCamera(){
  stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: "environment" }
  });
  document.getElementById("video").srcObject = stream;
}

function capture(){
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  stream.getTracks().forEach(t => t.stop());
  runOCR(canvas);
}

function normalizeEquation(text){
  const fa = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
  fa.forEach((n,i)=> text = text.replaceAll(n,i));

  return text
    .replace(/O/g,'0')
    .replace(/×/g,'*')
    .replace(/÷/g,'/')
    .replace(/−/g,'-')
    .replace(/x\s*2/g,'x^2')
    .replace(/x\s*3/g,'x^3')
    .replace(/x\s*4/g,'x^4')
    .replace(/(\d)x/g,'$1*x')
    .replace(/\s+/g,'')
    .replace(/=/g,'=0');
}

async function runOCR(canvas){
  const result = await Tesseract.recognize(canvas, 'eng');
  let raw = result.data.text;
  let equation = normalizeEquation(raw);

  document.getElementById("equation").innerText =
    "معادله تشخیص داده شده: " + equation;

  solveEquation(equation);
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
