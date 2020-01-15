#!/usr/bin/env perl

use 5.016;
use warnings;
use Getopt::Long;
use File::Basename;
use Data::Dumper;
use FASTX::Reader;
my $hasCSV = eval {
	require Text::CSV;
	Text::CSV->import();
	1;
};
my $opt_otu_header = '#OTUId';
my $opt_input_seqs;
my $opt_input_taxonomy;
my $opt_output_file;
my $opt_min_id = 0.8;
my $opt_verbose;
my $opt_force;
my $opt_help;
my $opt_input;
my $opt_preserve;
my $opt_separator = ",";
my $opt_first_col = '';

my $csv;
my $opt_disable_textcsv;

my $_opt = GetOptions(
    'i|input=s'          => \$opt_input_seqs,
    't|taxonomy=s'       => \$opt_input_taxonomy,
    'p|preservenames'    => \$opt_preserve,
    'm|minid=f'          => \$opt_min_id,
	'h|header=s'         => \$opt_first_col,
    'o|outputfile=s'     => \$opt_output_file,
    'v|verbose'          => \$opt_verbose,
    'help'               => \$opt_help,
		'no-text-csv'        => \$opt_disable_textcsv,
);

usage() if ($opt_help);

my $F = FASTX::Reader->new({ filename => "$opt_input_seqs"});
open (my $TAX, '<', "$opt_input_taxonomy") || die "FATAL ERROR:\n Unable to read taxonomy from $opt_input_taxonomy\n";
my $c  = 0;
my %taxonomy;
while (my $line = readline($TAX)) {
    chomp($line);
    my ($id, $tax) = split /\t/, $line;
    die "Expecting two columns:\n$line\n" if (not defined $tax);
    $tax =~s/k__/d__/;
    $tax =~s/__/:/g;
    $taxonomy{$id} = $tax;
    $c++;
}

while (my $seq = $F->getRead() ) {
    die "FATAL ERROR:\nNo annotation for $seq->{name}\n" unless ($taxonomy{ $seq->{name} });
    #>AB008314;tax=d:Bacteria,p:Firmicutes,c:Bacilli,o:Lactobacillales,
    say '>', $seq->{name} , ';tax=' , $taxonomy{ $seq->{name} }, "\n", $seq->{seq};
}
say STDERR "$c taxonomy annotations loaded";
sub usage {
    my $self = basename($0);
    say STDERR<<END;
    CONVERT USEARCH TAXONOMY TO TABBED TAXONOMY
    --------------------------------------------------

    $self [options] -t taxonomy.tab -i seqs.fa > seq-tax.fa
 
    -v, --verbose
 
END
exit;
} 