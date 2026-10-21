Our db_set function actually has pretty good performance for something that is so simple, because appending to a file is generally very efficient. Similarly to what db_set does, many databases internally use a log, which is an append-only data file. Real databases have more issues to deal with (such as concurrency control, reclaim‐ ing disk space so that the log doesn’t grow forever, and handling errors and partially written records), but the basic principle is the same. Logs are incredibly useful, and we will encounter them several times in the rest of this book.

The word log is often used to refer to application logs, where an application outputs text that describes what’s happening. In this book, log is used in the more general sense: an append-only sequence of records. It doesn’t have to be human-readable; it might be binary and intended only for other programs to read.

On the other hand, our db_get function has terrible performance if you have a large number of records in your database. Every time you want to look up a key, db_get has to scan the entire database file from beginning to end, looking for occurrences of the key. In algorithmic terms, the cost of a lookup is O(n): if you double the number of records n in your database, a lookup takes twice as long. That’s not good.

In order to efficiently find the value for a particular key in the database, we need a different data structure: an index. In this chapter we will look at a range of indexing structures and see how they compare; the general idea behind them is to keep some additional metadata on the side, which acts as a signpost and helps you to locate the data you want. If you want to search the same data in several different ways, you may need several different indexes on different parts of the data.

An index is an additional structure that is derived from the primary data. Many data‐ bases allow you to add and remove indexes, and this doesn’t affect the contents of the database; it only affects the performance of queries. Maintaining additional structures incurs overhead, especially on writes. For writes, it’s hard to beat the performance of simply appending to a file, because that’s the simplest possible write operation. Any kind of index usually slows down writes, because the index also needs to be updated every time data is written.

This is an important trade-off in storage systems: well-chosen indexes speed up read queries, but every index slows down writes. For this reason, databases don’t usually index everything by default, but require you—the application developer or database administrator—to choose indexes manually, using your knowledge of the applica‐ tion’s typical query patterns. You can then choose the indexes that give your applica‐ tion the greatest benefit, without introducing more overhead than necessary.

<!-- page 94 -->

## Hash Indexes

Let’s start with indexes for key-value data. This is not the only kind of data you can index, but it’s very common, and it’s a useful building block for more complex indexes.

Key-value stores are quite similar to the dictionary type that you can find in most programming languages, and which is usually implemented as a hash map (hash table). Hash maps are described in many algorithms textbooks [1, 2], so we won’t go into detail of how they work here. Since we already have hash maps for our inmemory data structures, why not use them to index our data on disk?

Let’s say our data storage consists only of appending to a file, as in the preceding example. Then the simplest possible indexing strategy is this: keep an in-memory hash map where every key is mapped to a byte offset in the data file—the location at which the value can be found, as illustrated in Figure 3-1. Whenever you append a new key-value pair to the file, you also update the hash map to reflect the offset of the data you just wrote (this works both for inserting new keys and for updating existing keys). When you want to look up a value, use the hash map to find the offset in the data file, seek to that location, and read the value.

<table>
<tr><th>key</th><th>byte offset</th><th>In-memory hash map</th></tr>
<tr><td>123456 0p</td><td></td><td></td></tr>
<tr><td>42.</td><td>64 p</td><td>Log-structured file on disk</td></tr>
<tr><td></td><td></td><td>(each box is one byte)</td></tr>
<tr><td colspan="3">$|1\||2|3|4|5|6\|_{j|{|{n}|n|a|m|e\|{"}|:\right|{}|L|o|n|d|o|n\|^{n|,|{|a|t\|t|x|a|$</td></tr>
<tr><td></td><td></td><td>20</td></tr>
<tr><td colspan="3">$ct\||{k|o\|n|s\||n|:|\||{|\|B|{|g|-|B|e\|n\|^{n}|,}\|^{}|{\right|\infty|n|d|o\|n||B|y|e$</td></tr>
<tr><td colspan="3">30 $"|)|)\left|0\right|4\||2\|,|(|{|n|a\left|m\||e\|{}\right|z|{|S|a|n|-|F|x|a|n\||c\||{k}|s|c|\infty|{n\right|$</td></tr>
<tr><td></td><td></td><td>80</td></tr>
<tr><td colspan="3">$,{\right|a|t\right|t\right|x|a|e\left|k|\infty|n\right|s\||^{}|\tau\right|\||{|G|o|1|d|e|n||G|a|t\right|e||\||B\right)$</td></tr>
<tr><td>90</td><td></td><td></td></tr>
<tr><td>\pi|i|d|g|e|"|]|)||n\right)$</td><td></td><td></td></tr>
<tr><td>120</td><td></td><td></td></tr>
</table>

Figure 3-1. Storing a log of key-value pairs in a CSV-like format, indexed with an inmemory hash map.

This may sound simplistic, but it is a viable approach. In fact, this is essentially what Bitcask (the default storage engine in Riak) does [3]. Bitcask offers high-performance reads and writes, subject to the requirement that all the keys fit in the available RAM, since the hash map is kept completely in memory. The values can use more space than there is available memory, since they can be loaded from disk with just one disk

<!-- page 95 -->

seek. If that part of the data file is already in the filesystem cache, a read doesn’t require any disk I/O at all.

A storage engine like Bitcask is well suited to situations where the value for each key is updated frequently. For example, the key might be the URL of a cat video, and the value might be the number of times it has been played (incremented every time someone hits the play button). In this kind of workload, there are a lot of writes, but there are not too many distinct keys—you have a large number of writes per key, but it’s feasible to keep all keys in memory.

As described so far, we only ever append to a file—so how do we avoid eventually running out of disk space? A good solution is to break the log into segments of a cer‐ tain size by closing a segment file when it reaches a certain size, and making subse‐ quent writes to a new segment file. We can then perform compaction on these segments, as illustrated in Figure 3-2. Compaction means throwing away duplicate keys in the log, and keeping only the most recent update for each key.

<table>
<tr><th>Data file segment</th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td>mew: 1078</td><td>purr: 2103</td><td>purr: 2104</td><td>mew: 1079</td><td>mew: 1080</td><td>mew: 1081</td></tr>
<tr><td>purr: 2105</td><td>purr: 2106</td><td>purr: 2107</td><td>yawn: 511</td><td>purr: 2108</td><td>mew: 1082</td></tr>
</table>

<table>
<tr><th colspan="2">Compacted segment</th><th></th></tr>
<tr><td>yawn: 511</td><td>mew: 1082</td><td>purr: 2108</td></tr>
</table>

) Compaction process

Figure 3-2. Compaction of a key-value update log (counting the number of times each cat video was played), retaining only the most recent value for each key.

