Only entire partitions are moved between nodes. The number of partitions does not change, nor does the assignment of keys to partitions. The only thing that changes is the assignment of partitions to nodes. This change of assignment is not immediate — it takes some time to transfer a large amount of data over the network—so the old assignment of partitions is used for any reads and writes that happen while the trans‐ fer is in progress.

<!-- page 233 -->

Before rebalancing (4 nodes in cluster)

<table>
<tr><th>Node 0</th><th>Node 1</th><th></th><th></th><th>Node 2</th><th></th><th></th><th colspan="2">Node 3</th><th></th></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>p2 p6 p10 p14 p18</td><td></td><td colspan="3">p3 p7 p11 p15 p19</td></tr>
<tr><td>p0</td><td>p17</td><td>p2</td><td>р6</td><td>p10 p18</td><td>p3.</td><td>p7 p11 p15</td><td>p4</td><td>p9.</td><td>p14 p19</td></tr>
<tr><td>Node 0</td><td>Node 1</td><td colspan="2">Node 2</td><td></td><td>Node 3</td><td></td><td colspan="2">Node 4</td><td></td></tr>
<tr><td colspan="3">After rebalancing (5 nodes in cluster)</td><td></td><td>Legend:</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td>--</td><td colspan="5">- - - - partition remains on the same node</td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td colspan="5">► partition migrated to another node</td></tr>
</table>

Figure 6-6. Adding a new node to a database cluster with multiple partitions per node.

In principle, you can even account for mismatched hardware in your cluster: by assigning more partitions to nodes that are more powerful, you can force those nodes to take a greater share of the load.

This approach to rebalancing is used in Riak [15], Elasticsearch [24], Couchbase [10], and Voldemort [25].

In this configuration, the number of partitions is usually fixed when the database is first set up and not changed afterward. Although in principle it’s possible to split and merge partitions (see the next section), a fixed number of partitions is operationally simpler, and so many fixed-partition databases choose not to implement partition splitting. Thus, the number of partitions configured at the outset is the maximum number of nodes you can have, so you need to choose it high enough to accommo‐ date future growth. However, each partition also has management overhead, so it’s counterproductive to choose too high a number.

Choosing the right number of partitions is difficult if the total size of the dataset is highly variable (for example, if it starts small but may grow much larger over time). Since each partition contains a fixed fraction of the total data, the size of each parti‐ tion grows proportionally to the total amount of data in the cluster. If partitions are very large, rebalancing and recovery from node failures become expensive. But if par‐ titions are too small, they incur too much overhead. The best performance is achieved when the size of partitions is “just right,” neither too big nor too small, which can be hard to achieve if the number of partitions is fixed but the dataset size varies.

<!-- page 234 -->

## Dynamic partitioning

For databases that use key range partitioning (see “Partitioning by Key Range” on page 202), a fixed number of partitions with fixed boundaries would be very incon‐ venient: if you got the boundaries wrong, you could end up with all of the data in one partition and all of the other partitions empty. Reconfiguring the partition bound‐ aries manually would be very tedious.

For that reason, key range–partitioned databases such as HBase and RethinkDB cre‐ ate partitions dynamically. When a partition grows to exceed a configured size (on HBase, the default is 10 GB), it is split into two partitions so that approximately half of the data ends up on each side of the split [26]. Conversely, if lots of data is deleted and a partition shrinks below some threshold, it can be merged with an adjacent par‐ tition. This process is similar to what happens at the top level of a B-tree (see “B- Trees” on page 79).

Each partition is assigned to one node, and each node can handle multiple partitions, like in the case of a fixed number of partitions. After a large partition has been split, one of its two halves can be transferred to another node in order to balance the load. In the case of HBase, the transfer of partition files happens through HDFS, the underlying distributed filesystem [3].

An advantage of dynamic partitioning is that the number of partitions adapts to the total data volume. If there is only a small amount of data, a small number of parti‐ tions is sufficient, so overheads are small; if there is a huge amount of data, the size of each individual partition is limited to a configurable maximum [23].

However, a caveat is that an empty database starts off with a single partition, since there is no a priori information about where to draw the partition boundaries. While the dataset is small—until it hits the point at which the first partition is split—all writes have to be processed by a single node while the other nodes sit idle. To miti‐ gate this issue, HBase and MongoDB allow an initial set of partitions to be configured on an empty database (this is called pre-splitting). In the case of key-range partition‐ ing, pre-splitting requires that you already know what the key distribution is going to look like [4, 26].

Dynamic partitioning is not only suitable for key range–partitioned data, but can equally well be used with hash-partitioned data. MongoDB since version 2.4 supports both key-range and hash partitioning, and it splits partitions dynamically in either case.

## Partitioning proportionally to nodes

With dynamic partitioning, the number of partitions is proportional to the size of the dataset, since the splitting and merging processes keep the size of each partition between some fixed minimum and maximum. On the other hand, with a fixed num‐

<!-- page 235 -->

ber of partitions, the size of each partition is proportional to the size of the dataset. In both of these cases, the number of partitions is independent of the number of nodes.

A third option, used by Cassandra and Ketama, is to make the number of partitions proportional to the number of nodes—in other words, to have a fixed number of par‐ titions per node [23, 27, 28]. In this case, the size of each partition grows proportion‐ ally to the dataset size while the number of nodes remains unchanged, but when you increase the number of nodes, the partitions become smaller again. Since a larger data volume generally requires a larger number of nodes to store, this approach also keeps the size of each partition fairly stable.

