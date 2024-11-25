#!/usr/bin/perl

# Code creates a "globalcity" newspaper front page

# by sawad brooks

# August 15, 2002

# Fixed version for modern Perl

use strict;
use warnings;
use Socket;

# URLs to fetch
my @space = ("www.example.com", "www.wikipedia.org", "www.perl.org");

open(my $file, '>', "global.html") or die("Cannot open file: $!");

select($file);
$| = 1;
select(STDOUT);

srand;

# Randomly select the initial URL
my $cityindex = int(rand 3);

for my $i (0..2) {
    print $file "<div style=\"position: absolute; left: " . ($i * 200) . "px; top: 0px\">";
    print "connecting $space[$cityindex] ...\n";

    my @stream = GetHTTP($space[$cityindex], "/");
    foreach my $s (@stream) {
        print $file $s;
        print ".";
    }
    print $file "</div>";

    # Update index for the next URL
    $cityindex++;
    $cityindex = 0 if $cityindex > 2;
}

# Add title to the generated HTML
print $file "<head><title>THREE POINTS IN SPACE - WITH HELP FROM SASSEN</title></head>";

close($file);
exit;

sub GetHTTP {
    my ($hostname, $doc) = @_;
    my ($line, @output);

    # Set up the socket connection
    socket(my $sock, PF_INET, SOCK_STREAM, getprotobyname('tcp')) or die "socket(): $!\n";
    my $paddr = sockaddr_in(80, inet_aton($hostname)) or die "inet_aton(): Could not resolve $hostname\n";
    connect($sock, $paddr) or die "connect(): Could not connect to $hostname: $!\n";

    select($sock);
    $| = 1;
    select(STDOUT);

    # Send the HTTP GET request
    print $sock "GET $doc HTTP/1.0\r\nHost: $hostname\r\nConnection: close\r\n\r\n";

    # Read the response headers
    do {
        $line = <$sock>;
    } until ($line =~ /^\r\n/);

    # Read the response body
    @output = <$sock>;
    close($sock);

    return @output;
}
