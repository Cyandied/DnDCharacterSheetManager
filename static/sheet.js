function run() {
    const tabs = document.querySelectorAll(".tab")
    const tab_contents = document.querySelectorAll(".tab-content")
    const inputs = document.querySelectorAll("input")
    const selectors = document.querySelectorAll("select")
    const rollHdie = document.querySelector("#roll-hit-die")
    const roll = document.querySelector("#roll")
    const faq_contents = document.querySelectorAll(".faq-content")
    const faqs_titles = document.querySelectorAll(".faq-title")
    const add_buttons = document.querySelectorAll(".showAdd")
    const remove_buttons = document.querySelectorAll(".remove")
    const form = document.querySelector("#sheet-form")
    const text_area = document.querySelectorAll("textarea")
    const modal_spells = document.querySelector(".modal.spell")
    const add_spell = document.querySelectorAll(".showAdd-spell")
    const filter_spells_button  =document.querySelector("#apply-filter-spell")
    const spells_in_master  =document.querySelectorAll(".spell-in-master-list")

    filter_spells_button.addEventListener("click", e=>{
        const look_for_level = document.querySelector("#filter-by-level-spell").value
        const look_for_class = document.querySelector("#filter-by-classes-spell").value
        const look_for_name = document.querySelector("#filter-by-name-spell").value
        if ( look_for_level !== ""){
            for(let spell of spells_in_master){
                const spell_level = spell.querySelector(".level").querySelector("span").innerHTML
                if( spell_level ==  look_for_level){
                    if(spell.classList.contains("hidden")){
                        spell.classList.remove("hidden")
                    }
                }
            }
        }
    })

    for (let button of add_spell) {
        button.addEventListener("click", e => {
            if (modal_spells.classList.contains("hidden")) {
                modal_spells.classList.remove("hidden")
            }
            else{
            modal_spells.classList.add("hidden")}
        })
    }


    for (let text of text_area) {
        if (!text.classList.contains("addFeat")) {
            text.addEventListener("focusout", submit)
        }

    }

    function removeItems(e, inputName) {
        const p = e.target.closest("p")
        const name = p.closest("div").getAttribute("name")

        document.querySelector(`input[name=delete-${inputName}-title]`).value = p.dataset.name
        document.querySelector(`input[name=delete-${inputName}-destination]`).value = name
        submit()
    }

    for (let remove_button of remove_buttons) {
        remove_button.addEventListener("click", e => {
            removeItems(e, remove_button.classList[1])
        })
    }

    for (let button of add_buttons) {
        button.addEventListener("click", e => {
            const current_faq = button.closest(".listItem")
            for (let stuff of current_faq.querySelectorAll(`.${button.id}`)) {
                if (stuff.classList.contains("hidden")) {
                    stuff.classList.remove("hidden")
                }
                else {
                    stuff.classList.add("hidden")
                }

            }
        })
    }


    for (let [index, title] of faqs_titles.entries()) {
        title.addEventListener("click", e => {
            if (title.classList[1] === "active") {
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

    rollHdie.addEventListener("click", () => {
        roll.value = "true"
        submit()
    })

    function submit() {
        form.requestSubmit()
    }

    for (let input of inputs) {
        if (input.type === "checkbox") {
            input.addEventListener("change", submit)
            continue
        }
        if (!input.classList.contains("addFeat") && !input.classList.contains("submit-not")) {
            input.addEventListener("focusout", submit)
        }

    }

    for (let selector of selectors) {
        selector.addEventListener("change", submit)
    }


}

if (document.readyState !== "loading") {
    run()
}
else {
    document.addEventListener("DOMContentLoaded", () => {
        run()
    })
}