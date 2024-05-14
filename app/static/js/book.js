let count = document.getElementsByClassName("list__book").length;
let count1 = document.getElementsByClassName("list__book");
if (count > 0)
{
    let addr = document.getElementsByClassName("list__add");
    for (let value of addr) 
    {
        value.classList.add("elemleft");
    }
    let listBooks = document.getElementsByClassName("list__books");
    for (let value of listBooks) 
    {
        value.classList.add("list__booksStart");
    }
}
else 
{
    let addr = document.getElementsByClassName("list__add");
    for (let value of addr) 
    {
        value.classList.remove("elemleft");
    }
}
