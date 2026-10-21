If you develop applications that have some kind of server/backend for storing or pro‐ cessing data, and your applications use the internet (e.g., web applications, mobile apps, or internet-connected sensors), then this book is for you.

<!-- page 17 -->

This book is for software engineers, software architects, and technical managers who love to code. It is especially relevant if you need to make decisions about the architec‐ ture of the systems you work on—for example, if you need to choose tools for solving a given problem and figure out how best to apply them. But even if you have no choice over your tools, this book will help you better understand their strengths and weaknesses.

You should have some experience building web-based applications or network serv‐ ices, and you should be familiar with relational databases and SQL. Any nonrelational databases and other data-related tools you know are a bonus, but not required. A general understanding of common network protocols like TCP and HTTP is helpful. Your choice of programming language or framework makes no dif‐ ference for this book.

If any of the following are true for you, you’ll find this book valuable:

• You want to learn how to make data systems scalable, for example, to support web or mobile apps with millions of users.
• You need to make applications highly available (minimizing downtime) and operationally robust.
• You are looking for ways of making systems easier to maintain in the long run, even as they grow and as requirements and technologies change.
• You have a natural curiosity for the way things work and want to know what goes on inside major websites and online services. This book breaks down the internals of various databases and data processing systems, and it’s great fun to explore the bright thinking that went into their design.

Sometimes, when discussing scalable data systems, people make comments along the lines of, “You’re not Google or Amazon. Stop worrying about scale and just use a relational database.” There is truth in that statement: building for scale that you don’t need is wasted effort and may lock you into an inflexible design. In effect, it is a form of premature optimization. However, it’s also important to choose the right tool for the job, and different technologies each have their own strengths and weaknesses. As we shall see, relational databases are important but not the final word on dealing with data.

## Scope of This Book

This book does not attempt to give detailed instructions on how to install or use spe‐ cific software packages or APIs, since there is already plenty of documentation for those things. Instead we discuss the various principles and trade-offs that are funda‐ mental to data systems, and we explore the different design decisions taken by differ‐ ent products.

<!-- page 18 -->

In the ebook editions we have included links to the full text of online resources. All links were verified at the time of publication, but unfortunately links tend to break frequently due to the nature of the web. If you come across a broken link, or if you are reading a print copy of this book, you can look up references using a search engine. For academic papers, you can search for the title in Google Scholar to find open-access PDF files. Alternatively, you can find all of the references at https:// github.com/ept/ddia-references, where we maintain up-to-date links.

We look primarily at the architecture of data systems and the ways they are integrated into data-intensive applications. This book doesn’t have space to cover deployment, operations, security, management, and other areas—those are complex and impor‐ tant topics, and we wouldn’t do them justice by making them superficial side notes in this book. They deserve books of their own.

Many of the technologies described in this book fall within the realm of the Big Data buzzword. However, the term “Big Data” is so overused and underdefined that it is not useful in a serious engineering discussion. This book uses less ambiguous terms, such as single-node versus distributed systems, or online/interactive versus offline/ batch processing systems.

This book has a bias toward free and open source software (FOSS), because reading, modifying, and executing source code is a great way to understand how something works in detail. Open platforms also reduce the risk of vendor lock-in. However, where appropriate, we also discuss proprietary software (closed-source software, soft‐ ware as a service, or companies’ in-house software that is only described in literature but not released publicly).

## Outline of This Book

This book is arranged into three parts:

1. In Part I, we discuss the fundamental ideas that underpin the design of dataintensive applications. We start in Chapter 1 by discussing what we’re actually trying to achieve: reliability, scalability, and maintainability; how we need to think about them; and how we can achieve them. In Chapter 2 we compare sev‐ eral different data models and query languages, and see how they are appropriate to different situations. In Chapter 3 we talk about storage engines: how databases arrange data on disk so that we can find it again efficiently. Chapter 4 turns to formats for data encoding (serialization) and evolution of schemas over time.
2. In Part II, we move from data stored on one machine to data that is distributed across multiple machines. This is often necessary for scalability, but brings with it a variety of unique challenges. We first discuss replication (Chapter 5), parti‐ tioning/sharding (Chapter 6), and transactions (Chapter 7). We then go into

<!-- page 19 -->

more detail on the problems with distributed systems (Chapter 8) and what it means to achieve consistency and consensus in a distributed system (Chapter 9).

3. In Part III, we discuss systems that derive some datasets from other datasets. Derived data often occurs in heterogeneous systems: when there is no one data‐ base that can do everything well, applications need to integrate several different databases, caches, indexes, and so on. In Chapter 10 we start with a batch pro‐ cessing approach to derived data, and we build upon it with stream processing in Chapter 11. Finally, in Chapter 12 we put everything together and discuss approaches for building reliable, scalable, and maintainable applications in the future.

## References and Further Reading

