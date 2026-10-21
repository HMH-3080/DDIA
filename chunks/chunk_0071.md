Despite being a simple goal—keeping a copy of the same data on several machines— replication turns out to be a remarkably tricky problem. It requires carefully thinking about concurrency and about all the things that can go wrong, and dealing with the consequences of those faults. At a minimum, we need to deal with unavailable nodes and network interruptions (and that’s not even considering the more insidious kinds of fault, such as silent data corruption due to software bugs).

We discussed three main approaches to replication:

## Single-leader replication

Clients send all writes to a single node (the leader), which sends a stream of data change events to the other replicas (followers). Reads can be performed on any replica, but reads from followers might be stale.

## Multi-leader replication

Clients send each write to one of several leader nodes, any of which can accept writes. The leaders send streams of data change events to each other and to any follower nodes.

## Leaderless replication

Clients send each write to several nodes, and read from several nodes in parallel in order to detect and correct nodes with stale data.

Each approach has advantages and disadvantages. Single-leader replication is popular because it is fairly easy to understand and there is no conflict resolution to worry about. Multi-leader and leaderless replication can be more robust in the presence of

<!-- page 215 -->

faulty nodes, network interruptions, and latency spikes—at the cost of being harder to reason about and providing only very weak consistency guarantees.

Replication can be synchronous or asynchronous, which has a profound effect on the system behavior when there is a fault. Although asynchronous replication can be fast when the system is running smoothly, it’s important to figure out what happens when replication lag increases and servers fail. If a leader fails and you promote an asynchronously updated follower to be the new leader, recently committed data may be lost.

We looked at some strange effects that can be caused by replication lag, and we dis‐ cussed a few consistency models which are helpful for deciding how an application should behave under replication lag:

## Read-after-write consistency

Users should always see data that they submitted themselves.

## Monotonic reads

After users have seen the data at one point in time, they shouldn’t later see the data from some earlier point in time.

## Consistent prefix reads

Users should see the data in a state that makes causal sense: for example, seeing a question and its reply in the correct order.

Finally, we discussed the concurrency issues that are inherent in multi-leader and leaderless replication approaches: because they allow multiple writes to happen con‐ currently, conflicts may occur. We examined an algorithm that a database might use to determine whether one operation happened before another, or whether they hap‐ pened concurrently. We also touched on methods for resolving conflicts by merging together concurrent updates.

In the next chapter we will continue looking at data that is distributed across multiple machines, through the counterpart of replication: splitting a large dataset into parti‐ tions.

## References

[1] Bruce G. Lindsay, Patricia Griffiths Selinger, C. Galtieri, et al.: “Notes on Dis‐ tributed Databases,” IBM Research, Research Report RJ2571(33471), July 1979.

[2] “Oracle Active Data Guard Real-Time Data Protection and Availability,” Oracle White Paper, June 2013.

[3] “AlwaysOn Availability Groups,” in SQL Server Books Online, Microsoft, 2012.

<!-- page 216 -->

[4] Lin Qiao, Kapil Surlaker, Shirshanka Das, et al.: “On Brewing Fresh Espresso: LinkedIn’s Distributed Data Serving Platform,” at ACM International Conference on Management of Data (SIGMOD), June 2013. [5] Jun Rao: “Intra-Cluster Replication for Apache Kafka,” at ApacheCon North America, February 2013. [6] “Highly Available Queues,” in RabbitMQ Server Documentation, Pivotal Software, Inc., 2014. [7] Yoshinori Matsunobu: “Semi-Synchronous Replication at Facebook,” yoshinori‐ matsunobu.blogspot.co.uk, April 1, 2014. [8] Robbert van Renesse and Fred B. Schneider: “Chain Replication for Supporting High Throughput and Availability,” at 6th USENIX Symposium on Operating System Design and Implementation (OSDI), December 2004. [9] Jeff Terrace and Michael J. Freedman: “Object Storage on CRAQ: High- Throughput Chain Replication for Read-Mostly Workloads,” at USENIX Annual Technical Conference (ATC), June 2009. [10] Brad Calder, Ju Wang, Aaron Ogus, et al.: “Windows Azure Storage: A Highly Available Cloud Storage Service with Strong Consistency,” at 23rd ACM Symposium on Operating Systems Principles (SOSP), October 2011. [11] Andrew Wang: “Windows Azure Storage,” umbrant.com, February 4, 2016. [12] “Percona Xtrabackup - Documentation,” Percona LLC, 2014. [13] Jesse Newland: “GitHub Availability This Week,” github.com, September 14, 2012. [14] Mark Imbriaco: “Downtime Last Saturday,” github.com, December 26, 2012. [15] John Hugg: “‘All in’ with Determinism for Performance and Testing in Dis‐ tributed Systems,” at Strange Loop, September 2015. [16] Amit Kapila: “WAL Internals of PostgreSQL,” at PostgreSQL Conference (PGCon), May 2012. [17] MySQL Internals Manual. Oracle, 2014. [18] Yogeshwer Sharma, Philippe Ajoux, Petchean Ang, et al.: “Wormhole: Reliable Pub-Sub to Support Geo-Replicated Internet Services,” at 12th USENIX Symposium on Networked Systems Design and Implementation (NSDI), May 2015. [19] “Oracle GoldenGate 12c: Real-Time Access to Real-Time Information,” Oracle White Paper, October 2013. [20] Shirshanka Das, Chavdar Botev, Kapil Surlaker, et al.: “All Aboard the Data‐ bus!,” at ACM Symposium on Cloud Computing (SoCC), October 2012.

<!-- page 217 -->

