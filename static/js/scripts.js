const dropArea = document.querySelector(".drag-area");
const dropText = dropArea.querySelector("h2");
const button = dropArea.querySelector("button");
const input = dropArea.querySelector("#input-file");

let files;

button.addEventListener('click', e => {
    input.click();

});

input.addEventListener('change', (e) => {
  files = this.files;
  dropArea.classList.add("active");
  showFiles(files);
  dropArea.classList.remove("active");
});

dropArea.addEventListener("dragover", e => {
    e.preventDefault();
    dropArea.classList.add("active");
    dragText.textContent = "Arrastra y suelta imagen";
});

dropArea.addEventListener("dragleave", e => {
    e.preventDefault();
    dropArea.classList.remove("active");
    dragText.textContent = "Suelta para subir archivos"
});

dropArea.addEventListener("drop", e => {
    e.preventDefault();
    file = e.dataTransfer.files;
    showFiles(file);
    dropArea.classList.remove("active");
    dragText.textContent = "Suelta para subir archivos"
});

function showFiles(files){
    if(files.length == undefined){
        processFile(files);
    } else{
        for (const file of files) {
            processFile(file);  
        }
    }
}

function processFile(file) {
    const fileType = file.type;
    const validExtensions = ['img/jpg', 'img/png', 'img/ico', 'img/webp'];

    if(validExtensions.includes(fileType)){
        const fileReader = new FileReader();
        const id = `file-${Math.random().toString(32).substring(7)}`;

        fileReader.addEventListener('load', e => {
            const fileurl = fileReader.result;
            const image = `
            <div id="${id}" class="file-container>
                <img src="${fileurl}" alt="${file.name}" width="50px">
                <div class"status">
                    <span>${file.name}</span>
                    <span class="status-text">Loading...</span>
                </div>
            </div>
            `;
            const html = document.querySelector('#preview').innerHTML;

            document.querySelector('#preview').innerHTML = image + html;
        });

        fileReader.readAsDataURL(file);
        uploadFile(file, id);
    }else{
        alert("No es un archivo valido");
    }
}

function uploadFile(file){
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = fetch('http://localhost:5000/upload', {
            method: "POST",
            body:formData,
        }); 

        const responseText =  response.text();

        document.querySelector(`#${id} .status-text`).innerHTML = `<span class="success">Archivo subido correctamente...</span>`;
    } catch (error) {
        document.querySelector(`#${id} .status-text`).innerHTML = `<span class="failure">El archivo no pudo subirse...</span>`;
    }
}