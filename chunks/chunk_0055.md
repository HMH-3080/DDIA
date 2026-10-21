If all you need is to scale to higher load, the simplest approach is to buy a more pow‐ erful machine (sometimes called vertical scaling or scaling up). Many CPUs, many RAM chips, and many disks can be joined together under one operating system, and a fast interconnect allows any CPU to access any part of the memory or disk. In this kind of shared-memory architecture, all the components can be treated as a single machine [1].i

The problem with a shared-memory approach is that the cost grows faster than line‐ arly: a machine with twice as many CPUs, twice as much RAM, and twice as much disk capacity as another typically costs significantly more than twice as much. And due to bottlenecks, a machine twice the size cannot necessarily handle twice the load.

A shared-memory architecture may offer limited fault tolerance—high-end machines have hot-swappable components (you can replace disks, memory modules, and even CPUs without shutting down the machines)—but it is definitely limited to a single geographic location.

Another approach is the shared-disk architecture, which uses several machines with independent CPUs and RAM, but stores data on an array of disks that is shared between the machines, which are connected via a fast network.ii This architecture is used for some data warehousing workloads, but contention and the overhead of lock‐ ing limit the scalability of the shared-disk approach [2].

## Shared-Nothing Architectures

By contrast, shared-nothing architectures [3] (sometimes called horizontal scaling or scaling out) have gained a lot of popularity. In this approach, each machine or virtual machine running the database software is called a node. Each node uses its CPUs, RAM, and disks independently. Any coordination between nodes is done at the soft‐ ware level, using a conventional network.

No special hardware is required by a shared-nothing system, so you can use whatever machines have the best price/performance ratio. You can potentially distribute data across multiple geographic regions, and thus reduce latency for users and potentially be able to survive the loss of an entire datacenter. With cloud deployments of virtual

<!-- page 169 -->

machines, you don’t need to be operating at Google scale: even for small companies, a multi-region distributed architecture is now feasible.

In this part of the book, we focus on shared-nothing architectures—not because they are necessarily the best choice for every use case, but rather because they require the most caution from you, the application developer. If your data is distributed across multiple nodes, you need to be aware of the constraints and trade-offs that occur in such a distributed system—the database cannot magically hide these from you.

While a distributed shared-nothing architecture has many advantages, it usually also incurs additional complexity for applications and sometimes limits the expressive‐ ness of the data models you can use. In some cases, a simple single-threaded program can perform significantly better than a cluster with over 100 CPU cores [4]. On the other hand, shared-nothing systems can be very powerful. The next few chapters go into details on the issues that arise when data is distributed.

## Replication Versus Partitioning

There are two common ways data is distributed across multiple nodes:

## Replication

Keeping a copy of the same data on several different nodes, potentially in differ‐ ent locations. Replication provides redundancy: if some nodes are unavailable, the data can still be served from the remaining nodes. Replication can also help improve performance. We discuss replication in Chapter 5.

## Partitioning

Splitting a big database into smaller subsets called partitions so that different par‐ titions can be assigned to different nodes (also known as sharding). We discuss partitioning in Chapter 6.

These are separate mechanisms, but they often go hand in hand, as illustrated in Figure II-1.

<!-- page 170 -->

Partition 1, Replica 1

