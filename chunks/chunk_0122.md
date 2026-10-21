iv. Partitioning (sharding) a single-leader database, so that there is a separate leader per partition, does not affect linearizability, since it is only a single-object guarantee. Cross-partition transactions are a different mat‐ ter (see “Distributed Transactions and Consensus” on page 352).

The most common approach to making a system fault-tolerant is to use replication. Let’s revisit the replication methods from Chapter 5, and compare whether they can be made linearizable:

## Single-leader replication (potentially linearizable)

In a system with single-leader replication (see “Leaders and Followers” on page 152), the leader has the primary copy of the data that is used for writes, and the followers maintain backup copies of the data on other nodes. If you make reads from the leader, or from synchronously updated followers, they have the poten‐ tial to be linearizable.iv However, not every single-leader database is actually line‐ arizable, either by design (e.g., because it uses snapshot isolation) or due to concurrency bugs [10].

Using the leader for reads relies on the assumption that you know for sure who the leader is. As discussed in “The Truth Is Defined by the Majority” on page 300, it is quite possible for a node to think that it is the leader, when in fact it is not—and if the delusional leader continues to serve requests, it is likely to violate linearizability [20]. With asynchronous replication, failover may even lose com‐ mitted writes (see “Handling Node Outages” on page 156), which violates both durability and linearizability.

## Consensus algorithms (linearizable)

Some consensus algorithms, which we will discuss later in this chapter, bear a resemblance to single-leader replication. However, consensus protocols contain measures to prevent split brain and stale replicas. Thanks to these details, con‐ sensus algorithms can implement linearizable storage safely. This is how Zoo‐ Keeper [21] and etcd [22] work, for example.

## Multi-leader replication (not linearizable)

Systems with multi-leader replication are generally not linearizable, because they concurrently process writes on multiple nodes and asynchronously replicate them to other nodes. For this reason, they can produce conflicting writes that require resolution (see “Handling Write Conflicts” on page 171). Such conflicts are an artifact of the lack of a single copy of the data.

## Leaderless replication (probably not linearizable)

For systems with leaderless replication (Dynamo-style; see “Leaderless Replica‐ tion” on page 177), people sometimes claim that you can obtain “strong consis‐ tency” by requiring quorum reads and writes (w + r > n). Depending on the exact

<!-- page 356 -->

configuration of the quorums, and depending on how you define strong consis‐ tency, this is not quite true.

“Last write wins” conflict resolution methods based on time-of-day clocks (e.g., in Cassandra; see “Relying on Synchronized Clocks” on page 291) are almost cer‐ tainly nonlinearizable, because clock timestamps cannot be guaranteed to be consistent with actual event ordering due to clock skew. Sloppy quorums (“Sloppy Quorums and Hinted Handoff” on page 183) also ruin any chance of linearizability. Even with strict quorums, nonlinearizable behavior is possible, as demonstrated in the next section.

## Linearizability and quorums

Intuitively, it seems as though strict quorum reads and writes should be linearizable in a Dynamo-style model. However, when we have variable network delays, it is pos‐ sible to have race conditions, as demonstrated in Figure 9-6.

<table>
<tr><th>time</th></tr>
<tr><td>Writer</td></tr>
<tr><td>Repilica 1 [</td></tr>
<tr><td>Reptica2 ]</td></tr>
</table>

Figure 9-6. A nonlinearizable execution, despite using a strict quorum.

In Figure 9-6, the initial value of x is 0, and a writer client is updating x to 1 by send‐ ing the write to all three replicas (n = 3, w = 3). Concurrently, client A reads from a quorum of two nodes (r = 2) and sees the new value 1 on one of the nodes. Also con‐ currently with the write, client B reads from a different quorum of two nodes, and gets back the old value 0 from both.

The quorum condition is met (w + r > n), but this execution is nevertheless not line‐ arizable: B’s request begins after A’s request completes, but B returns the old value

<!-- page 357 -->

while A returns the new value. (It’s once again the Alice and Bob situation from Figure 9-1.)

Interestingly, it is possible to make Dynamo-style quorums linearizable at the cost of reduced performance: a reader must perform read repair (see “Read repair and antientropy” on page 178) synchronously, before returning results to the application [23], and a writer must read the latest state of a quorum of nodes before sending its writes [24, 25]. However, Riak does not perform synchronous read repair due to the performance penalty [26]. Cassandra does wait for read repair to complete on quo‐ rum reads [27], but it loses linearizability if there are multiple concurrent writes to the same key, due to its use of last-write-wins conflict resolution.

Moreover, only linearizable read and write operations can be implemented in this way; a linearizable compare-and-set operation cannot, because it requires a consen‐ sus algorithm [28].

In summary, it is safest to assume that a leaderless system with Dynamo-style replica‐ tion does not provide linearizability.

## The Cost of Linearizability

As some replication methods can provide linearizability and others cannot, it is inter‐ esting to explore the pros and cons of linearizability in more depth.

We already discussed some use cases for different replication methods in Chapter 5; for example, we saw that multi-leader replication is often a good choice for multidatacenter replication (see “Multi-datacenter operation” on page 168). An example of such a deployment is illustrated in Figure 9-7.

Datacenter 1

Datacenter 2

interruption itio B

Clients

Figure 9-7. A network interruption forcing a choice between linearizability and availa‐ bility.

<!-- page 358 -->

v. These two choices are sometimes known as CP (consistent but not available under network partitions) and AP (available but not consistent under network partitions), respectively. However, this classification scheme has several flaws [9], so it is best avoided.

Consider what happens if there is a network interruption between the two datacen‐ ters. Let’s assume that the network within each datacenter is working, and clients can reach the datacenters, but the datacenters cannot connect to each other.

With a multi-leader database, each datacenter can continue operating normally: since writes from one datacenter are asynchronously replicated to the other, the writes are simply queued up and exchanged when network connectivity is restored.

