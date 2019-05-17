<!DOCTYPE html>
<html lang="en" >

<?php $ip=$_SERVER['REMOTE_ADDR'];?>

<head>
  <meta charset="UTF-8">
  <title>Lightweight slider evaluation page - slendr</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
  <link rel='stylesheet prefetch' href='https://fonts.googleapis.com/css?family=Roboto:100,300'>
  <link rel='stylesheet prefetch' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css'>
  <link rel="stylesheet" href="css/style.css">
</head>

<body>

<div class="slider-content">
<div class="slider-box">
<h1>List of banned IPs</h1>

<?php
$username = 'ldapuser1';
$password = 'f3ca9d298a553da117442deeb6fa932d';
$ldapconfig['host'] = 'lightweight.htb';
$ldapconfig['port'] = '389';
$ldapconfig['basedn'] = 'dc=lightweight,dc=htb';
//$ldapconfig['usersdn'] = 'cn=users';
$ds=ldap_connect($ldapconfig['host'], $ldapconfig['port']);
ldap_set_option($ds, LDAP_OPT_PROTOCOL_VERSION, 3);
ldap_set_option($ds, LDAP_OPT_REFERRALS, 0);
ldap_set_option($ds, LDAP_OPT_NETWORK_TIMEOUT, 10);

$dn="uid=ldapuser1,ou=People,dc=lightweight,dc=htb";

if ($bind=ldap_bind($ds, $dn, $password)) {
  echo("<p><i>You may or may not see this page when you are banned. </i><br><br>");
} else {
  echo("Unable to bind to server.</br>");
  echo("msg:'".ldap_error($ds)."'</br>".ldap_errno($ds)."");
  if ($bind=ldap_bind($ds)) {
    $filter = "(cn=*)";
    if (!($search=@ldap_search($ds, $ldapconfig['basedn'], $filter))) {
      echo("Unable to search ldap server<br>");
      echo("msg:'".ldap_error($ds)."'</br>");
    } else {
      $number_returned = ldap_count_entries($ds,$search);
      $info = ldap_get_entries($ds, $search);
      echo "The number of entries returned is ". $number_returned."<p>";
      for ($i=0; $i<$info["count"]; $i++) {
        var_dump($info[$i]);
      }
    }
  } else {
    echo("Unable to bind anonymously<br>");
    echo("msg:".ldap_error($ds)."<br>");
  }
}
?>

<?
include("banned.txt")
?>
<p><i>This page has been generated at <? echo date("Y/m/d H:i:s"); ?>. Data is refreshed every minute.</i>
</p>
<p></p>
<p><br><br><a href="index.php">home</a>&nbsp;&nbsp;<a href="info.php">info</a>&nbsp;&nbsp;<a href="status.php">status</a>&nbsp;&nbsp;<a href="user.php">user</a></p>
 </div>
</div>
</body>
</html>
