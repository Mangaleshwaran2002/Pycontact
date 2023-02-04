const mode=document.querySelector(".mode");
const darkbutton=document.querySelector("#darkbutton");
const lightbutton=document.querySelector("#lightbutton");


function setcookie(name){
    mode.classList.add(name);
}

function search_animal() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('contact');
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="list-item";                 
        }
    }
}


darkbutton.addEventListener('click',()=>{
    // mode.classList.toggle("dark");
    mode.classList.add("dark");
    mode.classList.remove("light");
    // alert("dark mode is activated");
    document.cookie = "mode=dark"; 
})
lightbutton.addEventListener('click',()=>{
    // mode.classList.toggle("dark");
    // alert("dark mode is activated");
    mode.classList.remove("dark");
    document.cookie = "mode=light"; 
})



// auth page 

// auth page 