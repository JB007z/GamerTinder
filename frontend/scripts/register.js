const api = axios.create({
    baseURL:"http://localhost:8080"
});

const form = document.getElementById('form')
const username_input = document.getElementById('username-input')
const email_input = document.getElementById('email-input')
const password_input = document.getElementById('password-input')
const error_div = document.getElementById('error-div')

function clearError() {
  error_div.textContent = "";
  error_div.style.display = "none";
}

inputs = [username_input,email_input,password_input]

function clearInputs(){
    inputs.forEach(input=>{
        input.value = ''
    })
}
inputs.forEach(input => {
    input.addEventListener("input",()=>{
        clearError()
        
    })
});



form.addEventListener('submit',async(e)=>{
    e.preventDefault()
    const email = email_input.value
    const username = username_input.value
    const password =password_input.value
    const platformActive = document.querySelector('input[name="platform"]:checked');
    const platform = platformActive ? platformActive.value : null;
    if(!username||!email||!password||!platform){
        error_div.style.display="block"
        error_div.textContent="All fields must be filled"
        return
    }
    const user_data ={
        username:username,
        email:email,
        raw_password:password,
        platform:platform
    }
    
    try {
        const{data} = await api.post('/register/',user_data)
        const{access_token,user} = data
        
        localStorage.setItem('token', access_token);
        localStorage.setItem('userId', user.id);
        window.location.href = "profile.html";        
        
    } catch (error) {
        error_div.style.display = "block";
    
        const status = error.response?.status;
        const data = error.response?.data;

        if (status===409){
            error_div.textContent = data?.detail
           
        }
        else if (status === 422) {
        let validationMsg = data?.detail?.[0]?.msg || "Dados inválidos.";
        validationMsg = validationMsg.replace(/^Value error, /i, "");
        error_div.textContent = validationMsg
        
    } 
    else {
        error_div.textContent = "Ocorreu um erro inesperado no servidor.";
    }
        
    }
    
}


)
