function toggleNav() {
    const nav = document.getElementsByClassName("nav-list")[0]
    const aClass = "active-nav"
    if (nav.classList.contains(aClass)){
        nav.classList.remove(aClass)
    } else {
        nav.classList.add(aClass)
    }        
  }



