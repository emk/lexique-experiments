#!/usr/bin/perl
# Program to output lines of file in random order

# Read File
while (<>) {
	push(foo, $_);
}

# Shuffle lines
srand;
for (0..$#foo) {
	$r = rand($#foo+1);
	($foo[$r], $foo[$_]) = ($foo[$_], $foo[$r]);
}

# Print it out
for (0..$#foo) {
	print $foo[$_];
}
