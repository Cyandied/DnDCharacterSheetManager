function run() {
    const tabs = document.querySelectorAll(".tab")
    const tab_contents = document.querySelectorAll(".tab-content")
    const inputs = document.querySelectorAll("input")
    const selectors = document.querySelectorAll("select")
    const rollHdie = document.querySelector("#roll-hit-die")
    const roll = document.querySelector("#roll")
    const faq_contents = document.querySelectorAll(".faq-content")
    const faqs_titles = document.querySelectorAll(".faq-title")
    const add_buttons = document.querySelector(".faqs").querySelectorAll("button")

    for(let button of add_buttons){
        button.addEventListener("click", e=> {
            const current_faq = button.closest(".faq")
            for(let stuff of current_faq.querySelectorAll(`.${button.id}`)){
                stuff.classList.remove("hidden")
            }
        })
    }
    
    
    for(let [index, title] of faqs_titles.entries()) {
        title.addEventListener("click", e => {
            if (title.classList[1] === "active"){
                title.classList.remove("active")
                faq_contents[index].classList.remove("active")
            }
            else {
                title.classList.add("active")
                faq_contents[index].classList.add("active")
            }
        })
    }
    
    
    
    for (let tab of tabs) {
        tab.addEventListener("click", e => {

            tabs.forEach(t => t.classList.remove("active"))
            tab.classList.add("active")

            for (let content of tab_contents) {
                content.classList.remove("active")

                if (e.target.classList[1] == content.dataset.tab) {
                    content.classList.add("active")
                }

            }

        })
    }

    rollHdie.addEventListener("click", ()=> {
        roll.value = "true"
        submit()
        roll.value = "false"
    })

    function submit(){
        const form = this.closest("form")
        form.requestSubmit()
    }

    for(let input of inputs){
        if(input.type === "checkbox"){
            input.addEventListener("change", submit)
            continue
        }
        if(!input.classList.contains("addFeat") ){
            input.addEventListener("focusout", submit)
        }

    }

    for(let selector of selectors){
        selector.addEventListener("change", submit)
    }


}

if(document.readyState !== "loading"){
    run()
}
else{
    document.addEventListener("DOMContentLoaded",()=>{
        run()
    })
}