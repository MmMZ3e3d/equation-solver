

function readEquation(){
    const file = document.getElementById('imageInput').files[0];
    if(!file) return alert("عکس انتخاب کن");

    Tesseract.recognize(
        file,
        'eng',
        { logger: m => console.log(m) }
    ).then(({ data: { text } }) => {
        // تمیزکاری متن
        text = text.replace(/\n/g,' ')
                   .replace(/=/g,'=0')
                   .replace(/x/g,'*x');
        document.getElementById('polyInput').value = text;
    });
}
