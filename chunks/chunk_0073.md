For queries that operate on a single partition, each node can independently execute the queries for its own partition, so query throughput can be scaled by adding more nodes. Large, complex queries can potentially be parallelized across many nodes, although this gets significantly harder.

Partitioned databases were pioneered in the 1980s by products such as Teradata and Tandem NonStop SQL [1], and more recently rediscovered by NoSQL databases and Hadoop-based data warehouses. Some systems are designed for transactional work‐ loads, and others for analytics (see “Transaction Processing or Analytics?” on page 90): this difference affects how the system is tuned, but the fundamentals of partition‐ ing apply to both kinds of workloads.

In this chapter we will first look at different approaches for partitioning large datasets and observe how the indexing of data interacts with partitioning. We’ll then talk about rebalancing, which is necessary if you want to add or remove nodes in your cluster. Finally, we’ll get an overview of how databases route requests to the right par‐ titions and execute queries.

## Partitioning and Replication

Partitioning is usually combined with replication so that copies of each partition are stored on multiple nodes. This means that, even though each record belongs to exactly one partition, it may still be stored on several different nodes for fault toler‐ ance.

A node may store more than one partition. If a leader–follower replication model is used, the combination of partitioning and replication can look like Figure 6-1. Each partition’s leader is assigned to one node, and its followers are assigned to other nodes. Each node may be the leader for some partitions and a follower for other par‐ titions.

Everything we discussed in Chapter 5 about replication of databases applies equally to replication of partitions. The choice of partitioning scheme is mostly independent of the choice of replication scheme, so we will keep things simple and ignore replica‐ tion in this chapter.

<!-- page 223 -->

<table>
<tr><th>Node 1</th><th></th><th></th><th></th><th></th><th>Node 2</th></tr>
<tr><td>Partit</td><td>itior</td><td>1</td><td>Partition 2</td><td>Partition 3</td><td>Partition 4</td></tr>
<tr><td></td><td colspan="2">ollower</td><td>Follower</td><td>Leader</td><td>Follower</td></tr>
<tr><td></td><td></td><td></td><td></td><td>Partiti</td><td>Partition 4</td></tr>
<tr><td></td><td></td><td></td><td></td><td>Follo</td><td>Leader</td></tr>
<tr><td>Node 3</td><td></td><td></td><td></td><td></td><td>Node 4</td></tr>
<tr><td></td><td></td><td></td><td></td><td>Vritin to</td><td></td></tr>
<tr><td></td><td colspan="2">= replication streams (per partition)</td><td></td><td>partition 4 Á</td><td></td></tr>
</table>

Figure 6-1. Combining replication and partitioning: each node acts as leader for some partitions and follower for other partitions.

## Partitioning of Key-Value Data

Say you have a large amount of data, and you want to partition it. How do you decide which records to store on which nodes?

Our goal with partitioning is to spread the data and the query load evenly across nodes. If every node takes a fair share, then—in theory—10 nodes should be able to handle 10 times as much data and 10 times the read and write throughput of a single node (ignoring replication for now).

If the partitioning is unfair, so that some partitions have more data or queries than others, we call it skewed. The presence of skew makes partitioning much less effective. In an extreme case, all the load could end up on one partition, so 9 out of 10 nodes are idle and your bottleneck is the single busy node. A partition with disproportion‐ ately high load is called a hot spot.

The simplest approach for avoiding hot spots would be to assign records to nodes randomly. That would distribute the data quite evenly across the nodes, but it has a big disadvantage: when you’re trying to read a particular item, you have no way of knowing which node it is on, so you have to query all nodes in parallel.

We can do better. Let’s assume for now that you have a simple key-value data model, in which you always access a record by its primary key. For example, in an oldfashioned paper encyclopedia, you look up an entry by its title; since all the entries are alphabetically sorted by title, you can quickly find the one you’re looking for.

<!-- page 224 -->

## Partitioning by Key Range

One way of partitioning is to assign a continuous range of keys (from some mini‐ mum to some maximum) to each partition, like the volumes of a paper encyclopedia (Figure 6-2). If you know the boundaries between the ranges, you can easily deter‐ mine which partition contains a given key. If you also know which partition is assigned to which node, then you can make your request directly to the appropriate node (or, in the case of the encyclopedia, pick the correct book off the shelf).

Figure 6-2. A print encyclopedia is partitioned by key range.

The ranges of keys are not necessarily evenly spaced, because your data may not be evenly distributed. For example, in Figure 6-2, volume 1 contains words starting with A and B, but volume 12 contains words starting with T, U, V, X, Y, and Z. Simply having one volume per two letters of the alphabet would lead to some volumes being much bigger than others. In order to distribute the data evenly, the partition bound‐ aries need to adapt to the data.

The partition boundaries might be chosen manually by an administrator, or the data‐ base can choose them automatically (we will discuss choices of partition boundaries in more detail in “Rebalancing Partitions” on page 209). This partitioning strategy is used by Bigtable, its open source equivalent HBase [2, 3], RethinkDB, and MongoDB before version 2.4 [4].

Within each partition, we can keep keys in sorted order (see “SSTables and LSM- Trees” on page 76). This has the advantage that range scans are easy, and you can treat the key as a concatenated index in order to fetch several related records in one query (see “Multi-column indexes” on page 87). For example, consider an application that stores data from a network of sensors, where the key is the timestamp of the measurement (year-month-day-hour-minute-second). Range scans are very useful in this case, because they let you easily fetch, say, all the readings from a particular month.

<!-- page 225 -->

However, the downside of key range partitioning is that certain access patterns can lead to hot spots. If the key is a timestamp, then the partitions correspond to ranges of time—e.g., one partition per day. Unfortunately, because we write data from the sensors to the database as the measurements happen, all the writes end up going to the same partition (the one for today), so that partition can be overloaded with writes while others sit idle [5].

