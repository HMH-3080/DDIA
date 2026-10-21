11. Stream Processing. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 439 Transmitting Event Streams 440 Messaging Systems 441 Partitioned Logs 446 Databases and Streams 451 Keeping Systems in Sync 452 Change Data Capture 454 Event Sourcing 457 459 State, Streams, and Immutability Processing Streams 464 Uses of Stream Processing 465 Reasoning About Time 468 Stream Joins 472 Fault Tolerance 476 Summary 479

<!-- page 14 -->

12. The Future of Data Systems. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 489 Data Integration 490 Combining Specialized Tools by Deriving Data 490 Batch and Stream Processing 494 Unbundling Databases 499 499 Composing Data Storage Technologies Designing Applications Around Dataflow 504 Observing Derived State 509 Aiming for Correctness 515 The End-to-End Argument for Databases 516 Enforcing Constraints 521 Timeliness and Integrity 524 Trust, but Verify 528 533 Doing the Right Thing Predictive Analytics 533 Privacy and Tracking 536 Summary 543 Glossary. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 553 Index. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 559

<!-- page 15 -->

## Preface

If you have worked in software engineering in recent years, especially in server-side and backend systems, you have probably been bombarded with a plethora of buzz‐ words relating to storage and processing of data. NoSQL! Big Data! Web-scale! Sharding! Eventual consistency! ACID! CAP theorem! Cloud services! MapReduce! Real-time!

In the last decade we have seen many interesting developments in databases, in dis‐ tributed systems, and in the ways we build applications on top of them. There are various driving forces for these developments:

• Internet companies such as Google, Yahoo!, Amazon, Facebook, LinkedIn, Microsoft, and Twitter are handling huge volumes of data and traffic, forcing them to create new tools that enable them to efficiently handle such scale.
• Businesses need to be agile, test hypotheses cheaply, and respond quickly to new market insights by keeping development cycles short and data models flexible.
• Free and open source software has become very successful and is now preferred to commercial or bespoke in-house software in many environments.
• CPU clock speeds are barely increasing, but multi-core processors are standard, and networks are getting faster. This means parallelism is only going to increase.
• Even if you work on a small team, you can now build systems that are distributed across many machines and even multiple geographic regions, thanks to infra‐ structure as a service (IaaS) such as Amazon Web Services.
• Many services are now expected to be highly available; extended downtime due to outages or maintenance is becoming increasingly unacceptable.

Data-intensive applications are pushing the boundaries of what is possible by making use of these technological developments. We call an application data-intensive if data is its primary challenge—the quantity of data, the complexity of data, or the speed at

<!-- page 16 -->

which it is changing—as opposed to compute-intensive, where CPU cycles are the bottleneck.

The tools and technologies that help data-intensive applications store and process data have been rapidly adapting to these changes. New types of database systems (“NoSQL”) have been getting lots of attention, but message queues, caches, search indexes, frameworks for batch and stream processing, and related technologies are very important too. Many applications use some combination of these.

The buzzwords that fill this space are a sign of enthusiasm for the new possibilities, which is a great thing. However, as software engineers and architects, we also need to have a technically accurate and precise understanding of the various technologies and their trade-offs if we want to build good applications. For that understanding, we have to dig deeper than buzzwords.

Fortunately, behind the rapid changes in technology, there are enduring principles that remain true, no matter which version of a particular tool you are using. If you understand those principles, you’re in a position to see where each tool fits in, how to make good use of it, and how to avoid its pitfalls. That’s where this book comes in.

The goal of this book is to help you navigate the diverse and fast-changing landscape of technologies for processing and storing data. This book is not a tutorial for one particular tool, nor is it a textbook full of dry theory. Instead, we will look at examples of successful data systems: technologies that form the foundation of many popular applications and that have to meet scalability, performance, and reliability require‐ ments in production every day.

We will dig into the internals of those systems, tease apart their key algorithms, dis‐ cuss their principles and the trade-offs they have to make. On this journey, we will try to find useful ways of thinking about data systems—not just how they work, but also why they work that way, and what questions we need to ask.

After reading this book, you will be in a great position to decide which kind of tech‐ nology is appropriate for which purpose, and understand how tools can be combined to form the foundation of a good application architecture. You won’t be ready to build your own database storage engine from scratch, but fortunately that is rarely necessary. You will, however, develop a good intuition for what your systems are doing under the hood so that you can reason about their behavior, make good design decisions, and track down any problems that may arise.

## Who Should Read This Book?

