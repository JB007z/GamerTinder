const api = axios.create({
    baseURL:"http://localhost:8080"
})

const form = document.getElementById('form')
const emailInput = document.getElementById('email-input')
const passwordInput = document.getElementById('password-input')
const error_div = document.getElementById('error-div')
function clearError() {
  error_div.textContent = "";
  error_div.style.display = "none";
}

inputs = [emailInput,passwordInput]
inputs.forEach(input => {
    input.addEventListener("input",()=>{
        clearError()
        
    })
});
form.addEventListener('submit',async(e)=>{
    e.preventDefault()
    const email = emailInput.value
    const password = passwordInput.value

    if(!email||!password){
        error_div.style.display = "block"
        error_div.innerText = "All fields must be filled"
    }
    
    const params = new URLSearchParams()
    params.append("username",email)
    params.append("password",password)
    
    try {
        const response = await api.post('/login/',params,{

            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }
        )
        localStorage.setItem('token',response.data.access_token)
        window.location.href = "index.html";        

    } catch (error) {
        error_div.style.display = "block"
        error_div.innerText = error.response?.data.detail
        
    }

})