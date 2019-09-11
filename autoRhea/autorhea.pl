#!/usr/bin/env perl

use 5.012;
use warnings;
use Getopt::Long;
use Find::Bin qw($RealBin);
my $autorhea = self_check();


sub self_check {
	# Check this package is fine
	my $r;
	$r->{dir} = dirname($RealBin);
	my @required = ('normalize.R', 'alpha.R', 'beta.R', 'check_dependencies.R');
	for my $file (@required) {
		if (-e "$file") {
			info("Required file found: $file");
		} else {
			die "Missing required file <$file>.\n";
		}
	}
}
