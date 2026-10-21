[54] Sergey Melnik, Andrey Gubarev, Jing Jing Long, et al.: “Dremel: Interactive Analysis of Web-Scale Datasets,” at 36th International Conference on Very Large Data Bases (VLDB), pages 330–339, September 2010. [55] Ralph Kimball and Margy Ross: The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling, 3rd edition. John Wiley & Sons, July 2013. ISBN: 978-1-118-53080-1 [56] Derrick Harris: “Why Apple, eBay, and Walmart Have Some of the Biggest Data Warehouses You’ve Ever Seen,” gigaom.com, March 27, 2013. [57] Julien Le Dem: “Dremel Made Simple with Parquet,” blog.twitter.com, Septem‐ ber 11, 2013. [58] Daniel J. Abadi, Peter Boncz, Stavros Harizopoulos, et al.: “The Design and Implementation of Modern Column-Oriented Database Systems,” Foundations and Trends in Databases, volume 5, number 3, pages 197–280, December 2013. doi: 10.1561/1900000024 [59] Peter Boncz, Marcin Zukowski, and Niels Nes: “MonetDB/X100: Hyper- Pipelining Query Execution,” at 2nd Biennial Conference on Innovative Data Systems Research (CIDR), January 2005. [60] Jingren Zhou and Kenneth A. Ross: “Implementing Database Operations Using SIMD Instructions,” at ACM International Conference on Management of Data (SIG‐ MOD), pages 145–156, June 2002. doi:10.1145/564691.564709 [61] Michael Stonebraker, Daniel J. Abadi, Adam Batkin, et al.: “C-Store: A Columnoriented DBMS,” at 31st International Conference on Very Large Data Bases (VLDB), pages 553–564, September 2005. [62] Andrew Lamb, Matt Fuller, Ramakrishna Varadarajan, et al.: “The Vertica Ana‐ lytic Database: C-Store 7 Years Later,” Proceedings of the VLDB Endowment, volume 5, number 12, pages 1790–1801, August 2012. [63] Julien Le Dem and Nong Li: “Efficient Data Storage for Analytics with Apache Parquet 2.0,” at Hadoop Summit, San Jose, June 2014. [64] Jim Gray, Surajit Chaudhuri, Adam Bosworth, et al.: “Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals,” Data Mining and Knowledge Discovery, volume 1, number 1, pages 29–53, March 2007. doi:10.1023/A:1009726021843

<!-- page 131 -->

<!-- page 132 -->

<table>
<tr><th></th><th></th><th></th></tr>
<tr><td>৬</td><td>-</td><td></td></tr>
</table>

<table>
<tr><th></th><th></th></tr>
<tr><td>n</td><td>w</td></tr>
<tr><td></td><td>Z</td></tr>
<tr><td></td><td>Q</td></tr>
<tr><td></td><td>O</td></tr>
<tr><td></td><td>u</td></tr>
<tr><td></td><td>2</td></tr>
<tr><td></td><td></td></tr>
<tr><td>-</td><td>ব</td></tr>
<tr><td></td><td>2</td></tr>
<tr><td></td><td></td></tr>
<tr><td>u</td><td></td></tr>
<tr><td>৩</td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>o</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>o</td></tr>
<tr><td></td><td></td></tr>
</table>

<!-- page 133 -->

## Encoding and Evolution

Everything changes and nothing stands still.

—Heraclitus of Ephesus, as quoted by Plato in Cratylus (360 BCE)

Applications inevitably change over time. Features are added or modified as new products are launched, user requirements become better understood, or business cir‐ cumstances change. In Chapter 1 we introduced the idea of evolvability: we should aim to build systems that make it easy to adapt to change (see “Evolvability: Making Change Easy” on page 21).

In most cases, a change to an application’s features also requires a change to data that it stores: perhaps a new field or record type needs to be captured, or perhaps existing data needs to be presented in a new way.

The data models we discussed in Chapter 2 have different ways of coping with such change. Relational databases generally assume that all data in the database conforms to one schema: although that schema can be changed (through schema migrations; i.e., ALTER statements), there is exactly one schema in force at any one point in time. By contrast, schema-on-read (“schemaless”) databases don’t enforce a schema, so the database can contain a mixture of older and newer data formats written at different times (see “Schema flexibility in the document model” on page 39).

When a data format or schema changes, a corresponding change to application code often needs to happen (for example, you add a new field to a record, and the applica‐ tion code starts reading and writing that field). However, in a large application, code changes often cannot happen instantaneously:

<!-- page 134 -->

• With server-side applications you may want to perform a rolling upgrade (also known as a staged rollout), deploying the new version to a few nodes at a time, checking whether the new version is running smoothly, and gradually working your way through all the nodes. This allows new versions to be deployed without service downtime, and thus encourages more frequent releases and better evolva‐ bility.
• With client-side applications you’re at the mercy of the user, who may not install the update for some time.

This means that old and new versions of the code, and old and new data formats, may potentially all coexist in the system at the same time. In order for the system to continue running smoothly, we need to maintain compatibility in both directions:

## Backward compatibility

Newer code can read data that was written by older code.

## Forward compatibility

Older code can read data that was written by newer code.

Backward compatibility is normally not hard to achieve: as author of the newer code, you know the format of data written by older code, and so you can explicitly handle it (if necessary by simply keeping the old code to read the old data). Forward compati‐ bility can be trickier, because it requires older code to ignore additions made by a newer version of the code.

In this chapter we will look at several formats for encoding data, including JSON, XML, Protocol Buffers, Thrift, and Avro. In particular, we will look at how they han‐ dle schema changes and how they support systems where old and new data and code need to coexist. We will then discuss how those formats are used for data storage and for communication: in web services, Representational State Transfer (REST), and remote procedure calls (RPC), as well as message-passing systems such as actors and message queues.

## Formats for Encoding Data

Programs usually work with data in (at least) two different representations:

1. In memory, data is kept in objects, structs, lists, arrays, hash tables, trees, and so on. These data structures are optimized for efficient access and manipulation by the CPU (typically using pointers).
2. When you want to write data to a file or send it over the network, you have to encode it as some kind of self-contained sequence of bytes (for example, a JSON document). Since a pointer wouldn’t make sense to any other process, this

<!-- page 135 -->

i. With the exception of some special cases, such as certain memory-mapped files or when operating directly on compressed data (as described in “Column Compression” on page 97).

ii. Note that encoding has nothing to do with encryption. We don’t discuss encryption in this book.

sequence-of-bytes representation looks quite different from the data structures that are normally used in memory.i

