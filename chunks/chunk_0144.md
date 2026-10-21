216.58.210.78 - - [27/Feb/2015:17:55:11 +0000] "GET /css/typography.css HTTP/1.1" 200 3377 "http://martin.kleppmann.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36"

(That is actually one line; it’s only broken onto multiple lines here for readability.) There’s a lot of information in that line. In order to interpret it, you need to look at the definition of the log format, which is as follows:

$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"

So, this one line of the log indicates that on February 27, 2015, at 17:55:11 UTC, the server received a request for the file /css/typography.css from the client IP address 216.58.210.78. The user was not authenticated, so $remote_user is set to a hyphen (-). The response status was 200 (i.e., the request was successful), and the response was 3,377 bytes in size. The web browser was Chrome 40, and it loaded the file because it was referenced in the page at the URL http://martin.kleppmann.com/.

## Simple Log Analysis

Various tools can take these log files and produce pretty reports about your website traffic, but for the sake of exercise, let’s build our own, using basic Unix tools. For example, say you want to find the five most popular pages on your website. You can do this in a Unix shell as follows:i

cat /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c sort -r -n head -n 5 | | o

Read the log file.

i. Some people love to point out that cat is unnecessary here, as the input file could be given directly as an argument to awk. However, the linear pipeline is more apparent when written like this.

<!-- page 414 -->

Split each line into fields by whitespace, and output only the seventh such field from each line, which happens to be the requested URL. In our example line, this request URL is /css/typography.css.

Alphabetically sort the list of requested URLs. If some URL has been requested n times, then after sorting, the file contains the same URL repeated n times in a row.

The uniq command filters out repeated lines in its input by checking whether two adjacent lines are the same. The -c option tells it to also output a counter: for every distinct URL, it reports how many times that URL appeared in the input. The second sort sorts by the number (-n) at the start of each line, which is the number of times the URL was requested. It then returns the results in reverse (-r) order, i.e. with the largest number first.

Finally, head outputs just the first five lines (-n 5) of input, and discards the rest.

The output of that series of commands looks something like this:

4189 /favicon.ico 3631 /2013/05/24/improving-security-of-ssh-private-keys.html 2124 /2012/12/05/schema-evolution-in-avro-protocol-buffers-thrift.html 1369 / 915 /css/typography.css

Although the preceding command line likely looks a bit obscure if you’re unfamiliar with Unix tools, it is incredibly powerful. It will process gigabytes of log files in a matter of seconds, and you can easily modify the analysis to suit your needs. For example, if you want to omit CSS files from the report, change the awk argument to '$7 !~ /\.css$/ {print $7}'. If you want to count top client IP addresses instead of top pages, change the awk argument to '{print $1}'. And so on.

We don’t have space in this book to explore Unix tools in detail, but they are very much worth learning about. Surprisingly many data analyses can be done in a few minutes using some combination of awk, sed, grep, sort, uniq, and xargs, and they perform surprisingly well [8].

## Chain of commands versus custom program

Instead of the chain of Unix commands, you could write a simple program to do the same thing. For example, in Ruby, it might look something like this:

<!-- page 415 -->

counts = Hash.new(0) File.open('/var/log/nginx/access.log') do |file| file.each do |line| url = line.split[6] counts[url] += 1 end end top5 = counts.map{|url, count| [count, url] }.sort.reverse[0...5] top5.each{|count, url| puts "#{count} #{url}" } counts is a hash table that keeps a counter for the number of times we’ve seen each URL. A counter is zero by default.

From each line of the log, we take the URL to be the seventh whitespaceseparated field (the array index here is 6 because Ruby’s arrays are zero-indexed).

Increment the counter for the URL in the current line of the log.

Sort the hash table contents by counter value (descending), and take the top five entries.

Print out those top five entries.

This program is not as concise as the chain of Unix pipes, but it’s fairly readable, and which of the two you prefer is partly a matter of taste. However, besides the superfi‐ cial syntactic differences between the two, there is a big difference in the execution flow, which becomes apparent if you run this analysis on a large file.

## Sorting versus in-memory aggregation

The Ruby script keeps an in-memory hash table of URLs, where each URL is mapped to the number of times it has been seen. The Unix pipeline example does not have such a hash table, but instead relies on sorting a list of URLs in which multiple occur‐ rences of the same URL are simply repeated.

Which approach is better? It depends how many different URLs you have. For most small to mid-sized websites, you can probably fit all distinct URLs, and a counter for each URL, in (say) 1 GB of memory. In this example, the working set of the job (the amount of memory to which the job needs random access) depends only on the number of distinct URLs: if there are a million log entries for a single URL, the space required in the hash table is still just one URL plus the size of the counter. If this working set is small enough, an in-memory hash table works fine—even on a laptop.

On the other hand, if the job’s working set is larger than the available memory, the sorting approach has the advantage that it can make efficient use of disks. It’s the

<!-- page 416 -->

same principle as we discussed in “SSTables and LSM-Trees” on page 76: chunks of data can be sorted in memory and written out to disk as segment files, and then mul‐ tiple sorted segments can be merged into a larger sorted file. Mergesort has sequential access patterns that perform well on disks. (Remember that optimizing for sequential I/O was a recurring theme in Chapter 3. The same pattern reappears here.)

