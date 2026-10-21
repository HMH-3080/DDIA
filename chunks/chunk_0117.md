[70] David Terei and Amit Levy: “Blade: A Data Center Garbage Collector,” arXiv: 1504.02578, April 13, 2015. [71] Martin Maas, Tim Harris, Krste Asanović, and John Kubiatowicz: “Trash Day: Coordinating Garbage Collection in Distributed Systems,” at 15th USENIX Workshop on Hot Topics in Operating Systems (HotOS), May 2015. [72] “Predictable Low Latency,” Cinnober Financial Technology AB, cinnober.com, November 24, 2013. [73] Martin Fowler: “The LMAX Architecture,” martinfowler.com, July 12, 2011. [74] Flavio P. Junqueira and Benjamin Reed: ZooKeeper: Distributed Process Coordi‐ nation. O’Reilly Media, 2013. ISBN: 978-1-449-36130-3 [75] Enis Söztutar: “HBase and HDFS: Understanding Filesystem Usage in HBase,” at HBaseCon, June 2013. [76] Caitie McCaffrey: “Clients Are Jerks: AKA How Halo 4 DoSed the Services at Launch & How We Survived,” caitiem.com, June 23, 2015. [77] Leslie Lamport, Robert Shostak, and Marshall Pease: “The Byzantine Generals Problem,” ACM Transactions on Programming Languages and Systems (TOPLAS), volume 4, number 3, pages 382–401, July 1982. doi:10.1145/357172.357176 [78] Jim N. Gray: “Notes on Data Base Operating Systems,” in Operating Systems: An Advanced Course, Lecture Notes in Computer Science, volume 60, edited by R. Bayer,
R. M. Graham, and G. Seegmüller, pages 393–481, Springer-Verlag, 1978. ISBN: 978-3-540-08755-7 [79] Brian Palmer: “How Complicated Was the Byzantine Empire?,” slate.com, Octo‐ ber 20, 2011. [80] Leslie Lamport: “My Writings,” research.microsoft.com, December 16, 2014. This page can be found by searching the web for the 23-character string obtained by removing the hyphens from the string allla-mport-spubso-ntheweb. [81] John Rushby: “Bus Architectures for Safety-Critical Embedded Systems,” at 1st International Workshop on Embedded Software (EMSOFT), October 2001. [82] Jake Edge: “ELC: SpaceX Lessons Learned,” lwn.net, March 6, 2013. [83] Andrew Miller and Joseph J. LaViola, Jr.: “Anonymous Byzantine Consensus from Moderately-Hard Puzzles: A Model for Bitcoin,” University of Central Florida, Technical Report CS-TR-14-01, April 2014. [84] James Mickens: “The Saddest Moment,” USENIX ;login: logout, May 2013. [85] Evan Gilman: “The Discovery of Apache ZooKeeper’s Poison Packet,” pagerd‐ uty.com, May 7, 2015.

<!-- page 340 -->

[86] Jonathan Stone and Craig Partridge: “When the CRC and TCP Checksum Disa‐ gree,” at ACM Conference on Applications, Technologies, Architectures, and Protocols for Computer Communication (SIGCOMM), August 2000. doi: 10.1145/347059.347561 [87] Evan Jones: “How Both TCP and Ethernet Checksums Fail,” evanjones.ca, Octo‐ ber 5, 2015. [88] Cynthia Dwork, Nancy Lynch, and Larry Stockmeyer: “Consensus in the Pres‐ ence of Partial Synchrony,” Journal of the ACM, volume 35, number 2, pages 288– 323, April 1988. doi:10.1145/42282.42283 [89] Peter Bailis and Ali Ghodsi: “Eventual Consistency Today: Limitations, Exten‐ sions, and Beyond,” ACM Queue, volume 11, number 3, pages 55-63, March 2013. doi:10.1145/2460276.2462076 [90] Bowen Alpern and Fred B. Schneider: “Defining Liveness,” Information Process‐ ing Letters, volume 21, number 4, pages 181–185, October 1985. doi: 10.1016/0020-0190(85)90056-0 [91] Flavio P. Junqueira: “Dude, Where’s My Metadata?,” fpj.me, May 28, 2015. [92] Scott Sanders: “January 28th Incident Report,” github.com, February 3, 2016. [93] Jay Kreps: “A Few Notes on Kafka and Jepsen,” blog.empathybox.com, Septem‐ ber 25, 2013. [94] Thanh Do, Mingzhe Hao, Tanakorn Leesatapornwongsa, et al.: “Limplock: Understanding the Impact of Limpware on Scale-out Cloud Systems,” at 4th ACM Symposium on Cloud Computing (SoCC), October 2013. doi: 10.1145/2523616.2523627 [95] Frank McSherry, Michael Isard, and Derek G. Murray: “Scalability! But at What COST?,” at 15th USENIX Workshop on Hot Topics in Operating Systems (HotOS), May 2015.

<!-- page 341 -->

<!-- page 342 -->

<!-- page 343 -->

## Consistency and Consensus

Is it better to be alive and wrong or right and dead?

—Jay Kreps, A Few Notes on Kafka and Jepsen (2013)

Lots of things can go wrong in distributed systems, as discussed in Chapter 8. The simplest way of handling such faults is to simply let the entire service fail, and show the user an error message. If that solution is unacceptable, we need to find ways of tolerating faults—that is, of keeping the service functioning correctly, even if some internal component is faulty.

In this chapter, we will talk about some examples of algorithms and protocols for building fault-tolerant distributed systems. We will assume that all the problems from Chapter 8 can occur: packets can be lost, reordered, duplicated, or arbitrarily delayed in the network; clocks are approximate at best; and nodes can pause (e.g., due to garbage collection) or crash at any time.

The best way of building fault-tolerant systems is to find some general-purpose abstractions with useful guarantees, implement them once, and then let applications rely on those guarantees. This is the same approach as we used with transactions in Chapter 7: by using a transaction, the application can pretend that there are no crashes (atomicity), that nobody else is concurrently accessing the database (isola‐ tion), and that storage devices are perfectly reliable (durability). Even though crashes, race conditions, and disk failures do occur, the transaction abstraction hides those problems so that the application doesn’t need to worry about them.

We will now continue along the same lines, and seek abstractions that can allow an application to ignore some of the problems with distributed systems. For example, one of the most important abstractions for distributed systems is consensus: that is, getting all of the nodes to agree on something. As we shall see in this chapter, reliably

<!-- page 344 -->

reaching consensus in spite of network faults and process failures is a surprisingly tricky problem.

Once you have an implementation of consensus, applications can use it for various purposes. For example, say you have a database with single-leader replication. If the leader dies and you need to fail over to another node, the remaining database nodes can use consensus to elect a new leader. As discussed in “Handling Node Outages” on page 156, it’s important that there is only one leader, and that all nodes agree who the leader is. If two nodes both believe that they are the leader, that situation is called split brain, and it often leads to data loss. Correct implementations of consensus help avoid such problems.

Later in this chapter, in “Distributed Transactions and Consensus” on page 352, we will look into algorithms to solve consensus and related problems. But first we first need to explore the range of guarantees and abstractions that can be provided in a distributed system.

We need to understand the scope of what can and cannot be done: in some situa‐ tions, it’s possible for the system to tolerate faults and continue working; in other sit‐ uations, that is not possible. The limits of what is and isn’t possible have been explored in depth, both in theoretical proofs and in practical implementations. We will get an overview of those fundamental limits in this chapter.

