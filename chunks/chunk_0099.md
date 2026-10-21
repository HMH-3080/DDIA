[44] Gary Fredericks: “Postgres Serializability Bug,” github.com, September 2015. [45] Michael Stonebraker, Samuel Madden, Daniel J. Abadi, et al.: “The End of an Architectural Era (It’s Time for a Complete Rewrite),” at 33rd International Confer‐ ence on Very Large Data Bases (VLDB), September 2007. [46] John Hugg: “H-Store/VoltDB Architecture vs. CEP Systems and Newer Stream‐ ing Architectures,” at Data @Scale Boston, November 2014. [47] Robert Kallman, Hideaki Kimura, Jonathan Natkins, et al.: “H-Store: A High- Performance, Distributed Main Memory Transaction Processing System,” Proceed‐ ings of the VLDB Endowment, volume 1, number 2, pages 1496–1499, August 2008. [48] Rich Hickey: “The Architecture of Datomic,” infoq.com, November 2, 2012. [49] John Hugg: “Debunking Myths About the VoltDB In-Memory Database,” voltdb.com, May 12, 2014. [50] Joseph M. Hellerstein, Michael Stonebraker, and James Hamilton: “Architecture of a Database System,” Foundations and Trends in Databases, volume 1, number 2, pages 141–259, November 2007. doi:10.1561/1900000002 [51] Michael J. Cahill: “Serializable Isolation for Snapshot Databases,” PhD Thesis, University of Sydney, July 2009. [52] D. Z. Badal: “Correctness of Concurrency Control and Implications in Dis‐ tributed Databases,” at 3rd International IEEE Computer Software and Applications Conference (COMPSAC), November 1979. [53] Rakesh Agrawal, Michael J. Carey, and Miron Livny: “Concurrency Control Per‐ formance Modeling: Alternatives and Implications,” ACM Transactions on Database Systems (TODS), volume 12, number 4, pages 609–654, December 1987. doi: 10.1145/32204.32220 [54] Dave Rosenthal: “Databases at 14.4MHz,” blog.foundationdb.com, December 10, 2014.

<!-- page 294 -->

a V

<!-- page 295 -->

i. With one exception: we will assume that faults are non-Byzantine (see “Byzantine Faults” on page 304).

## The Trouble with Distributed Systems

Hey I just met you The network’s laggy But here’s my data

So store it maybe

—Kyle Kingsbury, Carly Rae Jepsen and the Perils of Network Partitions (2013)

A recurring theme in the last few chapters has been how systems handle things going wrong. For example, we discussed replica failover (“Handling Node Outages” on page 156), replication lag (“Problems with Replication Lag” on page 161), and con‐ currency control for transactions (“Weak Isolation Levels” on page 233). As we come to understand various edge cases that can occur in real systems, we get better at han‐ dling them.

However, even though we have talked a lot about faults, the last few chapters have still been too optimistic. The reality is even darker. We will now turn our pessimism to the maximum and assume that anything that can go wrong will go wrong.i (Expe‐ rienced systems operators will tell you that is a reasonable assumption. If you ask nicely, they might tell you some frightening stories while nursing their scars of past battles.)

Working with distributed systems is fundamentally different from writing software on a single computer—and the main difference is that there are lots of new and excit‐ ing ways for things to go wrong [1, 2]. In this chapter, we will get a taste of the prob‐ lems that arise in practice, and an understanding of the things we can and cannot rely on.

<!-- page 296 -->

In the end, our task as engineers is to build systems that do their job (i.e., meet the guarantees that users are expecting), in spite of everything going wrong. In Chapter 9, we will look at some examples of algorithms that can provide such guarantees in a distributed system. But first, in this chapter, we must understand what challenges we are up against.

This chapter is a thoroughly pessimistic and depressing overview of things that may go wrong in a distributed system. We will look into problems with networks (“Unre‐ liable Networks” on page 277); clocks and timing issues (“Unreliable Clocks” on page 287); and we’ll discuss to what degree they are avoidable. The consequences of all these issues are disorienting, so we’ll explore how to think about the state of a dis‐ tributed system and how to reason about things that have happened (“Knowledge, Truth, and Lies” on page 300).

## Faults and Partial Failures

When you are writing a program on a single computer, it normally behaves in a fairly predictable way: either it works or it doesn’t. Buggy software may give the appearance that the computer is sometimes “having a bad day” (a problem that is often fixed by a reboot), but that is mostly just a consequence of badly written software.

There is no fundamental reason why software on a single computer should be flaky: when the hardware is working correctly, the same operation always produces the same result (it is deterministic). If there is a hardware problem (e.g., memory corrup‐ tion or a loose connector), the consequence is usually a total system failure (e.g., ker‐ nel panic, “blue screen of death,” failure to start up). An individual computer with good software is usually either fully functional or entirely broken, but not something in between.

This is a deliberate choice in the design of computers: if an internal fault occurs, we prefer a computer to crash completely rather than returning a wrong result, because wrong results are difficult and confusing to deal with. Thus, computers hide the fuzzy physical reality on which they are implemented and present an idealized system model that operates with mathematical perfection. A CPU instruction always does the same thing; if you write some data to memory or disk, that data remains intact and doesn’t get randomly corrupted. This design goal of always-correct computation goes all the way back to the very first digital computer [3].

When you are writing software that runs on several computers, connected by a net‐ work, the situation is fundamentally different. In distributed systems, we are no longer operating in an idealized system model—we have no choice but to confront the messy reality of the physical world. And in the physical world, a remarkably wide range of things can go wrong, as illustrated by this anecdote [4]:

<!-- page 297 -->

In my limited experience I’ve dealt with long-lived network partitions in a single data center (DC), PDU [power distribution unit] failures, switch failures, accidental power cycles of whole racks, whole-DC backbone failures, whole-DC power failures, and a hypoglycemic driver smashing his Ford pickup truck into a DC’s HVAC [heating, ven‐ tilation, and air conditioning] system. And I’m not even an ops guy.

—Coda Hale

