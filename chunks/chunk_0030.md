<table>
<tr><th colspan="2">handlebars: 3869</th><th>handprinted: 11150</th><th></th></tr>
<tr><td colspan="4">handcuffs: 2729 handful: 42307 handicap: 67884 handiwork: 16912</td></tr>
<tr><td colspan="3">handkerchief: 20952 handprinted: 15725</td><td></td></tr>
<tr><td>handful: 44662</td><td>.</td><td>handicap: 70836</td><td>handiwork: 45521 handlebars: 3869</td></tr>
<tr><td>handoff: 5741</td><td colspan="2">handprinted: 33632</td><td></td></tr>
<tr><td colspan="3">ompaction and merging process</td><td></td></tr>
<tr><td colspan="4">handbag: 8786 handcuffs: 2729 handful: 44662 handicap: 70836</td></tr>
<tr><td colspan="4">handiwork: 45521 handkerchief: 20952 handlebars: 3869 handoff: 5741</td></tr>
<tr><td colspan="2">handprinted: 33632</td><td></td><td></td></tr>
</table>

Figure 3-4. Merging several SSTable segments, retaining only the most recent value for each key.

<!-- page 99 -->

What if the same key appears in several input segments? Remember that each segment contains all the values written to the database during some period of time. This means that all the values in one input segment must be more recent than all the values in the other segment (assuming that we always merge adjacent segments). When multiple segments contain the same key, we can keep the value from the most recent segment and discard the values in older segments.

2. In order to find a particular key in the file, you no longer need to keep an index of all the keys in memory. See Figure 3-5 for an example: say you’re looking for the key handiwork, but you don’t know the exact offset of that key in the segment file. However, you do know the offsets for the keys handbag and handsome, and because of the sorting you know that handiwork must appear between those two. This means you can jump to the offset for handbag and scan from there until you find handiwork (or not, if the key is not present in the file).

<table>
<tr><th>Sparse index</th><th></th><th colspan="2">: Sorted segment file (SSTable) on disk</th></tr>
<tr><td>in memory</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td>hand: 91541 .</td></tr>
<tr><td>key</td><td>byte offset</td><td></td><td></td></tr>
<tr><td></td><td></td><td>handcuffs: 2729  handbag: 8786</td><td>handful: 44662</td></tr>
<tr><td>hammock</td><td>100491</td><td></td><td></td></tr>
<tr><td>handbag</td><td>102134</td><td>handicap: 70836</td><td>handiwork: 45521  handkerchief: 20952</td></tr>
<tr><td>handsome</td><td>104667</td><td>handlebars: 3869</td><td>handoff: 5741 handprinted: 33632</td></tr>
<tr><td>hangout</td><td>10681</td><td></td><td></td></tr>
<tr><td></td><td></td><td>handsome: 86478</td><td>handwaving: 44005 handwriting: 22846</td></tr>
</table>

Figure 3-5. An SSTable with an in-memory index.

You still need an in-memory index to tell you the offsets for some of the keys, but it can be sparse: one key for every few kilobytes of segment file is sufficient, because a few kilobytes can be scanned very quickly.i

3. Since read requests need to scan over several key-value pairs in the requested range anyway, it is possible to group those records into a block and compress it before writing it to disk (indicated by the shaded area in Figure 3-5). Each entry of the sparse in-memory index then points at the start of a compressed block. Besides saving disk space, compression also reduces the I/O bandwidth use.

i. If all keys and values had a fixed size, you could use binary search on a segment file and avoid the in-

memory index entirely. However, they are usually variable-length in practice, which makes it difficult to tell where one record ends and the next one starts if you don’t have an index.

<!-- page 100 -->

## Constructing and maintaining SSTables

Fine so far—but how do you get your data to be sorted by key in the first place? Our incoming writes can occur in any order.

Maintaining a sorted structure on disk is possible (see “B-Trees” on page 79), but maintaining it in memory is much easier. There are plenty of well-known tree data structures that you can use, such as red-black trees or AVL trees [2]. With these data structures, you can insert keys in any order and read them back in sorted order.

We can now make our storage engine work as follows:

• When a write comes in, add it to an in-memory balanced tree data structure (for example, a red-black tree). This in-memory tree is sometimes called a memtable.
• When the memtable gets bigger than some threshold—typically a few megabytes —write it out to disk as an SSTable file. This can be done efficiently because the tree already maintains the key-value pairs sorted by key. The new SSTable file becomes the most recent segment of the database. While the SSTable is being written out to disk, writes can continue to a new memtable instance.
• In order to serve a read request, first try to find the key in the memtable, then in the most recent on-disk segment, then in the next-older segment, etc.
• From time to time, run a merging and compaction process in the background to combine segment files and to discard overwritten or deleted values.

This scheme works very well. It only suffers from one problem: if the database crashes, the most recent writes (which are in the memtable but not yet written out to disk) are lost. In order to avoid that problem, we can keep a separate log on disk to which every write is immediately appended, just like in the previous section. That log is not in sorted order, but that doesn’t matter, because its only purpose is to restore the memtable after a crash. Every time the memtable is written out to an SSTable, the corresponding log can be discarded.

## Making an LSM-tree out of SSTables

The algorithm described here is essentially what is used in LevelDB [6] and RocksDB [7], key-value storage engine libraries that are designed to be embedded into other applications. Among other things, LevelDB can be used in Riak as an alternative to Bitcask. Similar storage engines are used in Cassandra and HBase [8], both of which were inspired by Google’s Bigtable paper [9] (which introduced the terms SSTable and memtable).

Originally this indexing structure was described by Patrick O’Neil et al. under the name Log-Structured Merge-Tree (or LSM-Tree) [10], building on earlier work on

<!-- page 101 -->

log-structured filesystems [11]. Storage engines that are based on this principle of merging and compacting sorted files are often called LSM storage engines.

Lucene, an indexing engine for full-text search used by Elasticsearch and Solr, uses a similar method for storing its term dictionary [12, 13]. A full-text index is much more complex than a key-value index but is based on a similar idea: given a word in a search query, find all the documents (web pages, product descriptions, etc.) that mention the word. This is implemented with a key-value structure where the key is a word (a term) and the value is the list of IDs of all the documents that contain the word (the postings list). In Lucene, this mapping from term to postings list is kept in SSTable-like sorted files, which are merged in the background as needed [14].

## Performance optimizations

