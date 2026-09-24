const api = axios.create({
    baseURL:"http://localhost:8080"
});
const token = localStorage.getItem('token')
const userId = localStorage.getItem('userId')

const form = document.getElementById('form')
const fileInput = document.getElementById('file-input')
const bioInput = document.getElementById('bio-input')
const previewImg = document.getElementById('preview')

function previewImage(event){
    const file = event.target.files[0]
    if(file){
        previewImg.src = URL.createObjectURL(file)  
    }
}

form.addEventListener('submit',async(e)=>{
    e.preventDefault()
    const formData = new FormData();
    formData.append('bio',bioInput.value)
    if(fileInput.files[0]){
        
        formData.append('profile_image',fileInput.files[0])
    }
    try {
        
        const {data} = await api.patch("/update_profile/",formData,{
            headers:{
                'Authorization':`Bearer ${token}`,
                'Content-Type': 'multipart/form-data'
            }
        })
        console.log("Success: ",data.user);
        window.location.href = "games.html";        

    } catch (error) {
        console.error("Erro", error.response?.data)
    }
    
})
