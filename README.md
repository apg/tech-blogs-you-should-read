# tech blogs to read

There was a great
[question](http://www.quora.com/Computer-Programming/What-are-the-best-programming-blogs)
on Quora (this almost never happens), which asked which are the best
tech focused blogs to read. Well, links are great, but being able to
just flat out import them into my reader is even better. So, off I
went, in the wee hours of the night to discover the RSS/Atom feeds for
them. But, of course, why should I do manual work when <link
rel="alternate"... /> exists? Doesn't everyone use that? Well, as it
turns out no. But, see quora.source.log for which feeds weren't
discovered.

## Use it

    $ pip install feedparser pyquery
    $ python discovery.py quora.source.tsv quora.xml

And, after a few minutes (it downloads the page, parses it, and then
attempts to download the discovered? feed, you'll have yourself an 
OPML file that should look like the one in this repo (I'm so nice,
I already saved you *more* time).

Feel free to fork and add, and remember, I was too lazy to get *all*
the links from that Quora post--I literally used the Firebug console
to extract them to begin with:

    $('li a.external_link').map(function (f) { 
           console.log($(f).text() + '\t' + $(f).attr('href')); });
           
but, I didn't scroll down to get all the answers loaded. (I did some
cleanup of that output in Emacs, with rectangle editing and org-tables)

