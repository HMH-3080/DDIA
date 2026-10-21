• The ability to replay historical events through the same processing engine that handles the stream of recent events. For example, log-based message brokers have the ability to replay messages (see “Replaying old messages” on page 451), and some stream processors can read input from a distributed filesystem like HDFS.
• Exactly-once semantics for stream processors—that is, ensuring that the output is the same as if no faults had occurred, even if faults did in fact occur (see “Fault Tolerance” on page 476). Like with batch processing, this requires discarding the partial output of any failed tasks.
• Tools for windowing by event time, not by processing time, since processing time is meaningless when reprocessing historical events (see “Reasoning About Time” on page 468). For example, Apache Beam provides an API for expressing such computations, which can then be run using Apache Flink or Google Cloud Dataflow.

<!-- page 521 -->

## Unbundling Databases

At a most abstract level, databases, Hadoop, and operating systems all perform the same functions: they store some data, and they allow you to process and query that data [16]. A database stores data in records of some data model (rows in tables, docu‐ ments, vertices in a graph, etc.) while an operating system’s filesystem stores data in files—but at their core, both are “information management” systems [17]. As we saw in Chapter 10, the Hadoop ecosystem is somewhat like a distributed version of Unix.

Of course, there are many practical differences. For example, many filesystems do not cope very well with a directory containing 10 million small files, whereas a database containing 10 million small records is completely normal and unremarkable. Never‐ theless, the similarities and differences between operating systems and databases are worth exploring.

Unix and relational databases have approached the information management prob‐ lem with very different philosophies. Unix viewed its purpose as presenting program‐ mers with a logical but fairly low-level hardware abstraction, whereas relational databases wanted to give application programmers a high-level abstraction that would hide the complexities of data structures on disk, concurrency, crash recovery, and so on. Unix developed pipes and files that are just sequences of bytes, whereas databases developed SQL and transactions.

Which approach is better? Of course, it depends what you want. Unix is “simpler” in the sense that it is a fairly thin wrapper around hardware resources; relational data‐ bases are “simpler” in the sense that a short declarative query can draw on a lot of powerful infrastructure (query optimization, indexes, join methods, concurrency control, replication, etc.) without the author of the query needing to understand the implementation details.

The tension between these philosophies has lasted for decades (both Unix and the relational model emerged in the early 1970s) and still isn’t resolved. For example, I would interpret the NoSQL movement as wanting to apply a Unix-esque approach of low-level abstractions to the domain of distributed OLTP data storage.

In this section I will attempt to reconcile the two philosophies, in the hope that we can combine the best of both worlds.

## Composing Data Storage Technologies

Over the course of this book we have discussed various features provided by data‐ bases and how they work, including:

• Secondary indexes, which allow you to efficiently search for records based on the value of a field (see “Other Indexing Structures” on page 85)

<!-- page 522 -->

• Materialized views, which are a kind of precomputed cache of query results (see “Aggregation: Data Cubes and Materialized Views” on page 101)
• Replication logs, which keep copies of the data on other nodes up to date (see “Implementation of Replication Logs” on page 158)
• Full-text search indexes, which allow keyword search in text (see “Full-text search and fuzzy indexes” on page 88) and which are built into some relational databases [1]

In Chapters 10 and 11, similar themes emerged. We talked about building full-text search indexes (see “The Output of Batch Workflows” on page 411), about material‐ ized view maintenance (see “Maintaining materialized views” on page 467), and about replicating changes from a database to derived data systems (see “Change Data Capture” on page 454).

It seems that there are parallels between the features that are built into databases and the derived data systems that people are building with batch and stream processors.

## Creating an index

Think about what happens when you run CREATE INDEX to create a new index in a relational database. The database has to scan over a consistent snapshot of a table, pick out all of the field values being indexed, sort them, and write out the index. Then it must process the backlog of writes that have been made since the consistent snap‐ shot was taken (assuming the table was not locked while creating the index, so writes could continue). Once that is done, the database must continue to keep the index up to date whenever a transaction writes to the table.

This process is remarkably similar to setting up a new follower replica (see “Setting Up New Followers” on page 155), and also very similar to bootstrapping change data capture in a streaming system (see “Initial snapshot” on page 455).

Whenever you run CREATE INDEX, the database essentially reprocesses the existing dataset (as discussed in “Reprocessing data for application evolution” on page 496) and derives the index as a new view onto the existing data. The existing data may be a snapshot of the state rather than a log of all changes that ever happened, but the two are closely related (see “State, Streams, and Immutability” on page 459).

## The meta-database of everything

In this light, I think that the dataflow across an entire organization starts looking like one huge database [7]. Whenever a batch, stream, or ETL process transports data from one place and form to another place and form, it is acting like the database sub‐ system that keeps indexes or materialized views up to date.

<!-- page 523 -->

Viewed like this, batch and stream processors are like elaborate implementations of triggers, stored procedures, and materialized view maintenance routines. The derived data systems they maintain are like different index types. For example, a relational database may support B-tree indexes, hash indexes, spatial indexes (see “Multicolumn indexes” on page 87), and other types of indexes. In the emerging architec‐ ture of derived data systems, instead of implementing those facilities as features of a single integrated database product, they are provided by various different pieces of software, running on different machines, administered by different teams.

