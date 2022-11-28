const searchWrapper = document.querySelector(".search-input");
const suggBox = searchWrapper.querySelector(".autocom-box");
document.getElementById('moviename').addEventListener('input', function() {
    // var movies=[];
    // function loadMovies(){
    //   $.getJSON('/movies', function(data, status, xhr){
    //   for (var i = 0; i < data.length; i++ ) {
    //     movies.push(data[i]);
    //   }
    // });
    // };
    // loadMovies();
    
    currMovie = this.value;
    var emptyArray = [];
    if(currMovie){
        emptyArray = movieList.filter((data)=>{
            return data.toLocaleLowerCase().includes(currMovie.toLocaleLowerCase());
        });
        // console.log(emptyArray);
        emptyArray = emptyArray.map((data)=>{
            return data = `<p onclick="select(this)"><a style="text-decoration: none">${data}</a></p>`;
        });
    } else{
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
    let listData;
    if(!emptyArray.length){
        userValue = this.value;
        listData = `<p>${userValue}</p>`;
    }else{
        listData = emptyArray.join('');
    }
    // console.log(listData)
    suggBox.innerHTML = listData;
});
function select(element){
    let selectData = element.textContent;
    // console.log(selectData);
    document.getElementById('moviename').value = selectData;
    searchWrapper.classList.remove("active");
}
