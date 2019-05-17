<?
$ip = $_SERVER['REMOTE_ADDR'];
file_put_contents("/var/www/html/reset_req", $ip.PHP_EOL, FILE_APPEND | LOCK_EX);
?>
<p>Reset request accepted for account <? echo $ip?>@lightweight.htb, please wait (up to) a minute. Your account will be deleted and added again.<p></p>Any file in your home directory will be deleted too.</p>
<?
echo date("Y/m/d H:i:s");
?>

