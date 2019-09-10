#!/usr/bin/env perl

use 5.016;
use warnings;
use Getopt::Long;
use File::Basename;
use Data::Dumper;

my $hasCSV = eval {
	require Text::CSV;
	Text::CSV->import();
	1;
};
my $opt_input_file;
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
    'i|input=s'          => \$opt_input,
    'p|preservenames'    => \$opt_preserve,
    'm|minid=f'          => \$opt_min_id,
		'h|header=s'         => \$opt_first_col,
    'o|outputfile=s'     => \$opt_output_file,
    'v|verbose'          => \$opt_verbose,
    'help'               => \$opt_help,
		'no-text-csv'        => \$opt_disable_textcsv,
);

usage() if ($opt_help or not defined $ARGV[0]);
if ($hasCSV) {
	$csv = Text::CSV->new({binary => 1, eol => $/ })
    or die "Failed to create a CSV handle: $!";
} else {
	say STDERR " - Text::CSV not detected!";
}

my @ranks = (
    'Domain',   # 0
    'Phylum',   # 1
    'Class',    # 2
    'Order',    # 3
    'Family',   # 4
    'Genus',    # 5
    'Species',  # 6
);
my %rank_re = (
    '[dk]' => 'Domain',
    'p' => 'Phylum',
    'c' => 'Class',
    'o' => 'Order',
    'f' => 'Family',
    'g' => 'Genus',
    's' => 'Species',
);

my $O = *STDOUT;
my $file = $opt_input // $ARGV[0];
die "Missing input file.\n" unless (defined $file);
    say STDERR "Opening $file" if ($opt_verbose);
    open my $I, '<', "$file" || die " FATAL ERROR: Unable to read <$file>.\n";

    if ($opt_output_file) {
        open STDOUT, '>', "$opt_output_file" || die " FATAL ERROR: Unable to write to <$opt_output_file>\n";    }

    my $counter = 0;
    print_row($O, [$opt_first_col, @ranks]);
    while (my $line = readline($I) ) {
        #Zotu99  k:Bacteria(1.0000),p:Firmicutes(1.0000),c:Clostridia(1.0000),o:Clostridiales(1.0000),f:Lachnospiraceae(0.8900)  +       k:Bacteria,p:Firmicutes,c:Clostridia,o:Clostridial

        my $data;
        # Domain Phylum Class Order Family Genus Species
        my ($otu_name, $assigned_taxonomy, $strand, $compact_taxonomy) = split /\t/, $line;

        if (not $opt_preserve) {
            ($otu_name) = split /;/, $otu_name;
        }
        die " Expecting column STRAND, found \"$strand\".\n" if ($strand ne '+' and $strand ne '-');
        while ($assigned_taxonomy =~/([a-z]):(.+?)\(([0-9.]+)\)[;,]/g) {
            my $rank = $1;
            my $taxonomy = $2;
            my $identity = $3;
            last if ($identity < $opt_min_id);
            my $long_rank = expand_rank($rank);
            $data->{$long_rank} = $taxonomy;

        }
        my @row = ($otu_name, taxonomy_to_list($data));
        print_row($O, \@row);


    }


sub print_row {
	my ($fh, $array_ref) = @_;
	if ($hasCSV and not $opt_disable_textcsv)  {
		$csv->print( $fh , $array_ref);
	} else {
		say { $fh } join("$opt_separator",@{ $array_ref });
	}
}
sub expand_rank {
    my $rank = $_[0];
    die "Expecting a one character rank: got $rank\n" if (length($rank) > 1);
    foreach my $re (keys %rank_re) {
        if ($rank =~/$re/ ) {
            return $rank_re{$re};
        }
    }
}

sub usage {
    my $self = basename($0);
    say STDERR<<END;
    CONVERT USEARCH TAXONOMY TO TABBED TAXONOMY
    --------------------------------------------------

    $self [options] INPUT.TXT > OUTPUT.TAB

    -m, --minid           Minimum identity to print a rank (0.8)
    -p, --preservenames   Avoid splitting OTU name after ";"
    -v, --verbose

		The input file is a four column tsv:
		 OTU, taxonomy, strand, accepted_taxonomy
END
}
sub taxonomy_to_list {
    my $tax = $_[0];
    my @tax_array = ();

    my $output = '';
    for my $rank (@ranks) {
        my $taxonomy_value = $tax->{$rank} // '';
        push(@tax_array, $taxonomy_value);
    }

    return @tax_array;

}
