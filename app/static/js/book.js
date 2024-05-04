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

    let listBooks = document.getElementsByClassName("list__books");
    console.log(listBooks)
    for (let value of listBooks) {
        value.classList.add("list__booksStart");
    }

}

else {
    let addr = document.getElementsByClassName("list__add");
    // console.log(add)
    for (let value of addr) {
        value.classList.remove("elemleft");
    }
}


// let markOne = document.getElementById("firstMark");
// let markTwo = document.getElementById("secondMark");

// markTwo.addEventListener("click", function() {
//     markOne.classList.add("bookChange");
// });
