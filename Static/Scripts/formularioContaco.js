document.addEventListener('DOMContentLoaded', function() {
    var inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="file"]');

    inputs.forEach(function(input) {
        input.addEventListener('input', function() {
            validateField(input);
        });
        input.addEventListener('blur', function() {
            validateField(input);
        });
    });

    function validateField(input) {
        var errorMessage = "";
        clearError(input);

        if (input.id === "name" && input.value.trim() === "") {
            setError(input, "El nombre es obligatorio.");
        }

        if (input.id === "email") {
            if (input.value.trim() === "") {
                setError(input, "El email es obligatorio.");
            } else {
                var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(input.value)) {
                    setError(input, "Por favor, ingresa un email válido.");
                }
            }
        }

        if (input.id === "image" && input.value.trim() === "") {
            setError(input, "La carga de una imagen es obligatoria.");
        }
    }

    function setError(element, message) {
        element.classList.add("input-error");
        var icon = element.nextElementSibling;
        if (icon && icon.classList.contains("icon")) {
            icon.classList.add("show-icon");
        }
    }

    function clearError(element) {
        element.classList.remove("input-error");
        var icon = element.nextElementSibling;
        if (icon && icon.classList.contains("icon")) {
            icon.classList.remove("show-icon");
        }
    }

    document.querySelector('form').addEventListener('submit', function(event) {
        var name = document.getElementById("name");
        var email = document.getElementById("email");
        var image = document.getElementById("image");
        var serviceDogWalking = document.getElementById("dog-walking").checked;
        var servicePetSitting = document.getElementById("pet-sitting").checked;
        var errorMessage = "";
        var isValid = true;

        clearError(name);
        clearError(email);
        clearError(image);

        if (name.value.trim() === "") {
            setError(name, "El nombre es obligatorio.");
            isValid = false;
        }

        if (email.value.trim() === "") {
            setError(email, "El email es obligatorio.");
            isValid = false;
        } else {
            var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email.value)) {
                setError(email, "Por favor, ingresa un email válido.");
                isValid = false;
            }
        }

        if (image.value.trim() === "") {
            setError(image, "La carga de una imagen es obligatoria.");
            isValid = false;
        }

        if (!serviceDogWalking && !servicePetSitting) {
            errorMessage += "Por favor, selecciona un tipo de servicio.\n";
            isValid = false;
        }

        if (!isValid) {
            document.getElementById("error-message").innerText = errorMessage;
            event.preventDefault();
        }
    });
});