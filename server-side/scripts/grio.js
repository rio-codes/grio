function csvToArray(posts, delimiter = ',')
{
    const postHeaders = headers.slice(0, headers.indexOf("\n")).split(delimiter);
    const postFileRows = posts.slice(str.indexOf("\n")).split("\n");
    const postArray = posts.map(
        function (row) 
        { 
            const postValues = row.split(delimiter);
            const postObjects = postHeaders.reduce(
                function (object, header, index) { 
                    object[header] = values[index];
                    return object    
                }, 
                {}
            );
            return postObjects;
        }
    );
    return postArray;
}

function readCSV(file) {
    $.get(file, function(data) {
        return data
    });
}
//const reader = new FileReader();
//reader.onload = function (event) {
//    console.log(event.target.result);
//};

//window.onload = function(){
const csvFile = readCSV('grioblog.csv')
console.log("test")

//postArray = csvToArray(csvFile);

//document.write(postArray[0])
    //responseType='text';
//}



// function cb(){
//     if(this.readyState===4)document.getElementById('grio_post')
//         .innerHTML=post(this.responseText); 
// }
// function post(csv){
//     firstPost = csv.split('\n')
//     return csv.split('\n')
//             .map(
//                 function(tr,i) { 
//                     return '<tr><td>'+tr.replace(/\t/g,'</td><td>')+'</td></tr>';
//                 }
//             )
//             .join('\n'); 
// }