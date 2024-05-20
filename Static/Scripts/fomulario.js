

const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll("#formulario input");
// expresiones regulares(se utilizan para verificar que los inputs cumplan con los requisitos indicados)
const expresiones = {
	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Permite letras, numeros, guion y guion_bajo, desde 4 a 16 caracteres
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Permite letras y espacios, pueden llevar acentos.
	password: /^.{4,12}$/, // DE 4 a 12 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/ // DE 7 a 14 numeros.
}

const validarFormulario = (e)=>{
    switch(e.target.name){
        case "usuario":
            if(expresiones.usuario.test(e.target.value)){

            }else{
                
            }
        break;
        case "password":
            console.log("funciona");
        break;
        case "password2":
            console.log("funciona");
        break;
        case "email":
            console.log("funciona");
        break;
    }
}

// Llama a la funciones seleccionadas, se ejecuta para cada input
inputs.forEach(input => {
    input.addEventListener('keyup', validarFormulario)
    input.addEventListener('blur', validarFormulario)
});

// Evita el envio de formulario al realizar submit
formulario.addEventListener("submit", (e)=>{
    e.preventDefault();
}
);