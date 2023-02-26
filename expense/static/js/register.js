const usernameField = document.querySelector('#username-field');
const feedbackField = document.querySelector('.invalid_feedback')
const emailField = document.querySelector('#email-field')
const emailFeedbackField = document.querySelector('.emailFeedbackField')
const passwordField = document.querySelector('#password-field')
const usernameSuccess = document.querySelector('.username-success')
const emailSuccess = document.querySelector('.email-success')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const submitButton = document.querySelector('.submit-btn')


const handleToggle = (e) => {
    if (showPasswordToggle.textContent === 'SHOW') {
        showPasswordToggle.textContent = 'HIDE'

        passwordField.setAttribute('type', 'text')
    }else {
        showPasswordToggle.textContent = 'SHOW'

        passwordField.setAttribute('type', 'password')
    }
}
showPasswordToggle.addEventListener('click', handleToggle)


emailField.addEventListener('keyup', (e) => {

    const emailVal = e.target.value;
    emailSuccess.textContent= `Checking ${emailVal}`
    emailSuccess.style.display = 'block'; 

    emailField.classList.remove('is-invalid');
    emailFeedbackField.style.display = 'none';


    if (emailVal.length > 0) {
        // Making api calls to validate the email
        fetch('/authentication/email-validation',{
            body:JSON.stringify({email: emailVal}), method: 'Post'
        }).then((res) => res.json()).then((data) => {
            console.log('data', data)
            emailSuccess.style.display = 'none'; 
            if (data.email_error) {
                submitButton.disabled = true
                emailField.classList.add('is-invalid');

                emailFeedbackField.style.display = 'block';
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`
            }else{
                submitButton.removeAttribute('disabled')
            }
        })
    }
    
})





usernameField.addEventListener('keyup', (e) => {

    const usernameVal = e.target.value;
    usernameSuccess.textContent= `Checking ${usernameVal}`
    usernameSuccess.style.display = 'block'; 


    usernameField.classList.remove('is-invalid');
    feedbackField.style.display = 'none';


    if (usernameVal.length > 0) {
        // Making api calls to validate the user
        fetch('/authentication/validate-username',{
            body:JSON.stringify({username: usernameVal}), method: 'Post'
        }).then((res) => res.json()).then((data) => {
            console.log('data', data)
            usernameSuccess.style.display = 'none'
            if (data.username_error) {
                submitButton.disabled = true
                usernameField.classList.add('is-invalid');

                feedbackField.style.display = 'block';
                feedbackField.innerHTML = `<p>${data.username_error}</p>`
            }else{
                submitButton.removeAttribute('disabled')
            }
        })
    }
    
})