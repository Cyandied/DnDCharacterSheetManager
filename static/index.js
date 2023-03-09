function run() {
    const modal = document.querySelector("#modal")
    const new_sheet = document.querySelector("#new-sheet")
    const modal_buttons = modal.querySelectorAll(".modal-button")

    for(let button of modal_buttons){
        button.addEventListener("click", e=>{
            modal.classList.add("hidden")
        })
    }


    new_sheet.addEventListener("click", e=> {
        modal.classList.remove("hidden")

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