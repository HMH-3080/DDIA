When a new node joins the cluster, it randomly chooses a fixed number of existing partitions to split, and then takes ownership of one half of each of those split parti‐ tions while leaving the other half of each partition in place. The randomization can produce unfair splits, but when averaged over a larger number of partitions (in Cas‐ sandra, 256 partitions per node by default), the new node ends up taking a fair share of the load from the existing nodes. Cassandra 3.0 introduced an alternative rebalanc‐ ing algorithm that avoids unfair splits [29].

Picking partition boundaries randomly requires that hash-based partitioning is used (so the boundaries can be picked from the range of numbers produced by the hash function). Indeed, this approach corresponds most closely to the original definition of consistent hashing [7] (see “Consistent Hashing” on page 204). Newer hash func‐ tions can achieve a similar effect with lower metadata overhead [8].

## Operations: Automatic or Manual Rebalancing

There is one important question with regard to rebalancing that we have glossed over: does the rebalancing happen automatically or manually?

There is a gradient between fully automatic rebalancing (the system decides automat‐ ically when to move partitions from one node to another, without any administrator interaction) and fully manual (the assignment of partitions to nodes is explicitly con‐ figured by an administrator, and only changes when the administrator explicitly reconfigures it). For example, Couchbase, Riak, and Voldemort generate a suggested partition assignment automatically, but require an administrator to commit it before it takes effect.

Fully automated rebalancing can be convenient, because there is less operational work to do for normal maintenance. However, it can be unpredictable. Rebalancing is an expensive operation, because it requires rerouting requests and moving a large amount of data from one node to another. If it is not done carefully, this process can overload the network or the nodes and harm the performance of other requests while the rebalancing is in progress.

<!-- page 236 -->

Such automation can be dangerous in combination with automatic failure detection. For example, say one node is overloaded and is temporarily slow to respond to requests. The other nodes conclude that the overloaded node is dead, and automati‐ cally rebalance the cluster to move load away from it. This puts additional load on the overloaded node, other nodes, and the network—making the situation worse and potentially causing a cascading failure.

For that reason, it can be a good thing to have a human in the loop for rebalancing. It’s slower than a fully automatic process, but it can help prevent operational surprises.

## Request Routing

We have now partitioned our dataset across multiple nodes running on multiple machines. But there remains an open question: when a client wants to make a request, how does it know which node to connect to? As partitions are rebalanced, the assignment of partitions to nodes changes. Somebody needs to stay on top of those changes in order to answer the question: if I want to read or write the key “foo”, which IP address and port number do I need to connect to?

This is an instance of a more general problem called service discovery, which isn’t limited to just databases. Any piece of software that is accessible over a network has this problem, especially if it is aiming for high availability (running in a redundant configuration on multiple machines). Many companies have written their own inhouse service discovery tools, and many of these have been released as open source [30].

On a high level, there are a few different approaches to this problem (illustrated in Figure 6-7):

1. Allow clients to contact any node (e.g., via a round-robin load balancer). If that node coincidentally owns the partition to which the request applies, it can handle the request directly; otherwise, it forwards the request to the appropriate node, receives the reply, and passes the reply along to the client.
2. Send all requests from clients to a routing tier first, which determines the node that should handle each request and forwards it accordingly. This routing tier does not itself handle any requests; it only acts as a partition-aware load balancer.
3. Require that clients be aware of the partitioning and the assignment of partitions to nodes. In this case, a client can connect directly to the appropriate node, without any intermediary.

In all cases, the key problem is: how does the component making the routing decision (which may be one of the nodes, or the routing tier, or the client) learn about changes in the assignment of partitions to nodes?

<!-- page 237 -->

