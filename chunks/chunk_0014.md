[24] Jeffrey Dean and Luiz André Barroso: “The Tail at Scale,” Communications of the ACM, volume 56, number 2, pages 74–80, February 2013. doi: 10.1145/2408776.2408794 [25] Graham Cormode, Vladislav Shkapenyuk, Divesh Srivastava, and Bojian Xu: “Forward Decay: A Practical Time Decay Model for Streaming Systems,” at 25th IEEE International Conference on Data Engineering (ICDE), March 2009. [26] Ted Dunning and Otmar Ertl: “Computing Extremely Accurate Quantiles Using t-Digests,” github.com, March 2014. [27] Gil Tene: “HdrHistogram,” hdrhistogram.org. [28] Baron Schwartz: “Why Percentiles Don’t Work the Way You Think,” vividcor‐ tex.com, December 7, 2015. [29] James Hamilton: “On Designing and Deploying Internet-Scale Services,” at 21st Large Installation System Administration Conference (LISA), November 2007. [30] Brian Foote and Joseph Yoder: “Big Ball of Mud,” at 4th Conference on Pattern Languages of Programs (PLoP), September 1997. [31] Frederick P Brooks: “No Silver Bullet – Essence and Accident in Software Engi‐ neering,” in The Mythical Man-Month, Anniversary edition, Addison-Wesley, 1995. ISBN: 978-0-201-83595-3 [32] Ben Moseley and Peter Marks: “Out of the Tar Pit,” at BCS Software Practice Advancement (SPA), 2006. [33] Rich Hickey: “Simple Made Easy,” at Strange Loop, September 2011. [34] Hongyu Pei Breivold, Ivica Crnkovic, and Peter J. Eriksson: “Analyzing Software Evolvability,” at 32nd Annual IEEE International Computer Software and Applica‐ tions Conference (COMPSAC), July 2008. doi:10.1109/COMPSAC.2008.50

<!-- page 48 -->

<!-- page 49 -->

## Data Models and Query Languages

The limits of my language mean the limits of my world.

—Ludwig Wittgenstein, Tractatus Logico-Philosophicus (1922)

Data models are perhaps the most important part of developing software, because they have such a profound effect: not only on how the software is written, but also on how we think about the problem that we are solving.

Most applications are built by layering one data model on top of another. For each layer, the key question is: how is it represented in terms of the next-lower layer? For example:

1. As an application developer, you look at the real world (in which there are peo‐ ple, organizations, goods, actions, money flows, sensors, etc.) and model it in terms of objects or data structures, and APIs that manipulate those data struc‐ tures. Those structures are often specific to your application.
2. When you want to store those data structures, you express them in terms of a general-purpose data model, such as JSON or XML documents, tables in a rela‐ tional database, or a graph model.
3. The engineers who built your database software decided on a way of representing that JSON/XML/relational/graph data in terms of bytes in memory, on disk, or on a network. The representation may allow the data to be queried, searched, manipulated, and processed in various ways.
4. On yet lower levels, hardware engineers have figured out how to represent bytes in terms of electrical currents, pulses of light, magnetic fields, and more.

In a complex application there may be more intermediary levels, such as APIs built upon APIs, but the basic idea is still the same: each layer hides the complexity of the layers below it by providing a clean data model. These abstractions allow different

<!-- page 50 -->

groups of people—for example, the engineers at the database vendor and the applica‐ tion developers using their database—to work together effectively.

There are many different kinds of data models, and every data model embodies assumptions about how it is going to be used. Some kinds of usage are easy and some are not supported; some operations are fast and some perform badly; some data transformations feel natural and some are awkward.

It can take a lot of effort to master just one data model (think how many books there are on relational data modeling). Building software is hard enough, even when work‐ ing with just one data model and without worrying about its inner workings. But since the data model has such a profound effect on what the software above it can and can’t do, it’s important to choose one that is appropriate to the application.

In this chapter we will look at a range of general-purpose data models for data stor‐ age and querying (point 2 in the preceding list). In particular, we will compare the relational model, the document model, and a few graph-based data models. We will also look at various query languages and compare their use cases. In Chapter 3 we will discuss how storage engines work; that is, how these data models are actually implemented (point 3 in the list).

## Relational Model Versus Document Model

The best-known data model today is probably that of SQL, based on the relational model proposed by Edgar Codd in 1970 [1]: data is organized into relations (called tables in SQL), where each relation is an unordered collection of tuples (rows in SQL).

The relational model was a theoretical proposal, and many people at the time doubted whether it could be implemented efficiently. However, by the mid-1980s, relational database management systems (RDBMSes) and SQL had become the tools of choice for most people who needed to store and query data with some kind of reg‐ ular structure. The dominance of relational databases has lasted around 25‒30 years —an eternity in computing history.

The roots of relational databases lie in business data processing, which was performed on mainframe computers in the 1960s and ’70s. The use cases appear mundane from today’s perspective: typically transaction processing (entering sales or banking trans‐ actions, airline reservations, stock-keeping in warehouses) and batch processing (cus‐ tomer invoicing, payroll, reporting).

Other databases at that time forced application developers to think a lot about the internal representation of the data in the database. The goal of the relational model was to hide that implementation detail behind a cleaner interface.

Over the years, there have been many competing approaches to data storage and querying. In the 1970s and early 1980s, the network model and the hierarchical model

<!-- page 51 -->

were the main alternatives, but the relational model came to dominate them. Object databases came and went again in the late 1980s and early 1990s. XML databases appeared in the early 2000s, but have only seen niche adoption. Each competitor to the relational model generated a lot of hype in its time, but it never lasted [2].

