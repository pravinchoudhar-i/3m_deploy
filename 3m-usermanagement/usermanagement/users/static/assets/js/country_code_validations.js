var input = document.querySelector("#mobile"),
errorMsg = document.querySelector("#error-msg"),
validMsg = document.querySelector("#valid-msg");

// here, the index maps to the error code returned from getValidationError - see readme
var errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];

// initialise plugin
var iti = window.intlTelInput(input, {
    initialCountry: 'in',
    preferredCountries: ['in','us','gb'],
    separateDialCode:true,  
    utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/11.0.9/js/utils.js"
}); 

var updateNumber = function() {
    console.log("Entered here")
    console.log(iti.getSelectedCountryData())
    var selected_country = iti.getSelectedCountryData()
    console.log(selected_country['dialCode'])
    document.getElementById('dial-code').value = selected_country['dialCode'];
}

var reset = function() {
    input.classList.remove("error");
    errorMsg.innerHTML = "";
    errorMsg.classList.add("hide");
    validMsg.classList.add("hide");
};

// on blur: validate
input.addEventListener('blur', function() {
reset();
if (input.value.trim()) {
    
    if (iti.isValidNumber()) {
        validMsg.classList.remove("hide");
        updateNumber()
    } else {
    input.classList.add("error");
    var errorCode = iti.getValidationError();
    errorMsg.innerHTML = errorMap[errorCode];
    errorMsg.classList.remove("hide");

    }
}
});

var submit_button = $("#submit")

// on keyup / change flag: reset
input.addEventListener('change', reset);
input.addEventListener('keyup', reset);
// input.addEventListener('click',updateNumber);