[82] Pat Helland: “Life Beyond Distributed Transactions: An Apostate’s Opinion,” at 3rd Biennial Conference on Innovative Data Systems Research (CIDR), January 2007. [83] Jonathan Oliver: “My Beef with MSDTC and Two-Phase Commits,” blog.jona‐ thanoliver.com, April 4, 2011. [84] Oren Eini (Ahende Rahien): “The Fallacy of Distributed Transactions,” ayende.com, July 17, 2014. [85] Clemens Vasters: “Transactions in Windows Azure (with Service Bus) – An Email Discussion,” vasters.com, July 30, 2012. [86] “Understanding Transactionality in Azure,” NServiceBus Documentation, Par‐ ticular Software, 2015. [87] Randy Wigginton, Ryan Lowe, Marcos Albe, and Fernando Ipar: “Distributed Transactions in MySQL,” at MySQL Conference and Expo, April 2013. [88] Mike Spille: “XA Exposed, Part I,” jroller.com, April 3, 2004. [89] Ajmer Dhariwal: “Orphaned MSDTC Transactions (-2 spids),” eraofdata.com, December 12, 2008. [90] Paul Randal: “Real World Story of DBCC PAGE Saving the Day,” sqlskills.com, June 19, 2013. [91] “in-doubt xact resolution Server Configuration Option,” SQL Server 2016 docu‐ mentation, Microsoft, Inc., 2016. [92] Cynthia Dwork, Nancy Lynch, and Larry Stockmeyer: “Consensus in the Pres‐ ence of Partial Synchrony,” Journal of the ACM, volume 35, number 2, pages 288– 323, April 1988. doi:10.1145/42282.42283 [93] Miguel Castro and Barbara H. Liskov: “Practical Byzantine Fault Tolerance and Proactive Recovery,” ACM Transactions on Computer Systems, volume 20, number 4, pages 396–461, November 2002. doi:10.1145/571637.571640 [94] Brian M. Oki and Barbara H. Liskov: “Viewstamped Replication: A New Primary Copy Method to Support Highly-Available Distributed Systems,” at 7th ACM Sympo‐ sium on Principles of Distributed Computing (PODC), August 1988. doi: 10.1145/62546.62549 [95] Barbara H. Liskov and James Cowling: “Viewstamped Replication Revisited,” Massachusetts Institute of Technology, Tech Report MIT-CSAIL-TR-2012-021, July 2012. [96] Leslie Lamport: “The Part-Time Parliament,” ACM Transactions on Computer Systems, volume 16, number 2, pages 133–169, May 1998. doi:10.1145/279227.279229

<!-- page 405 -->

[97] Leslie Lamport: “Paxos Made Simple,” ACM SIGACT News, volume 32, number 4, pages 51–58, December 2001.

[98] Tushar Deepak Chandra, Robert Griesemer, and Joshua Redstone: “Paxos Made Live – An Engineering Perspective,” at 26th ACM Symposium on Principles of Dis‐ tributed Computing (PODC), June 2007. [99] Robbert van Renesse: “Paxos Made Moderately Complex,” cs.cornell.edu, March 2011. [100] Diego Ongaro: “Consensus: Bridging Theory and Practice,” PhD Thesis, Stan‐ ford University, August 2014. [101] Heidi Howard, Malte Schwarzkopf, Anil Madhavapeddy, and Jon Crowcroft: “Raft Refloated: Do We Have Consensus?,” ACM SIGOPS Operating Systems Review, volume 49, number 1, pages 12–21, January 2015. doi:10.1145/2723872.2723876 [102] André Medeiros: “ZooKeeper’s Atomic Broadcast Protocol: Theory and Prac‐ tice,” Aalto University School of Science, March 20, 2012. [103] Robbert van Renesse, Nicolas Schiper, and Fred B. Schneider: “Vive La Différ‐ ence: Paxos vs. Viewstamped Replication vs. Zab,” IEEE Transactions on Dependable and Secure Computing, volume 12, number 4, pages 472–484, September 2014. doi: 10.1109/TDSC.2014.2355848 [104] Will Portnoy: “Lessons Learned from Implementing Paxos,” blog.willport‐ noy.com, June 14, 2012. [105] Heidi Howard, Dahlia Malkhi, and Alexander Spiegelman: “Flexible Paxos: Quorum Intersection Revisited,” arXiv:1608.06696, August 24, 2016. [106] Heidi Howard and Jon Crowcroft: “Coracle: Evaluating Consensus at the Inter‐ net Edge,” at Annual Conference of the ACM Special Interest Group on Data Commu‐ nication (SIGCOMM), August 2015. doi:10.1145/2829988.2790010 [107] Kyle Kingsbury: “Call Me Maybe: Elasticsearch 1.5.0,” aphyr.com, April 27, 2015. [108] Ivan Kelly: “BookKeeper Tutorial,” github.com, October 2014. [109] Camille Fournier: “Consensus Systems for the Skeptical Architect,” at Craft Conference, Budapest, Hungary, April 2015. [110] Kenneth P. Birman: “A History of the Virtual Synchrony Replication Model,” in Replication: Theory and Practice, Springer LNCS volume 5959, chapter 6, pages 91–120, 2010. ISBN: 978-3-642-11293-5, doi:10.1007/978-3-642-11294-2_6

<!-- page 406 -->

<!-- page 407 -->

## Derived Data

In Parts I and II of this book, we assembled from the ground up all the major consid‐ erations that go into a distributed database, from the layout of data on disk all the way to the limits of distributed consistency in the presence of faults. However, this discussion assumed that there was only one database in the application.

In reality, data systems are often more complex. In a large application you often need to be able to access and process data in many different ways, and there is no one data‐ base that can satisfy all those different needs simultaneously. Applications thus com‐ monly use a combination of several different datastores, indexes, caches, analytics systems, etc. and implement mechanisms for moving data from one store to another.

In this final part of the book, we will examine the issues around integrating multiple different data systems, potentially with different data models and optimized for dif‐ ferent access patterns, into one coherent application architecture. This aspect of system-building is often overlooked by vendors who claim that their product can sat‐ isfy all your needs. In reality, integrating disparate systems is one of the most impor‐ tant things that needs to be done in a nontrivial application.

<!-- page 408 -->

## Systems of Record and Derived Data

On a high level, systems that store and process data can be grouped into two broad categories:

## Systems of record

A system of record, also known as source of truth, holds the authoritative version of your data. When new data comes in, e.g., as user input, it is first written here. Each fact is represented exactly once (the representation is typically normalized). If there is any discrepancy between another system and the system of record, then the value in the system of record is (by definition) the correct one.

## Derived data systems

Data in a derived system is the result of taking some existing data from another system and transforming or processing it in some way. If you lose derived data, you can recreate it from the original source. A classic example is a cache: data can be served from the cache if present, but if the cache doesn’t contain what you need, you can fall back to the underlying database. Denormalized values, indexes, and materialized views also fall into this category. In recommendation systems, predictive summary data is often derived from usage logs.

Technically speaking, derived data is redundant, in the sense that it duplicates exist‐ ing information. However, it is often essential for getting good performance on read queries. It is commonly denormalized. You can derive several different datasets from a single source, enabling you to look at the data from different “points of view.”

Not all systems make a clear distinction between systems of record and derived data in their architecture, but it’s a very helpful distinction to make, because it clarifies the dataflow through your system: it makes explicit which parts of the system have which inputs and which outputs, and how they depend on each other.

