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
    if(!username||!email|!password){
        error_div.style.display="block"
        error_div.textContent="All fields must be filled"
        return
    }
    const user_data ={
        username:username,
        email:email,
        raw_password:password
    }
    
    try {
        const{data} = await api.post('/register',user_data)
        console.log(data);
        
        
    } catch (error) {
        console.error(error.response?.data || error.message);
        
    }
    
}


)
