function filter_table() {
  // Declare variables
  var input, filter, table, tr, td, i, j, res;
  input = document.getElementById("search_val");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  res = filter.split("+");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    // For every ith element in the table
    last_name = tr[i].getElementsByTagName("td")[0];
    first_name = tr[i].getElementsByTagName("td")[1];
    courses = tr[i].getElementsByTagName("td")[6];
    found = false;
    for(j = 0; j<res.length; j++){
      // For every jth search term
      filter = res[j].replace(" ", "");

      if (last_name) {
        if (last_name.innerHTML.toUpperCase().indexOf(filter) > -1) {
          found = true;
        }
        if (first_name.innerHTML.toUpperCase().indexOf(filter) > -1) {
          found = true;
        }
        if (courses.innerHTML.toUpperCase().indexOf(filter) > -1) {
          found = true;
        }
        if (found) {
          tr[i].style.display = "";
          break;
        }
        else{
          tr[i].style.display = "none";
        }

      }
    }
  }
}

$(function(){
  $("#myTable").tablesorter();
});
