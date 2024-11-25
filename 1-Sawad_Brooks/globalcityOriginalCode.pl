#!/usr/bin/perl

# code creates a "globalcity" newspaper front page

# by sawad brooks

# august 15, 2002

# program creates on your computer an HTML file named "global.html"



use Socket;

#@space = ("www.nytimes.com", "www.theguardian.com/uk", "www.asahi.com");
@space = ("http://www.example.com", "http://www.wikipedia.org", "http://www.perl.org");

open(FILE,">global.html") || die("Cannot Open File");

select(FILE); $| = 1; select(STDOUT);

srand;

$cityindex = int(rand 3);

print FILE "<div style=\"position: absolute; left: 0px; top: 0px\">";

print "connecting $space[$cityindex] ...";

@stream = &GetHTTP($space[$cityindex], "/");

foreach $s (@stream) { print FILE $s; print "."; }

print FILE "<\div>";

$cityindex++; if ($cityindex > 2) { $cityindex = 0; }

print FILE "<div style=\"position: absolute; left: 200px; top: 0px\">";

print "connecting $space[$cityindex] ...";

@stream = &GetHTTP($space[$cityindex], "/");

foreach $s (@stream) { print FILE $s; print "."; }

print FILE "<\div>";

$cityindex++; if ($cityindex > 2) { $cityindex = 0; }

print FILE "<div style=\"position: absolute; left: 400px; top: 0px\">";

print "connecting $space[$cityindex] ...";

@stream = &GetHTTP($space[$cityindex], "/");

foreach $s (@stream) { print FILE $s; print "."; }

print FILE "<\div>";

print FILE "<head><title>THREE POINTS IN SPACE - WITH HELP FROM

SASSEN<\title><\head>";

exit;

sub GetHTTP {

	local($hostname, $doc) = @_;

	local($port, $iaddr, $paddr, $proto, $line, @output);

	# ignore the "host:port" notation, and assume http=80 everytime.

	socket(SOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp')) || die

	"socket(): $!\n";

	$paddr = sockaddr_in(80, inet_aton($hostname));

	connect(SOCK, $paddr) || die "connect(): $!\n";

	select (SOCK); $| = 1; select(STDOUT);

	# send the HTTP-Request

	print SOCK "GET $doc HTTP/1.0\n\n";

	# now read the entire response:

	do { $line = <SOCK> } until ($line =~ /^\r\n/);

	@output = <SOCK>;

	close(SOCK);

	return @output;

}