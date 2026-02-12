const api = axios.create({
    baseURL:"http;//localhost:8080"
})

const form = document.getElementById('form')
const emailInput = document.getElementById('email-input')
const password_input = document.getElementById('password-input')
const error_div = document.getElementById('error-div')
function clearError() {
  error_div.textContent = "";
  error_div.style.display = "none";
}
inputs.forEach(input => {
    input.addEventListener("input",()=>{
        clearError()
        
    })
});
form.addEventListener('submit',async(e)=>{
    e.preventDefault()
    const email = email_input.value
})