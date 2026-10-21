Rather, the data needs to be sorted an entire row at a time, even though it is stored by column. The administrator of the database can choose the columns by which the table should be sorted, using their knowledge of common queries. For example, if queries often target date ranges, such as the last month, it might make sense to make date_key the first sort key. Then the query optimizer can scan only the rows from the last month, which will be much faster than scanning all rows.

A second column can determine the sort order of any rows that have the same value in the first column. For example, if date_key is the first sort key in Figure 3-10, it might make sense for product_sk to be the second sort key so that all sales for the same product on the same day are grouped together in storage. That will help queries that need to group or filter sales by product within a certain date range.

Another advantage of sorted order is that it can help with compression of columns. If the primary sort column does not have many distinct values, then after sorting, it will have long sequences where the same value is repeated many times in a row. A simple run-length encoding, like we used for the bitmaps in Figure 3-11, could compress that column down to a few kilobytes—even if the table has billions of rows.

That compression effect is strongest on the first sort key. The second and third sort keys will be more jumbled up, and thus not have such long runs of repeated values. Columns further down the sorting priority appear in essentially random order, so they probably won’t compress as well. But having the first few columns sorted is still a win overall.

## Several different sort orders

A clever extension of this idea was introduced in C-Store and adopted in the com‐ mercial data warehouse Vertica [61, 62]. Different queries benefit from different sort orders, so why not store the same data sorted in several different ways? Data needs to be replicated to multiple machines anyway, so that you don’t lose data if one machine fails. You might as well store that redundant data sorted in different ways so that when you’re processing a query, you can use the version that best fits the query pattern.

Having multiple sort orders in a column-oriented store is a bit similar to having mul‐ tiple secondary indexes in a row-oriented store. But the big difference is that the roworiented store keeps every row in one place (in the heap file or a clustered index), and secondary indexes just contain pointers to the matching rows. In a column store, there normally aren’t any pointers to data elsewhere, only columns containing values.

<!-- page 123 -->

## Writing to Column-Oriented Storage

These optimizations make sense in data warehouses, because most of the load con‐ sists of large read-only queries run by analysts. Column-oriented storage, compres‐ sion, and sorting all help to make those read queries faster. However, they have the downside of making writes more difficult.

An update-in-place approach, like B-trees use, is not possible with compressed col‐ umns. If you wanted to insert a row in the middle of a sorted table, you would most likely have to rewrite all the column files. As rows are identified by their position within a column, the insertion has to update all columns consistently.

Fortunately, we have already seen a good solution earlier in this chapter: LSM-trees. All writes first go to an in-memory store, where they are added to a sorted structure and prepared for writing to disk. It doesn’t matter whether the in-memory store is row-oriented or column-oriented. When enough writes have accumulated, they are merged with the column files on disk and written to new files in bulk. This is essen‐ tially what Vertica does [62].

Queries need to examine both the column data on disk and the recent writes in mem‐ ory, and combine the two. However, the query optimizer hides this distinction from the user. From an analyst’s point of view, data that has been modified with inserts, updates, or deletes is immediately reflected in subsequent queries.

## Aggregation: Data Cubes and Materialized Views

Not every data warehouse is necessarily a column store: traditional row-oriented databases and a few other architectures are also used. However, columnar storage can be significantly faster for ad hoc analytical queries, so it is rapidly gaining popularity [51, 63].

Another aspect of data warehouses that is worth mentioning briefly is materialized aggregates. As discussed earlier, data warehouse queries often involve an aggregate function, such as COUNT, SUM, AVG, MIN, or MAX in SQL. If the same aggregates are used by many different queries, it can be wasteful to crunch through the raw data every time. Why not cache some of the counts or sums that queries use most often?

One way of creating such a cache is a materialized view. In a relational data model, it is often defined like a standard (virtual) view: a table-like object whose contents are the results of some query. The difference is that a materialized view is an actual copy of the query results, written to disk, whereas a virtual view is just a shortcut for writ‐ ing queries. When you read from a virtual view, the SQL engine expands it into the view’s underlying query on the fly and then processes the expanded query.

When the underlying data changes, a materialized view needs to be updated, because it is a denormalized copy of the data. The database can do that automatically, but

<!-- page 124 -->

such updates make writes more expensive, which is why materialized views are not often used in OLTP databases. In read-heavy data warehouses they can make more sense (whether or not they actually improve read performance depends on the indi‐ vidual case).

A common special case of a materialized view is known as a data cube or OLAP cube [64]. It is a grid of aggregates grouped by different dimensions. Figure 3-12 shows an example.

<table>
<tr><th>SELECT SUM(net_price)</th><th></th><th></th><th></th><th>SELECT SUM(net_price)</th><th></th></tr>
<tr><td>FROM fact sales</td><td></td><td></td><td></td><td>FROM fact_sales</td><td></td></tr>
<tr><td>key = 140101 WHERE date</td><td></td><td></td><td></td><td>WHERE date_key = 140101</td><td></td></tr>
<tr><td>duct_sk = 32 AND pr</td><td colspan="2">product_sk</td><td></td><td></td><td></td></tr>
<tr><td></td><td>32</td><td>33</td><td>34</td><td>35</td><td>total</td></tr>
<tr><td>140101</td><td colspan="4">149.60-(F)-31.01-(+-84.58-(+-28.18 -(F) (+)</td><td>40710.53 (+)</td></tr>
<tr><td>140102</td><td>132.18</td><td>19.78</td><td>82.91</td><td>10.96</td><td>73091.28</td></tr>
<tr><td></td><td>(+)</td><td></td><td></td><td></td><td>(+)</td></tr>
<tr><td>140103</td><td>196.75</td><td>0.00</td><td>12.52</td><td>64.67</td><td>54688.10</td></tr>
<tr><td></td><td>(+)</td><td></td><td></td><td></td><td>(f)</td></tr>
<tr><td>140104</td><td>178.36</td><td>9.98</td><td>88.75</td><td>56.16</td><td>95121.09</td></tr>
<tr><td>A(net_price) SELE</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>• •</td></tr>
<tr><td>FROM fac sales</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>ct WHERE</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>total</td><td>14967.09</td><td>5910.43</td><td>7328.85</td><td>6885.39</td><td>lots</td></tr>
</table>

Figure 3-12. Two dimensions of a data cube, aggregating data by summing.

