The simplest way of avoiding concurrency problems is to remove the concurrency entirely: to execute only one transaction at a time, in serial order, on a single thread. By doing so, we completely sidestep the problem of detecting and preventing con‐ flicts between transactions: the resulting isolation is by definition serializable.

<!-- page 275 -->

Even though this seems like an obvious idea, database designers only fairly recently— around 2007—decided that a single-threaded loop for executing transactions was fea‐ sible [45]. If multi-threaded concurrency was considered essential for getting good performance during the previous 30 years, what changed to make single-threaded execution possible?

Two developments caused this rethink:

• RAM became cheap enough that for many use cases is now feasible to keep the entire active dataset in memory (see “Keeping everything in memory” on page 88). When all data that a transaction needs to access is in memory, transactions can execute much faster than if they have to wait for data to be loaded from disk.
• Database designers realized that OLTP transactions are usually short and only make a small number of reads and writes (see “Transaction Processing or Ana‐ lytics?” on page 90). By contrast, long-running analytic queries are typically readonly, so they can be run on a consistent snapshot (using snapshot isolation) outside of the serial execution loop.

The approach of executing transactions serially is implemented in VoltDB/H-Store, Redis, and Datomic [46, 47, 48]. A system designed for single-threaded execution can sometimes perform better than a system that supports concurrency, because it can avoid the coordination overhead of locking. However, its throughput is limited to that of a single CPU core. In order to make the most of that single thread, transac‐ tions need to be structured differently from their traditional form.

## Encapsulating transactions in stored procedures

In the early days of databases, the intention was that a database transaction could encompass an entire flow of user activity. For example, booking an airline ticket is a multi-stage process (searching for routes, fares, and available seats; deciding on an itinerary; booking seats on each of the flights of the itinerary; entering passenger details; making payment). Database designers thought that it would be neat if that entire process was one transaction so that it could be committed atomically.

Unfortunately, humans are very slow to make up their minds and respond. If a data‐ base transaction needs to wait for input from a user, the database needs to support a potentially huge number of concurrent transactions, most of them idle. Most data‐ bases cannot do that efficiently, and so almost all OLTP applications keep transac‐ tions short by avoiding interactively waiting for a user within a transaction. On the web, this means that a transaction is committed within the same HTTP request—a transaction does not span multiple requests. A new HTTP request starts a new trans‐ action.

Even though the human has been taken out of the critical path, transactions have continued to be executed in an interactive client/server style, one statement at a time.

<!-- page 276 -->

An application makes a query, reads the result, perhaps makes another query depending on the result of the first query, and so on. The queries and results are sent back and forth between the application code (running on one machine) and the data‐ base server (on another machine).

In this interactive style of transaction, a lot of time is spent in network communica‐ tion between the application and the database. If you were to disallow concurrency in the database and only process one transaction at a time, the throughput would be dreadful because the database would spend most of its time waiting for the applica‐ tion to issue the next query for the current transaction. In this kind of database, it’s necessary to process multiple transactions concurrently in order to get reasonable performance.

For this reason, systems with single-threaded serial transaction processing don’t allow interactive multi-statement transactions. Instead, the application must submit the entire transaction code to the database ahead of time, as a stored procedure. The differences between these approaches is illustrated in Figure 7-9. Provided that all data required by a transaction is in memory, the stored procedure can execute very fast, without waiting for any network or disk I/O.

Interactive transaction:

<table>
<tr><th>select count(*)</th><th>if (currently_</th><th>update doctors</th></tr>
<tr><td>from doctors</td><td>on_call \geq 2) {</td><td>set on_call = false</td></tr>
<tr><td>where on_call = true</td><td></td><td>where name = ‘Bob’</td></tr>
<tr><td>and shift_id = 1234 Application</td><td></td><td>time and shift_id = 1234</td></tr>
<tr><td></td><td></td><td>k</td></tr>
<tr><td>Query processor</td><td></td><td></td></tr>
<tr><td>Storage  ---</td><td></td><td></td></tr>
<tr><td>Stored procedure:</td><td>execute stored procedure</td><td></td></tr>
<tr><td></td><td>take_doctor_off_call_if_safe</td><td></td></tr>
<tr><td></td><td>with name = ‘Bob, shift_id = 1234</td><td>time</td></tr>
<tr><td>Application  - -</td><td></td><td></td></tr>
<tr><td></td><td>ok</td><td></td></tr>
<tr><td>Query processor</td><td></td><td></td></tr>
<tr><td></td><td>ok</td><td></td></tr>
<tr><td>Storage .</td><td>-4</td><td></td></tr>
</table>

Figure 7-9. The difference between an interactive transaction and a stored procedure (using the example transaction of Figure 7-8).

<!-- page 277 -->

## Pros and cons of stored procedures

Stored procedures have existed for some time in relational databases, and they have been part of the SQL standard (SQL/PSM) since 1999. They have gained a somewhat bad reputation, for various reasons:

• Each database vendor has its own language for stored procedures (Oracle has PL/ SQL, SQL Server has T-SQL, PostgreSQL has PL/pgSQL, etc.). These languages haven’t kept up with developments in general-purpose programming languages, so they look quite ugly and archaic from today’s point of view, and they lack the ecosystem of libraries that you find with most programming languages.
• Code running in a database is difficult to manage: compared to an application server, it’s harder to debug, more awkward to keep in version control and deploy, trickier to test, and difficult to integrate with a metrics collection system for monitoring.
• A database is often much more performance-sensitive than an application server, because a single database instance is often shared by many application servers. A badly written stored procedure (e.g., using a lot of memory or CPU time) in a database can cause much more trouble than equivalent badly written code in an application server.

However, those issues can be overcome. Modern implementations of stored proce‐ dures have abandoned PL/SQL and use existing general-purpose programming lan‐ guages instead: VoltDB uses Java or Groovy, Datomic uses Java or Clojure, and Redis uses Lua.

With stored procedures and in-memory data, executing all transactions on a single thread becomes feasible. As they don’t need to wait for I/O and they avoid the over‐ head of other concurrency control mechanisms, they can achieve quite good throughput on a single thread.

