<?//universal email header spoofer

if($submit){

 $fp=popen("/usr/sbin/sendmail -t","w");

 fputs($fp, "$x $xx\n$y $yy\nTo: $t\nFrom: $f\nSubject: $s\n\n$b");

 pclose($fp);echo "sent";exit;

}?><PRE>UNIVERSAL EMAIL HEADER SPOOFER<FORM ACTION="<?echo $PHP_SELF?>">

<B>To:</B>        <INPUT TYPE="text" NAME="t">

<B>From:</B>      <INPUT TYPE="text" NAME="f">

<B>Subject:</B>   <INPUT TYPE="text" NAME="s">

<SELECT name="x" style="width=120">

 <OPTION>Content-Type:</OPTION>

 <OPTION>In-Reply-To:</OPTION>

 <OPTION>X-Priority:</OPTION>

</SELECT>  <INPUT TYPE="text" NAME="xx">

<INPUT TYPE="text" NAME="y" VALUE="??" style="width=120">  <INPUT TYPE="text" NAME="yy">

<B>Body:</B>

<TEXTAREA NAME="b"></TEXTAREA>

<INPUT TYPE="submit" VALUE="send" NAME="submit">