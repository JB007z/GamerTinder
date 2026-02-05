const api = axios.create({
    baseURL:"http://localhost:8080"
});
const token = localStorage.getItem('token')
const userId = localStorage.getItem('userId')

form = document.getElementById('form')
fileInput = document.getElementById('file-input')
bioInput = document.getElementById('bio-input')


form.addEventListener('submit',async(e)=>{
    e.preventDefault()
    const formData = new FormData();
    formData.append('bio',bioInput.value)
    if(fileInput.files[0]){
        
        formData.append('profile_image',fileInput.files[0])
    }
    try {
        
        const {data} = await api.patch("/update_profile/",formData,{
            Headers:{
                'Authorization':`Bearer ${token}`,
                'Content-Type': 'multipart/form-data'
            }
        })
        console.log("Success: ",data.user);
    } catch (error) {
        console.error("Erro", error.response?.data)
    }
    
})
