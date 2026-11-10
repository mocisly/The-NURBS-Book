use Cwd ();
my $book_index_style = Cwd::abs_path('backmatter/book.ist');
die 'Cannot find backmatter/book.ist' unless defined $book_index_style;
$makeindex = 'makeindex -s "' . $book_index_style . '" -o %D %S';
