const api = axios.create(
    {
        baseURL:"http://localhost:8080"
    }
)


const form = document.getElementById('gameForm')
const error_div = document.getElementById('error-div')
const checkboxes = document.querySelectorAll('input[name="games"]');
const token = localStorage.getItem('token')
const userId = localStorage.getItem('userId')

function clearError(){
    error_div.style.display = 'none'
    error_div.innerText = ''
}
checkboxes.forEach(box=>{
    box.addEventListener('change',()=>{
        clearError()
    })
})
form.addEventListener('submit',async(e)=>{
    e.preventDefault()

    const selectedCheckboxes = document.querySelectorAll('input[name="games"]:checked');

    const selectedGames = Array.from(selectedCheckboxes).map(checkbox=>{
        return checkbox.value
    })

    if(selectedGames.length===0){
        error_div.style.display = "block"
        error_div.innerText = "Select at least one game!"
        return
    }
    console.log(selectedGames);
    console.log(token);
    
    try {
        const {data} = await api.post('/games/',{
            games:selectedGames
        },{
            headers:{
                'Authorization':`Bearer ${token}`,

            }
        })
        window.location.href = "index.html"
    } catch (error) {
         error_div.style.display = "block"
        error_div.innerText = `${error.response?.data}`        
    }

    
})