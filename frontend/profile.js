const api = axios.create({
    baseURL:"http://localhost:8080"
});

form = document.getElementById('form')
fileInput = document.getElementById('file-input')
bioInput = document.getElementById('bio-input')


form.addEventListener('submit',async(e)=>{
    e.preventDefault()
    const formData = new FormData();
    formData.append('profile_image',fileInput.files[0])
})
