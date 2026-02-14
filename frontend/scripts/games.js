const api = axios.create(
    {
        baseURL:"http://localhost:8080"
    }
)


const form = document.getElementById('gameForm')
const error_div = document.getElementById('error-div')
const checkboxes = document.querySelectorAll('input[name="games"]');


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
        checkbox.value
    })

    if(selectedGames.length===0){
        error_div.style.display = "block"
        error_div.innerText = "Select at least one game!"
        return
    }

    
})