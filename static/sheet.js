function run() {
    const tabs = document.querySelectorAll(".tab")
    const tab_contents = document.querySelectorAll(".tab-content")

    const current_active_tab = document.querySelector("input[name=current-tab]").value;
    document.querySelector('ul.tab-container').querySelector(`li.${current_active_tab}`).classList.add("active");
    document.querySelector(`.tab-content[data-tab=${current_active_tab}]`).classList.add("active");

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
    const spell_filter_button = document.querySelector("#apply-filter-spell");
    const spells = document.querySelectorAll(".spell-in-master-list");
    const add_to_spell_list = document.querySelectorAll(".add-to-list-spells")

    const modal_items = document.querySelector(".modal.item")
    const add_item = document.querySelectorAll(".showAdd-item")
    const item_filter_button = document.querySelector("#apply-filter-item");
    const items = document.querySelectorAll(".item-in-master-list");
    const add_to_item_list = document.querySelectorAll(".add-to-list-items")

    const add_to_master_only = document.querySelector(".add-to-only-master")
    const add_custom_spell = document.querySelectorAll(".make-spell")
    
    const add_custom_item = document.querySelectorAll(".make-item")

    const picture_input = document.querySelector("#upload-image")

    picture_input.addEventListener("change", submit)

    add_to_item_list.forEach(element => {
        element.addEventListener("click", e => {
            const item_name = element.closest("p").dataset.name
            document.querySelector("input[name = add-to-item-list-name]").value = item_name
            submit()
        }) 
    });

    add_custom_item.forEach(button => {
        button.addEventListener("click", e=>{
            if(document.querySelector("#add-custom-item").classList.contains("hidden")){
                document.querySelector("#add-custom-item").classList.remove("hidden")
                return
            }
            document.querySelector("#add-custom-item").classList.add("hidden")
        })
    })

    item_filter_button.addEventListener("click", e => {
        const itemFilterName = document.querySelector("#filter-by-name-item").value;

        items.forEach(item => {
            const itemName = item.querySelector(".name").dataset.name.toLowerCase();

            if(itemFilterName && !itemName.includes(itemFilterName)) {
                item.classList.add("hidden");
                return;
            }

            item.classList.remove("hidden");
        });
    });

    for (let button of add_item) {
        button.addEventListener("click", e => {
            if (modal_items.classList.contains("hidden")) {
                modal_items.classList.remove("hidden")
                document.querySelector("input[name = add-to-item-list-level]").value = button.id
            }
            else {
                modal_items.classList.add("hidden")
            }
        })
    }

    add_custom_spell.forEach(button => {
        button.addEventListener("click", e=>{
            if(document.querySelector("#add-custom-spell").classList.contains("hidden")){
                document.querySelector("#add-custom-spell").classList.remove("hidden")
                return
            }
            document.querySelector("#add-custom-spell").classList.add("hidden")
        })
    })

    add_to_master_only.addEventListener("click", e=>{
        document.querySelector(".add-to-only-master").value = "true"
        submit()
    })

    add_to_spell_list.forEach(element => {
        element.addEventListener("click", e => {
            const spell_name = element.closest("p").dataset.name
            document.querySelector("input[name = add-to-spell-list-name]").value = spell_name
            submit()
        }) 
    });

    spell_filter_button.addEventListener("click", e => {
        const spellFilterLevel = document.querySelector("#filter-by-level-spell").value;
        const spellFilterClass = document.querySelector("#filter-by-classes-spell").value.toLowerCase();
        const spellFilterName = document.querySelector("#filter-by-name-spell").value.toLowerCase();

        spells.forEach(spell => {
            const spellLevel = spell.querySelector(".level").querySelector("span").innerHTML.toLowerCase();
            const spellClasses = spell.querySelector(".classes").querySelector("span").innerHTML.toLowerCase();
            const spellName = spell.querySelector(".name").dataset.name.toLowerCase();

            if(spellFilterLevel && spellFilterLevel !== spellLevel) {
                spell.classList.add("hidden");
                return;
            }
            
            if(spellFilterClass && !spellClasses.includes(spellFilterClass)) {
                spell.classList.add("hidden");
                return;
            }
            
            if(spellFilterName && !spellName.includes(spellFilterName)) {
                spell.classList.add("hidden");
                return;
            }

            spell.classList.remove("hidden");
        });
    });

    for (let button of add_spell) {
        button.addEventListener("click", e => {
            if (modal_spells.classList.contains("hidden")) {
                modal_spells.classList.remove("hidden")
                document.querySelector("input[name = add-to-spell-list-level]").value = button.id
            }
            else {
                modal_spells.classList.add("hidden")
            }
        })
    }


    for (let text of text_area) {
        if (!text.classList.contains("addFeat") && !text.classList.contains("submit-not")) {
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
            if(e.target == title){
            if (title.classList.contains("active")) {
                title.classList.remove("active")
                faq_contents[index].classList.remove("active")
            }
            else {
                title.classList.add("active")
                faq_contents[index].classList.add("active")
            }}
        })
    }



    for (let tab of tabs) {

        tab.addEventListener("click", e => {

            tabs.forEach(t => t.classList.remove("active"))
            // tab.classList.add("active")

            for (let content of tab_contents) {
                content.classList.remove("active")

                if (e.target.classList.contains(content.dataset.tab)) {
                    // content.classList.add("active")
                    document.querySelector("input[name = current-tab]").value = content.dataset.tab
                    submit()
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



}

if (document.readyState !== "loading") {
    run()
}
else {
    document.addEventListener("DOMContentLoaded", () => {
        run()
    })
}