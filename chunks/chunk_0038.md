Besides only loading those columns from disk that are required for a query, we can further reduce the demands on disk throughput by compressing data. Fortunately, column-oriented storage often lends itself very well to compression.

Take a look at the sequences of values for each column in Figure 3-10: they often look quite repetitive, which is a good sign for compression. Depending on the data in the column, different compression techniques can be used. One technique that is particu‐ larly effective in data warehouses is bitmap encoding, illustrated in Figure 3-11.

<!-- page 120 -->

## Column values:

product_sk: 69| 69 69 (69||74 31 |31||31 31 |29 |30 30 31 |31 |31 68 69 (69

## Bitmap for each possible value:

product_sk=29: | 0 ||0 || 0 || 0 ||0 || 0 || 0 ||0 || 0 || 1 || 0 || 0 ||0 || 0 || 0 ||0 || 0 || 0 product_sk=30: | 0 ||0 || 0 || 0 ||0 || 0 || 0 ||0 || 0 || 0 ||1 || 1 ||0 | 0 || 0 ||0 || 0 || 0 product,sk=31: 0 0 0 0 0 |1 |1 |1 |1 0 0 0 |1 |1 |1 0 0 0 product,sk=68: |0 | 0 0 0 | 0 0 0 | 0 0 0 0 0 0 0 0 |1 0 0 product_sk=69: | 1 ||1 ||1 ||1 || 0 ||0 ||0 |0 ||0 || 0 ||0 ||0 ||0 ||0 || 0 ||0 ||1 ||1 product_sk=74: | 0 || 0 0 || 0 ||1 ||0 || 0 0 || 0 ||0 ||0 || 0 0 || 0 ||0 ||0 || 0 0

## Run-length encoding:

<table>
<tr><th>product_sk = 29:</th><th>9, 1</th><th>(9 zeros, 1 one, rest zeros)</th></tr>
<tr><td>product_sk = 30:</td><td>10, 2</td><td>(10 zeros, 2 ones, rest zeros)</td></tr>
<tr><td>product_sk = 31:</td><td>5,4, 3, 3</td><td>(5 zeros, 4 ones, 3 zeros, 3 ones, rest zeros)</td></tr>
<tr><td>product_sk = 68:</td><td>15, 1</td><td>(15 zeros, 1 one, rest zeros)</td></tr>
<tr><td>product_sk = 69:</td><td>0, 4, 12, 2</td><td>(0 zeros, 4 ones, 12 zeros, 2 ones)</td></tr>
<tr><td>product_sk = 74:</td><td>4, 1</td><td>(4 zeros, 1 one, rest zeros)</td></tr>
</table>

Figure 3-11. Compressed, bitmap-indexed storage of a single column.

Often, the number of distinct values in a column is small compared to the number of rows (for example, a retailer may have billions of sales transactions, but only 100,000 distinct products). We can now take a column with n distinct values and turn it into n separate bitmaps: one bitmap for each distinct value, with one bit for each row. The bit is 1 if the row has that value, and 0 if not.

If n is very small (for example, a country column may have approximately 200 dis‐ tinct values), those bitmaps can be stored with one bit per row. But if n is bigger, there will be a lot of zeros in most of the bitmaps (we say that they are sparse). In that case, the bitmaps can additionally be run-length encoded, as shown at the bottom of Figure 3-11. This can make the encoding of a column remarkably compact.

Bitmap indexes such as these are very well suited for the kinds of queries that are common in a data warehouse. For example:

WHERE product_sk IN (30, 68, 69):

Load the three bitmaps for product_sk = 30, product_sk = 68, and product_sk = 69, and calculate the bitwise OR of the three bitmaps, which can be done very efficiently.

<!-- page 121 -->

## WHERE product_sk = 31 AND store_sk = 3:

Load the bitmaps for product_sk = 31 and store_sk = 3, and calculate the bit‐ wise AND. This works because the columns contain the rows in the same order, so the kth bit in one column’s bitmap corresponds to the same row as the kth bit in another column’s bitmap.

There are also various other compression schemes for different kinds of data, but we won’t go into them in detail—see [58] for an overview.

Column-oriented storage and column families Cassandra and HBase have a concept of column families, which they inherited from Bigtable [9]. However, it is very misleading to call them column-oriented: within each column family, they store all columns from a row together, along with a row key, and they do not use column compression. Thus, the Bigtable model is still mostly row-oriented.

## Memory bandwidth and vectorized processing

For data warehouse queries that need to scan over millions of rows, a big bottleneck is the bandwidth for getting data from disk into memory. However, that is not the only bottleneck. Developers of analytical databases also worry about efficiently using the bandwidth from main memory into the CPU cache, avoiding branch mispredic‐ tions and bubbles in the CPU instruction processing pipeline, and making use of single-instruction-multi-data (SIMD) instructions in modern CPUs [59, 60].

Besides reducing the volume of data that needs to be loaded from disk, columnoriented storage layouts are also good for making efficient use of CPU cycles. For example, the query engine can take a chunk of compressed column data that fits comfortably in the CPU’s L1 cache and iterate through it in a tight loop (that is, with no function calls). A CPU can execute such a loop much faster than code that requires a lot of function calls and conditions for each record that is processed. Col‐ umn compression allows more rows from a column to fit in the same amount of L1 cache. Operators, such as the bitwise AND and OR described previously, can be designed to operate on such chunks of compressed column data directly. This techni‐ que is known as vectorized processing [58, 49].

## Sort Order in Column Storage

In a column store, it doesn’t necessarily matter in which order the rows are stored. It’s easiest to store them in the order in which they were inserted, since then inserting a new row just means appending to each of the column files. However, we can choose to impose an order, like we did with SSTables previously, and use that as an indexing mechanism.

<!-- page 122 -->

Note that it wouldn’t make sense to sort each column independently, because then we would no longer know which items in the columns belong to the same row. We can only reconstruct a row because we know that the kth item in one column belongs to the same row as the kth item in another column.

