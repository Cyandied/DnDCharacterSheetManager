function run() {
    const tabs = document.querySelectorAll(".tab")
    const tab_contents = document.querySelectorAll(".tab-content")
    const inputs = document.querySelectorAll("input")

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

    console.log("penis")

}

if(document.readyState !== "loading"){
    run()
}
else{
    document.addEventListener("DOMContentLoaded",()=>{
        run()
    })
}