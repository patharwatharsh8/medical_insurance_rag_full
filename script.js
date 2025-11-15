const API = "REPLACE_BACKEND_URL";

async function uploadPDF() {
    let file = document.getElementById("pdfInput").files[0];
    let form = new FormData();
    form.append("file", file);

    let res = await fetch(API + "/upload", {
        method: "POST",
        body: form
    });

    let data = await res.json();
    alert("Uploaded Successfully. Chunks: " + data.chunks);
}

async function ask() {
    let query = document.getElementById("query").value;

    let form = new FormData();
    form.append("query", query);

    let res = await fetch(API + "/ask", {
        method: "POST",
        body: form
    });

    let data = await res.json();
    document.getElementById("responseBox").innerText = data.answer;
}
