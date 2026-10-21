A widely misunderstood theoretical result that is not useful in practice. See “The CAP theorem” on page 336.

## causality

The dependency between events that ari‐ ses when one thing “happens before” another thing in a system. For example, a later event that is in response to an earlier event, or builds upon an earlier event, or should be understood in the light of an earlier event. See “The “happens-before” relationship and concurrency” on page 186 and “Ordering and Causality” on page 339.

## consensus

A fundamental problem in distributed computing, concerning getting several nodes to agree on something (for exam‐ ple, which node should be the leader for a database cluster). The problem is much harder than it seems at first glance. See “Fault-Tolerant Consensus” on page 364.

## data warehouse

A database in which data from several dif‐ ferent OLTP systems has been combined and prepared to be used for analytics pur‐ poses. See “Data Warehousing” on page 91.

## declarative

Describing the properties that something should have, but not the exact steps for how to achieve it. In the context of quer‐ ies, a query optimizer takes a declarative query and decides how it should best be executed. See “Query Languages for Data” on page 42.

## denormalize

To introduce some amount of redun‐ dancy or duplication in a normalized dataset, typically in the form of a cache or index, in order to speed up reads. A denormalized value is a kind of precom‐ puted query result, similar to a material‐

ized view. See “Single-Object and Multi- Object Operations” on page 228 and “Deriving several views from the same event log” on page 461.

## derived data

A dataset that is created from some other data through a repeatable process, which you could run again if necessary. Usually, derived data is needed to speed up a par‐ ticular kind of read access to the data. Indexes, caches, and materialized views are examples of derived data. See the introduction to Part III.

## deterministic

Describing a function that always pro‐ duces the same output if you give it the same input. This means it cannot depend on random numbers, the time of day, net‐ work communication, or other unpredict‐ able things.

## distributed

Running on several nodes connected by a network. Characterized by partial failures: some part of the system may be broken while other parts are still working, and it is often impossible for the software to know what exactly is broken. See “Faults and Partial Failures” on page 274.

## durable

Storing data in a way such that you believe it will not be lost, even if various faults occur. See “Durability” on page 226.

## ETL

Extract–Transform–Load. The process of extracting data from a source database, transforming it into a form that is more suitable for analytic queries, and loading it into a data warehouse or batch processing system. See “Data Warehousing” on page 91.

## failover

In systems that have a single leader, fail‐ over is the process of moving the leader‐ ship role from one node to another. See “Handling Node Outages” on page 156.

<!-- page 577 -->

## fault-tolerant

Able to recover automatically if some‐ thing goes wrong (e.g., if a machine crashes or a network link fails). See “Reli‐ ability” on page 6.

## flow control

## See backpressure.

## follower

A replica that does not directly accept any writes from clients, but only processes data changes that it receives from a leader. Also known as a secondary, slave, read replica, or hot standby. See “Leaders and Followers” on page 152.

## full-text search

Searching text by arbitrary keywords, often with additional features such as matching similarly spelled words or syno‐ nyms. A full-text index is a kind of secon‐ dary index that supports such queries. See “Full-text search and fuzzy indexes” on page 88.

## graph

A data structure consisting of vertices (things that you can refer to, also known as nodes or entities) and edges (connec‐ tions from one vertex to another, also known as relationships or arcs). See “Graph-Like Data Models” on page 49.

## hash

A function that turns an input into a random-looking number. The same input always returns the same number as out‐ put. Two different inputs are very likely to have two different numbers as output, although it is possible that two different inputs produce the same output (this is called a collision). See “Partitioning by Hash of Key” on page 203.

## idempotent

Describing an operation that can be safely retried; if it is executed more than once, it has the same effect as if it was only exe‐ cuted once. See “Idempotence” on page 478.

## index

A data structure that lets you efficiently search for all records that have a particu‐ lar value in a particular field. See “Data Structures That Power Your Database” on page 70.

## isolation

In the context of transactions, describing the degree to which concurrently execut‐ ing transactions can interfere with each other. Serializable isolation provides the strongest guarantees, but weaker isolation levels are also used. See “Isolation” on page 225.

## join

To bring together records that have some‐ thing in common. Most commonly used in the case where one record has a refer‐ ence to another (a foreign key, a docu‐ ment reference, an edge in a graph) and a query needs to get the record that the ref‐ erence points to. See “Many-to-One and Many-to-Many Relationships” on page 33 and “Reduce-Side Joins and Grouping” on page 403.

## leader

When data or a service is replicated across several nodes, the leader is the designated replica that is allowed to make changes. A leader may be elected through some pro‐ tocol, or manually chosen by an adminis‐ trator. Also known as the primary or master. See “Leaders and Followers” on page 152.

## linearizable

Behaving as if there was only a single copy of data in the system, which is updated by atomic operations. See “Linearizability” on page 324.

## locality

A performance optimization: putting sev‐ eral pieces of data in the same place if they are frequently needed at the same time. See “Data locality for queries” on page 41.

<!-- page 578 -->

## lock

A mechanism to ensure that only one thread, node, or transaction can access something, and anyone else who wants to access the same thing must wait until the lock is released. See “Two-Phase Locking (2PL)” on page 257 and “The leader and the lock” on page 301.

## log

