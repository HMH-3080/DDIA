Moreover, since compaction often makes segments much smaller (assuming that a key is overwritten several times on average within one segment), we can also merge several segments together at the same time as performing the compaction, as shown in Figure 3-3. Segments are never modified after they have been written, so the merged segment is written to a new file. The merging and compaction of frozen seg‐ ments can be done in a background thread, and while it is going on, we can still con‐ tinue to serve read and write requests as normal, using the old segment files. After the merging process is complete, we switch read requests to using the new merged seg‐ ment instead of the old segments—and then the old segment files can simply be deleted.

<!-- page 96 -->

Data file segment 1

<table>
<tr><th>mew: 1078</th><th>purr: 2103</th><th>purr: 2104</th><th>mew: 1079</th><th>mew: 1080</th><th>mew: 1081</th></tr>
<tr><td>purr: 2105</td><td>purr: 2106</td><td>purr: 2107</td><td>yawn: 511</td><td>purr: 2108</td><td>mew: 1082</td></tr>
<tr><td colspan="2">Data file segment 2</td><td></td><td></td><td></td><td></td></tr>
<tr><td>purr: 2109</td><td>purr: 2110</td><td>mew: 1083</td><td>scratch: 252</td><td>mew: 1084</td><td>mew: 1085</td></tr>
<tr><td>purr: 2111</td><td>mew: 1086</td><td>purr: 2112</td><td>purr: 2113</td><td>mew: 1087</td><td>purr: 2114</td></tr>
<tr><td colspan="2">) Compaction and merging process +</td><td></td><td></td><td></td><td></td></tr>
<tr><td colspan="2">Merged segments 1 and 2</td><td></td><td></td><td></td><td></td></tr>
<tr><td>yawn: 511</td><td>scratch: 252</td><td>mew: 1087</td><td>purr: 2114</td><td></td><td></td></tr>
</table>

Figure 3-3. Performing compaction and segment merging simultaneously.

Each segment now has its own in-memory hash table, mapping keys to file offsets. In order to find the value for a key, we first check the most recent segment’s hash map; if the key is not present we check the second-most-recent segment, and so on. The merging process keeps the number of segments small, so lookups don’t need to check many hash maps.

Lots of detail goes into making this simple idea work in practice. Briefly, some of the issues that are important in a real implementation are:

## File format

CSV is not the best format for a log. It’s faster and simpler to use a binary format that first encodes the length of a string in bytes, followed by the raw string (without need for escaping).

## Deleting records

If you want to delete a key and its associated value, you have to append a special deletion record to the data file (sometimes called a tombstone). When log seg‐ ments are merged, the tombstone tells the merging process to discard any previ‐ ous values for the deleted key.

## Crash recovery

If the database is restarted, the in-memory hash maps are lost. In principle, you can restore each segment’s hash map by reading the entire segment file from beginning to end and noting the offset of the most recent value for every key as you go along. However, that might take a long time if the segment files are large, which would make server restarts painful. Bitcask speeds up recovery by storing

<!-- page 97 -->

a snapshot of each segment’s hash map on disk, which can be loaded into mem‐ ory more quickly.

## Partially written records

The database may crash at any time, including halfway through appending a record to the log. Bitcask files include checksums, allowing such corrupted parts of the log to be detected and ignored.

## Concurrency control

As writes are appended to the log in a strictly sequential order, a common imple‐ mentation choice is to have only one writer thread. Data file segments are append-only and otherwise immutable, so they can be read concurrently by mul‐ tiple threads.

An append-only log seems wasteful at first glance: why don’t you update the file in place, overwriting the old value with the new value? But an append-only design turns out to be good for several reasons:

• Appending and segment merging are sequential write operations, which are gen‐ erally much faster than random writes, especially on magnetic spinning-disk hard drives. To some extent sequential writes are also preferable on flash-based solid state drives (SSDs) [4]. We will discuss this issue further in “Comparing B- Trees and LSM-Trees” on page 83.
• Concurrency and crash recovery are much simpler if segment files are appendonly or immutable. For example, you don’t have to worry about the case where a crash happened while a value was being overwritten, leaving you with a file con‐ taining part of the old and part of the new value spliced together.
• Merging old segments avoids the problem of data files getting fragmented over time.

However, the hash table index also has limitations:

• The hash table must fit in memory, so if you have a very large number of keys, you’re out of luck. In principle, you could maintain a hash map on disk, but unfortunately it is difficult to make an on-disk hash map perform well. It requires a lot of random access I/O, it is expensive to grow when it becomes full, and hash collisions require fiddly logic [5].
• Range queries are not efficient. For example, you cannot easily scan over all keys between kitty00000 and kitty99999—you’d have to look up each key individu‐ ally in the hash maps.

In the next section we will look at an indexing structure that doesn’t have those limi‐ tations.

<!-- page 98 -->

## SSTables and LSM-Trees

In Figure 3-3, each log-structured storage segment is a sequence of key-value pairs. These pairs appear in the order that they were written, and values later in the log take precedence over values for the same key earlier in the log. Apart from that, the order of key-value pairs in the file does not matter.

Now we can make a simple change to the format of our segment files: we require that the sequence of key-value pairs is sorted by key. At first glance, that requirement seems to break our ability to use sequential writes, but we’ll get to that in a moment.

We call this format Sorted String Table, or SSTable for short. We also require that each key only appears once within each merged segment file (the compaction process already ensures that). SSTables have several big advantages over log segments with hash indexes:

1. Merging segments is simple and efficient, even if the files are bigger than the available memory. The approach is like the one used in the mergesort algorithm and is illustrated in Figure 3-4: you start reading the input files side by side, look at the first key in each file, copy the lowest key (according to the sort order) to the output file, and repeat. This produces a new merged segment file, also sorted by key.

handbag: 8786 handful: 40308 handicap: 65995 handkerchief: 16324

