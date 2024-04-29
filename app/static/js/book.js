let count = document.getElementsByClassName("list__book").length;
let count1 = document.getElementsByClassName("list__book");
// console.log(count)
if (count > 0) {
    console.log(count)
    let addr = document.getElementsByClassName("list__add");
    // console.log(add)
    for (let value of addr) {
        value.classList.add("elemleft");
    }

}

else {
    let addr = document.getElementsByClassName("list__add");
    // console.log(add)
    for (let value of addr) {
        value.classList.remove("elemleft");
    }
}