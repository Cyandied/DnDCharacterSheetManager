function run() {
    const modal = document.querySelector("#modal")
    const new_sheet = document.querySelector("#new-sheet")
    const modal_buttons = modal.querySelectorAll(".modal-button")
    const load_character_button = document.querySelector("#load-sheet")
    const load_character_name = document.querySelector("#load-character")

    for(let button of modal_buttons){
        button.addEventListener("click", e=>{
            modal.classList.add("hidden")
        })
    }


    new_sheet.addEventListener("click", e=> {
        modal.classList.remove("hidden")

    })

    load_character_button.addEventListener("click", e=> {
        if(load_character_name.value !== ""){
            window.location.href = `http://localhost:5000/sheet/${load_character_name.value}`
        }
        
    })

}

if(document.readyState !== "loading"){
    run()
}
else{
    document.addEventListener("DOMContentLoaded",()=>{
        run()
    })
}