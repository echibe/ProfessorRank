<!DOCTYPE html>
<html>
<head>
  <title>IIT Professor Search</title>
  <link href="bootstrap-3.3.7-dist/css/bootstrap.min.css" rel="stylesheet" type = "text/css"/>
  <link href="style.css" rel="stylesheet" type = "text/css"/>
  <script type="text/javascript" src="tablesorter-master/jquery-latest.js"></script>
  <script type="text/javascript" src="tablesorter-master/jquery.tablesorter.js"></script>
</head>
<body>

<script src="filter_table.js"></script>
<script src="https://www.w3schools.com/lib/w3.js"></script>

<div class="container-fluid">
<div class="container-fluid row">
<div class="container-fluid col-sm-8 col-lg-6">
  <h2>IIT Professor Search</h2>
  <h4><small>Try searching for a professor's name or a specific class. Data is taken from IIT's course evaluation database as well as RateMyProfessor.com (RMP). You can order the table by any column by clicking on the column name.</small></h4>
</div>
</div>

<div class="container-fluid row">
<div class="container-fluid col-sm-6 col-lg-4">
  <input class="form-control" type="text" id="search_val" onkeyup="filter_table()" placeholder="Search for name or course">
  <h5><small><em>Examples: 'cs115', 'hanrath', 'arch', 'culotta + zazi'</em></small></h5>
</div>
</div>

<div class="container-fluid col-sm-12">
<table class='table table-hover table-condensed tablesorter' id='myTable'>
<thead>
<tr class="header">
    <th>Last Name</th>
    <th style="width: 10%;">First Name</th>
    <th>IIT Score</th>
    <th>RMP Score</th>
    <th>Total Score</th>
    <th><abbr title="Total number of ratings in both IIT and RMP databases.">Confidence</abbr></th>
    <th style="width:40%;">Courses</th>
</tr>
</thead>


<tbody>
<?php

$row = 1;
if (($handle = fopen("Prof.csv", "r")) !== FALSE) {
  while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
    if($row==1){
      $row++;
      continue;
    }
    $num = count($data);
    $row++;
      $id = $data[0];
      $last = $data[1];
      $first = $data[2];
      $rmp = $data[3];
      $confidence = $data[4];
      $IIT = $data[5];
      $courses = $data[6];
      $overall = $data[7];

      if($overall != ''){
        echo "<tr>";
          echo "<td>".$last."</td>";
          echo "<td>".$first."</td>";

          if($IIT == 0){
            echo "<td>".''."</td>";
          }
          else{
            echo "<td>".number_format($IIT, 2, '.', ',')."</td>";
          }

          if($rmp == 0){
            echo "<td>".''."</td>";
          }
          else{
            echo "<td>".number_format($rmp, 2, '.', ',')."</td>";
          }

          if($overall == 0){
            echo "<td>".''."</td>";
          }
          else if($overall >= 4.5){
            echo "<td><span class='label label-success'>".number_format($overall, 2, '.', ',')."</span></td>";
          }
          else if($overall <= 2.8){
            echo "<td><span class='label label-danger'>".number_format($overall, 2, '.', ',')."</span></td>";
          }
          else{
            echo "<td><span class='label label-default'>".number_format($overall, 2, '.', ',')."</span></td>";
          }


          echo "<td>".$confidence."</td>";
          echo "<td>";
          $courses = explode(' ', $courses);
          for($i = 0; $i<count($courses); $i++){
            print_r(preg_replace("/[^A-Za-z0-9 ]/", '', $courses[$i]));
            if($i != count($courses)-1){
              print_r(', ');
            }
          }
          echo "</td>";
        echo "</tr>";
      }
    }
    echo "</table>";
    }
  fclose($handle);

// // Create connection
// $conn = new mysqli($servername, $username, $password, $dbname);
// // Check connection
// if ($conn->connect_error) {
//     die("Connection failed: " . $conn->connect_error);
// }
//
// $sql = "SELECT * FROM Professors ORDER BY last";
// $result = $conn->query($sql);
//
// if ($result->num_rows > 0) {
//     // output data of each row
//     while($row = $result->fetch_assoc()) {
//       if($row['overall'] != ''){
//         echo "<tr>";
//           echo "<td>".$row['last']."</td>";
//           echo "<td>".$row['first']."</td>";
//
//           if($row['IIT_rating'] == 0){
//             echo "<td>".''."</td>";
//           }
//           else{
//             echo "<td>".number_format($row['IIT_rating'], 2, '.', ',')."</td>";
//           }
//
//           if($row['rmp_rating'] == 0){
//             echo "<td>".''."</td>";
//           }
//           else{
//             echo "<td>".number_format($row['rmp_rating'], 2, '.', ',')."</td>";
//           }
//
//           if($row['overall'] == 0){
//             echo "<td>".''."</td>";
//           }
//           else if($row['overall'] >= 4.5){
//             echo "<td><span class='label label-success'>".number_format($row['overall'], 2, '.', ',')."</span></td>";
//           }
//           else if($row['overall'] <= 2.8){
//             echo "<td><span class='label label-danger'>".number_format($row['overall'], 2, '.', ',')."</span></td>";
//           }
//           else{
//             echo "<td><span class='label label-default'>".number_format($row['overall'], 2, '.', ',')."</span></td>";
//           }
//
//           // To include those without scores
//
//           // if($row['overall_avg'] == ''){
//           //   echo "<td>".'Insufficient data'."</td>";
//           // }
//           // else{
//           //   echo "<td>".$row['overall_avg']."</td>";
//           // }
//           echo "<td>".$row['confidence']."</td>";
//           echo "<td>";
//           $courses = explode(' ', $row['courses']);
//           for($i = 0; $i<count($courses); $i++){
//             print_r(preg_replace("/[^A-Za-z0-9 ]/", '', $courses[$i]));
//             if($i != count($courses)-1){
//               print_r(', ');
//             }
//           }
//           echo "</td>";
//         echo "</tr>";
//       }
//     }
//   echo "</table>";
// } else {
//     echo "0 results";
// }
// $conn->close();


?>
</tbody>
<h5><em><small>made by Elliot Chibe | version - 1.1</small></em></h5>
<h5><em><small><a href="mailto:echibe@hawk.iit.edu?Subject=Feedback">Send feedback</a></small></em></h5>

</div>
</div>

</body>
</html>
