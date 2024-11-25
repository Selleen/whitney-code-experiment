#!/usr/bin/perl

# Modificado para usar LWP::Simple en lugar de Socket para manejar HTTP
use strict;
use warnings;
use LWP::Simple;

# Arreglo de URLs
my @space = ("https://www.example.com", "https://www.wikipedia.org", "https://www.perl.org");

# Abre el archivo para escribir el contenido
open(my $file, ">", "global.html") or die("Cannot open file");

print $file "<html><body>";

# Recorre las URLs y recupera el contenido
foreach my $url (@space) {
    print "Connecting to $url ...\n";
    my $content = get($url);  # Realiza la solicitud HTTP
    if (defined $content) {
        print $file "<div style=\"margin-bottom: 20px;\">\n";
        print $file "<h2>Content from $url</h2>\n";
        print $file $content;  # Escribe el contenido en el archivo
        print $file "</div>\n";
    } else {
        print $file "<div style=\"margin-bottom: 20px;\">\n";
        print $file "<h2>Failed to fetch content from $url</h2>\n";
        print $file "</div>\n";
        print "Failed to fetch content from $url\n";
    }
}

print $file "</body></html>";
close($file);

print "Finished writing to global.html\n";
