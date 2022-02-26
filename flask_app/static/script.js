
let registerForm = document.getElementById('register_form')
    registerForm.onsubmit = function(e){
        // "e" is the js event happening when we submit the form.
        // e.preventDefault() is a method that stops the default nature of javascript.
        e.preventDefault();
        // create FormData object from javascript and send it through a fetch post request.
        var form = new FormData(registerForm);
        // this how we set up a post request and send the form data.
        fetch("http://127.0.0.1:5000/register", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => {
                if (data['message']=='success'){
                    console.log('made it');
                    window.location.replace("http://127.0.0.1:5000/dashboard");
                }
                else{
                    var array = data['messages'];
                    
                    for (index = 0; index < array.length; index++) {
                        let div = document.getElementById('registerError');
                        console.log(array[index]);
                        div.innerHTML += `<p>${array[index]}</p>`
                    }
                }})
            }
let loginForm = document.getElementById('login_form');
    loginForm.onsubmit = function(e){
        // "e" is the js event happening when we submit the form.
        // e.preventDefault() is a method that stops the default nature of javascript.
        e.preventDefault();
        // create FormData object from javascript and send it through a fetch post request.
        var form = new FormData(loginForm);
        // this how we set up a post request and send the form data.
        fetch("http://127.0.0.1:5000/login", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => {
                if (data['message']=='success'){
                    console.log('made it');
                    window.location.replace("http://127.0.0.1:5000/dashboard");
                }
                else{
                    // alert("login information incorrect");
                    let p = document.getElementById('loginError');
                    p.append(data['messages'][0]);
                }
            }
                )
    }