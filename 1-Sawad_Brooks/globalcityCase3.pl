#!/usr/bin/perl

# code creates a "globalcity" newspaper front page

# by sawad brooks

# Updated to modern Perl practices

# November 2024

# program creates on your computer an HTML file named "global.html"

use strict;
use warnings;
use LWP::UserAgent;

# Define an array of URLs
my @space = ("http://www.example.com", "http://www.wikipedia.org", "http://www.perl.org");

# Open the output file
open(my $file, '>', "global.html") or die("Cannot Open File: $!");

# Set autoflush for immediate output
select($file);
$| = 1;
select(STDOUT);

# Randomly pick an index for the first connection
srand;
my $cityindex = int(rand 3);

# Create a user agent object
my $ua = LWP::UserAgent->new;
$ua->timeout(10);  # Set a timeout for HTTP requests

# Iterate three times to connect to different URLs
for my $i (0..2) {
    print $file "<div style=\"position: absolute; left: " . ($i * 200) . "px; top: 0px\">";
    print "connecting $space[$cityindex] ...\n";

    my $response = $ua->get($space[$cityindex]);
    
    if ($response->is_success) {
        print $file $response->decoded_content;  # Print content directly to the file
        print ".";
    } else {
        print $file "<p>Failed to fetch $space[$cityindex]: " . $response->status_line . "</p>";
        print "Error fetching $space[$cityindex]: " . $response->status_line . "\n";
    }

    print $file "</div>";

    # Update the index to move to the next URL
    $cityindex++;
    $cityindex = 0 if $cityindex > 2;
}

# Add the head section with a title
print $file "<head><title>THREE POINTS IN SPACE - WITH HELP FROM SASSEN</title></head>";

close($file);

exit;