<table>
<tr><th>)</th><th></th><th></th><th>2 Q</th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td></td><td>client</td><td></td><td></td><td>client</td><td></td><td></td><td>client</td><td></td></tr>
<tr><td colspan="3">get“foo” / choose node 0</td><td>get “foo”</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>randomly</td><td></td><td></td><td></td><td></td><td></td><td>get “foo”</td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td>routing tier</td><td></td><td colspan="2">connect directly</td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>to node 2</td><td></td></tr>
<tr><td></td><td colspan="2">“foo” lives on node 2</td><td colspan="2">“foo” lives on node 2 N</td><td></td><td></td><td></td><td></td></tr>
<tr><td>node 0</td><td>node 1</td><td>node 2</td><td>node 0</td><td>node 1</td><td>node 2</td><td>node 0</td><td>node 1</td><td>node 2</td></tr>
<tr><td></td><td></td><td>“foo”</td><td></td><td></td><td>foo"</td><td></td><td></td><td>“foo”</td></tr>
</table>

w = the knowledge of which partition is assigned to which node

Figure 6-7. Three different ways of routing a request to the right node.

This is a challenging problem, because it is important that all participants agree — - - otherwise requests would be sent to the wrong nodes and not handled correctly. There are protocols for achieving consensus in a distributed system, but they are hard to implement correctly (see Chapter 9).

Many distributed data systems rely on a separate coordination service such as Zoo‐ Keeper to keep track of this cluster metadata, as illustrated in Figure 6-8. Each node registers itself in ZooKeeper, and ZooKeeper maintains the authoritative mapping of partitions to nodes. Other actors, such as the routing tier or the partitioning-aware client, can subscribe to this information in ZooKeeper. Whenever a partition changes ownership, or a node is added or removed, ZooKeeper notifies the routing tier so that it can keep its routing information up to date.

<table>
<tr><th></th><th>client</th><th></th><th>Key range</th><th>Partition</th><th>Node</th><th>IP address</th></tr>
<tr><td>get “Danu</td><td></td><td></td><td>A-ak — Bayes</td><td>partition 0</td><td>node 0</td><td>10.20.30.100</td></tr>
<tr><td></td><td></td><td>ZooKeeper</td><td>Bayeu — Ceanothus</td><td>partition 1</td><td>node 1</td><td>10.20.30.101</td></tr>
<tr><td></td><td>routing tier</td><td></td><td>Ceara — Deluc</td><td>partition 2</td><td>node 2</td><td>10.20.30.102</td></tr>
<tr><td></td><td></td><td></td><td>Delusion — Frenssen</td><td>partition 3</td><td>node 0</td><td>10.20.30.100</td></tr>
<tr><td></td><td></td><td></td><td>Freon — Holderlin</td><td>partition 4</td><td>node 1</td><td>10.20.30.101</td></tr>
<tr><td></td><td></td><td></td><td>Holderness — Krasnoje</td><td>partition 5</td><td>node 2</td><td>10.20.30.102</td></tr>
<tr><td></td><td></td><td></td><td>Krasnokamsk  — Menadra</td><td>partition 6</td><td>node 0</td><td>10.20.30.100</td></tr>
<tr><td>node 0</td><td>node 1</td><td>node</td><td>Menage — Ottawa</td><td>partition 7</td><td>node 1</td><td>10.20.30.101</td></tr>
<tr><td></td><td></td><td></td><td>Otter — Rethimnon</td><td>partition 8</td><td>node 2</td><td>10.20.30.102</td></tr>
<tr><td></td><td></td><td></td><td>Reti — Solovets</td><td>partition 9</td><td>node 0</td><td>10.20.30.100</td></tr>
<tr><td></td><td></td><td></td><td>Solovyov — Truck</td><td>partition 10</td><td>node 1</td><td>10.20.30.101</td></tr>
<tr><td></td><td></td><td></td><td>Trudeau — Zywiec</td><td>partition 11</td><td>node 2</td><td>10.20.30.102</td></tr>
</table>

w

w = the knowledge of which partition is assigned to which node

Figure 6-8. Using ZooKeeper to keep track of assignment of partitions to nodes.

<!-- page 238 -->

