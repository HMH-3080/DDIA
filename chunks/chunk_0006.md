The Internet was done so well that most people think of it as a natural resource like the Pacific Ocean, rather than something that was man-made. When was the last time a tech‐ nology with a scale like that was so error-free?

—Alan Kay, in interview with Dr Dobb’s Journal (2012)

Many applications today are data-intensive, as opposed to compute-intensive. Raw CPU power is rarely a limiting factor for these applications—bigger problems are usually the amount of data, the complexity of data, and the speed at which it is changing.

A data-intensive application is typically built from standard building blocks that pro‐ vide commonly needed functionality. For example, many applications need to:

• Store data so that they, or another application, can find it again later (databases)
• Remember the result of an expensive operation, to speed up reads (caches)
• Allow users to search data by keyword or filter it in various ways (search indexes)
• Send a message to another process, to be handled asynchronously (stream pro‐ cessing)
• Periodically crunch a large amount of accumulated data (batch processing)

If that sounds painfully obvious, that’s just because these data systems are such a suc‐ cessful abstraction: we use them all the time without thinking too much. When build‐ ing an application, most engineers wouldn’t dream of writing a new data storage engine from scratch, because databases are a perfectly good tool for the job.

<!-- page 26 -->

But reality is not that simple. There are many database systems with different charac‐ teristics, because different applications have different requirements. There are vari‐ ous approaches to caching, several ways of building search indexes, and so on. When building an application, we still need to figure out which tools and which approaches are the most appropriate for the task at hand. And it can be hard to combine tools when you need to do something that a single tool cannot do alone.

This book is a journey through both the principles and the practicalities of data sys‐ tems, and how you can use them to build data-intensive applications. We will explore what different tools have in common, what distinguishes them, and how they achieve their characteristics.

In this chapter, we will start by exploring the fundamentals of what we are trying to achieve: reliable, scalable, and maintainable data systems. We’ll clarify what those things mean, outline some ways of thinking about them, and go over the basics that we will need for later chapters. In the following chapters we will continue layer by layer, looking at different design decisions that need to be considered when working on a data-intensive application.

## Thinking About Data Systems

We typically think of databases, queues, caches, etc. as being very different categories of tools. Although a database and a message queue have some superficial similarity— both store data for some time—they have very different access patterns, which means different performance characteristics, and thus very different implementations.

So why should we lump them all together under an umbrella term like data systems?

Many new tools for data storage and processing have emerged in recent years. They are optimized for a variety of different use cases, and they no longer neatly fit into traditional categories [1]. For example, there are datastores that are also used as mes‐ sage queues (Redis), and there are message queues with database-like durability guar‐ antees (Apache Kafka). The boundaries between the categories are becoming blurred.

Secondly, increasingly many applications now have such demanding or wide-ranging requirements that a single tool can no longer meet all of its data processing and stor‐ age needs. Instead, the work is broken down into tasks that can be performed effi‐ ciently on a single tool, and those different tools are stitched together using application code.

For example, if you have an application-managed caching layer (using Memcached or similar), or a full-text search server (such as Elasticsearch or Solr) separate from your main database, it is normally the application code’s responsibility to keep those caches and indexes in sync with the main database. Figure 1-1 gives a glimpse of what this may look like (we will go into detail in later chapters).

<!-- page 27 -->

<table>
<tr><th>O</th><th></th><th></th></tr>
<tr><td>• In-memory Client</td><td></td><td></td></tr>
<tr><td>cache requests</td><td></td><td></td></tr>
<tr><td>Read reque est Application</td><td>ch</td><td></td></tr>
<tr><td>first check</td><td></td><td></td></tr>
<tr><td>data is cache</td><td></td><td></td></tr>
<tr><td>Cache misses</td><td>Search</td><td></td></tr>
<tr><td>and writes</td><td>quests</td><td></td></tr>
<tr><td>r upd</td><td>Full-text</td><td>Message :</td></tr>
<tr><td>atab che</td><td>ndex</td><td>queu</td></tr>
<tr><td>Capture</td><td></td><td></td></tr>
<tr><td>change</td><td></td><td></td></tr>
<tr><td>o data</td><td>pply updates</td><td>n code</td></tr>
<tr><td></td><td>earch index</td><td></td></tr>
<tr><td></td><td></td><td>“Outside world”</td></tr>
</table>

Figure 1-1. One possible architecture for a data system that combines several components.

When you combine several tools in order to provide a service, the service’s interface or application programming interface (API) usually hides those implementation details from clients. Now you have essentially created a new, special-purpose data system from smaller, general-purpose components. Your composite data system may provide certain guarantees: e.g., that the cache will be correctly invalidated or upda‐ ted on writes so that outside clients see consistent results. You are now not only an application developer, but also a data system designer.

If you are designing a data system or service, a lot of tricky questions arise. How do you ensure that the data remains correct and complete, even when things go wrong internally? How do you provide consistently good performance to clients, even when parts of your system are degraded? How do you scale to handle an increase in load? What does a good API for the service look like?

There are many factors that may influence the design of a data system, including the skills and experience of the people involved, legacy system dependencies, the time‐ scale for delivery, your organization’s tolerance of different kinds of risk, regulatory constraints, etc. Those factors depend very much on the situation.

<!-- page 28 -->

In this book, we focus on three concerns that are important in most software systems:

## Reliability

The system should continue to work correctly (performing the correct function at the desired level of performance) even in the face of adversity (hardware or soft‐ ware faults, and even human error). See “Reliability” on page 6.

## Scalability

As the system grows (in data volume, traffic volume, or complexity), there should be reasonable ways of dealing with that growth. See “Scalability” on page 10.

## Maintainability

Over time, many different people will work on the system (engineering and oper‐ ations, both maintaining current behavior and adapting the system to new use cases), and they should all be able to work on it productively. See “Maintainabil‐ ity” on page 18.

