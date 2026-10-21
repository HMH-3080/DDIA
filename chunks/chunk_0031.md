As always, a lot of detail goes into making a storage engine perform well in practice. For example, the LSM-tree algorithm can be slow when looking up keys that do not exist in the database: you have to check the memtable, then the segments all the way back to the oldest (possibly having to read from disk for each one) before you can be sure that the key does not exist. In order to optimize this kind of access, storage engines often use additional Bloom filters [15]. (A Bloom filter is a memory-efficient data structure for approximating the contents of a set. It can tell you if a key does not appear in the database, and thus saves many unnecessary disk reads for nonexistent keys.)

There are also different strategies to determine the order and timing of how SSTables are compacted and merged. The most common options are size-tiered and leveled compaction. LevelDB and RocksDB use leveled compaction (hence the name of Lev‐ elDB), HBase uses size-tiered, and Cassandra supports both [16]. In size-tiered com‐ paction, newer and smaller SSTables are successively merged into older and larger SSTables. In leveled compaction, the key range is split up into smaller SSTables and older data is moved into separate “levels,” which allows the compaction to proceed more incrementally and use less disk space.

Even though there are many subtleties, the basic idea of LSM-trees—keeping a cas‐ cade of SSTables that are merged in the background—is simple and effective. Even when the dataset is much bigger than the available memory it continues to work well. Since data is stored in sorted order, you can efficiently perform range queries (scan‐ ning all keys above some minimum and up to some maximum), and because the disk writes are sequential the LSM-tree can support remarkably high write throughput.

## B-Trees

The log-structured indexes we have discussed so far are gaining acceptance, but they are not the most common type of index. The most widely used indexing structure is quite different: the B-tree.

<!-- page 102 -->

Introduced in 1970 [17] and called “ubiquitous” less than 10 years later [18], B-trees have stood the test of time very well. They remain the standard index implementation in almost all relational databases, and many nonrelational databases use them too.

Like SSTables, B-trees keep key-value pairs sorted by key, which allows efficient keyvalue lookups and range queries. But that’s where the similarity ends: B-trees have a very different design philosophy.

The log-structured indexes we saw earlier break the database down into variable-size segments, typically several megabytes or more in size, and always write a segment sequentially. By contrast, B-trees break the database down into fixed-size blocks or pages, traditionally 4 KB in size (sometimes bigger), and read or write one page at a time. This design corresponds more closely to the underlying hardware, as disks are also arranged in fixed-size blocks.

Each page can be identified using an address or location, which allows one page to refer to another—similar to a pointer, but on disk instead of in memory. We can use these page references to construct a tree of pages, as illustrated in Figure 3-6.

<table>
<tr><th></th><th></th><th></th><th></th><th></th><th colspan="2">“Look up user_id = 251”</th></tr>
<tr><td></td><td></td><td></td><td></td><td>00</td><td>200</td><td></td></tr>
<tr><td>key &lt; 100</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>ref</td><td>111</td><td>ref 135</td><td>ref</td><td>152</td><td>169</td><td>rer | 190 | ref</td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td></td><td>270 | ref 29 | ref</td></tr>
</table>

|250 val 251 val 252 val |253 val |254 val |

Figure 3-6. Looking up a key using a B-tree index.

One page is designated as the root of the B-tree; whenever you want to look up a key in the index, you start here. The page contains several keys and references to child pages. Each child is responsible for a continuous range of keys, and the keys between the references indicate where the boundaries between those ranges lie.

In the example in Figure 3-6, we are looking for the key 251, so we know that we need to follow the page reference between the boundaries 200 and 300. That takes us to a similar-looking page that further breaks down the 200–300 range into subranges.

<!-- page 103 -->

Eventually we get down to a page containing individual keys (a leaf page), which either contains the value for each key inline or contains references to the pages where the values can be found.

The number of references to child pages in one page of the B-tree is called the branching factor. For example, in Figure 3-6 the branching factor is six. In practice, the branching factor depends on the amount of space required to store the page refer‐ ences and the range boundaries, but typically it is several hundred.

If you want to update the value for an existing key in a B-tree, you search for the leaf page containing that key, change the value in that page, and write the page back to disk (any references to that page remain valid). If you want to add a new key, you need to find the page whose range encompasses the new key and add it to that page. If there isn’t enough free space in the page to accommodate the new key, it is split into two half-full pages, and the parent page is updated to account for the new subdi‐ vision of key ranges—see Figure 3-7. ii

<table>
<tr><th>ref</th><th colspan="5">310 ref 333 ref 345</th><th>ref</th><th></th><th></th><th>(spare space)</th><th></th></tr>
<tr><td></td><td></td><td></td><td colspan="3">333 s key &lt; 345</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>333</td><td>val</td><td>335</td><td>-val</td><td>I</td><td>337</td><td>val</td><td>340</td><td>val</td><td>342</td><td>-val</td></tr>
</table>

<table>
<tr><th>After adding key 334:</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td>ref</td><td>310</td><td></td><td>ref |333</td><td>ref |337</td><td></td><td>ref</td><td>345</td><td>ref</td><td>(spare)</td></tr>
<tr><td>333 \leq key</td><td></td><td></td><td></td><td>337 \leq ke</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>333  val 334 val 335</td><td></td><td>val</td><td></td><td>spare</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td>337 val</td><td></td><td>340</td><td>val</td><td>342</td><td>val (spare space)</td></tr>
</table>

Figure 3-7. Growing a B-tree by splitting a page.

This algorithm ensures that the tree remains balanced: a B-tree with n keys always has a depth of O(log n). Most databases can fit into a B-tree that is three or four levels deep, so you don’t need to follow many page references to find the page you are look‐ ing for. (A four-level tree of 4 KB pages with a branching factor of 500 can store up to 256 TB.)

ii. Inserting a new key into a B-tree is reasonably intuitive, but deleting one (while keeping the tree balanced) is somewhat more involved [2].

<!-- page 104 -->

## Making B-trees reliable