<table>
<tr><th></th><th></th><th></th><th></th><th></th><th colspan="2">Partition 2, Replica 1</th><th></th><th></th></tr>
<tr><td>136 →</td><td>211 →</td><td>S</td><td>377 →</td><td>N</td><td>629 →</td><td>696 →</td><td>N</td><td>858 →</td></tr>
<tr><td>Four score</td><td>Johannes</td><td></td><td>Whereas</td><td></td><td>Die Würde</td><td>Whereas</td><td></td><td>We hold</td></tr>
<tr><td>and seven</td><td>Dei gracia</td><td></td><td colspan="2">recognition</td><td>des Men-</td><td>the Lords</td><td></td><td>these truths</td></tr>
<tr><td>years ago</td><td>Rex Anglie,</td><td></td><td>of the</td><td></td><td>schen ist</td><td>Spiritual</td><td></td><td>to be self-</td></tr>
<tr><td>our fathers</td><td>Dominus</td><td></td><td>inherent</td><td></td><td>unantastbar</td><td colspan="2">and Tempo-</td><td>evident</td></tr>
<tr><td></td><td></td><td></td><td></td><td>¹ copy of</td><td></td><td></td><td></td><td>¹ copy of</td></tr>
<tr><td></td><td></td><td></td><td></td><td>◦ the same</td><td></td><td></td><td></td><td>◦ the same</td></tr>
<tr><td colspan="2">Partition 1, Replica 2</td><td></td><td>v</td><td>. data</td><td colspan="2">Partition 2, Replica 2</td><td></td><td>. data</td></tr>
<tr><td>X 136 →</td><td>211 →</td><td></td><td>377 →</td><td>S</td><td>629 →</td><td>696 →</td><td></td><td>858 →</td></tr>
<tr><td>Four score</td><td>Johannes</td><td></td><td>Whereas</td><td></td><td>Die Würde</td><td>Whereas</td><td></td><td>We hold</td></tr>
<tr><td>and seven</td><td>Dei gracia</td><td></td><td colspan="2">recognition</td><td>des Men-</td><td>the Lords</td><td></td><td>these truths</td></tr>
<tr><td>years ago</td><td>Rex Anglie,</td><td></td><td>of the</td><td></td><td>schen ist</td><td>Spiritual</td><td></td><td>to be self-</td></tr>
<tr><td>our fathers</td><td>Dominus</td><td></td><td>inherent</td><td></td><td>unantastbar</td><td colspan="2">and Tempo-</td><td>evident</td></tr>
</table>

Figure II-1. A database split into two partitions, with two replicas per partition.

With an understanding of those concepts, we can discuss the difficult trade-offs that you need to make in a distributed system. We’ll discuss transactions in Chapter 7, as that will help you understand all the many things that can go wrong in a data system, and what you can do about them. We’ll conclude this part of the book by discussing the fundamental limitations of distributed systems in Chapters 8 and 9.

Later, in Part III of this book, we will discuss how you can take several (potentially distributed) datastores and integrate them into a larger system, satisfying the needs of a complex application. But first, let’s talk about distributed data.

## References

[1] Ulrich Drepper: “What Every Programmer Should Know About Memory,” akka‐ dia.org, November 21, 2007. [2] Ben Stopford: “Shared Nothing vs. Shared Disk Architectures: An Independent View,” benstopford.com, November 24, 2009. [3] Michael Stonebraker: “The Case for Shared Nothing,” IEEE Database Engineering Bulletin, volume 9, number 1, pages 4–9, March 1986. [4] Frank McSherry, Michael Isard, and Derek G. Murray: “Scalability! But at What COST?,” at 15th USENIX Workshop on Hot Topics in Operating Systems (HotOS), May 2015.

<!-- page 171 -->

<!-- page 172 -->

<table>
<tr><th></th><th></th><th>To Consistency</th></tr>
<tr><td>• -</td><td></td><td>&amp; Consensus</td></tr>
<tr><td>RethinkDB</td><td>Mon</td><td>Chapter 9)</td></tr>
<tr><td>fy</td><td></td><td></td></tr>
<tr><td></td><td>NC</td><td></td></tr>
<tr><td>PostgreSQL</td><td></td><td></td></tr>
</table>

<table>
<tr><th></th><th>OR</th><th></th></tr>
<tr><td></td><td></td><td>CouchDB</td></tr>
<tr><td></td><td></td><td>alendar, sync</td></tr>
<tr><td></td><td></td><td>-</td></tr>
<tr><td></td><td></td><td></td></tr>
<tr><td></td><td>C A</td><td>10</td></tr>
<tr><td></td><td></td><td>Eassandra</td></tr>
</table>

To Log-structured Storage (Chapter 3)

<!-- page 173 -->

## Replication

The major difference between a thing that might go wrong and a thing that cannot possibly go wrong is that when a thing that cannot possibly go wrong goes wrong it usually turns out to be impossible to get at or repair.

—Douglas Adams, Mostly Harmless (1992)

Replication means keeping a copy of the same data on multiple machines that are connected via a network. As discussed in the introduction to Part II, there are several reasons why you might want to replicate data:

• To keep data geographically close to your users (and thus reduce latency)
• To allow the system to continue working even if some of its parts have failed (and thus increase availability)
• To scale out the number of machines that can serve read queries (and thus increase read throughput)

