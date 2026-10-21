In our example, the function in question was duplicate suppression. We saw that TCP suppresses duplicate packets at the TCP connection level, and some stream process‐ ors provide so-called exactly-once semantics at the message processing level, but that is not enough to prevent a user from submitting a duplicate request if the first one times out. By themselves, TCP, database transactions, and stream processors cannot entirely rule out these duplicates. Solving the problem requires an end-to-end solu‐ tion: a transaction identifier that is passed all the way from the end-user client to the database.

The end-to-end argument also applies to checking the integrity of data: checksums built into Ethernet, TCP, and TLS can detect corruption of packets in the network, but they cannot detect corruption due to bugs in the software at the sending and receiving ends of the network connection, or corruption on the disks where the data is stored. If you want to catch all possible sources of data corruption, you also need end-to-end checksums.

A similar argument applies with encryption [55]: the password on your home WiFi network protects against people snooping your WiFi traffic, but not against attackers elsewhere on the internet; TLS/SSL between your client and the server protects

<!-- page 542 -->

against network attackers, but not against compromises of the server. Only end-toend encryption and authentication can protect against all of these things.

Although the low-level features (TCP duplicate suppression, Ethernet checksums, WiFi encryption) cannot provide the desired end-to-end features by themselves, they are still useful, since they reduce the probability of problems at the higher levels. For example, HTTP requests would often get mangled if we didn’t have TCP putting the packets back in the right order. We just need to remember that the low-level reliabil‐ ity features are not by themselves sufficient to ensure end-to-end correctness.

## Applying end-to-end thinking in data systems

This brings me back to my original thesis: just because an application uses a data sys‐ tem that provides comparatively strong safety properties, such as serializable transac‐ tions, that does not mean the application is guaranteed to be free from data loss or corruption. The application itself needs to take end-to-end measures, such as dupli‐ cate suppression, as well.

That is a shame, because fault-tolerance mechanisms are hard to get right. Low-level reliability mechanisms, such as those in TCP, work quite well, and so the remaining higher-level faults occur fairly rarely. It would be really nice to wrap up the remain‐ ing high-level fault-tolerance machinery in an abstraction so that application code needn’t worry about it—but I fear that we have not yet found the right abstraction.

Transactions have long been seen as a good abstraction, and I do believe that they are useful. As discussed in the introduction to Chapter 7, they take a wide range of possi‐ ble issues (concurrent writes, constraint violations, crashes, network interruptions, disk failures) and collapse them down to two possible outcomes: commit or abort. That is a huge simplification of the programming model, but I fear that it is not enough.

Transactions are expensive, especially when they involve heterogeneous storage tech‐ nologies (see “Distributed Transactions in Practice” on page 360). When we refuse to use distributed transactions because they are too expensive, we end up having to reimplement fault-tolerance mechanisms in application code. As numerous examples throughout this book have shown, reasoning about concurrency and partial failure is difficult and counterintuitive, and so I suspect that most application-level mecha‐ nisms do not work correctly. The consequence is lost or corrupted data.

For these reasons, I think it is worth exploring fault-tolerance abstractions that make it easy to provide application-specific end-to-end correctness properties, but also maintain good performance and good operational characteristics in a large-scale dis‐ tributed environment.

<!-- page 543 -->

## Enforcing Constraints

Let’s think about correctness in the context of the ideas around unbundling databases (“Unbundling Databases” on page 499). We saw that end-to-end duplicate suppres‐ sion can be achieved with a request ID that is passed all the way from the client to the database that records the write. What about other kinds of constraints?

In particular, let’s focus on uniqueness constraints—such as the one we relied on in Example 12-2. In “Constraints and uniqueness guarantees” on page 330 we saw sev‐ eral other examples of application features that need to enforce uniqueness: a user‐ name or email address must uniquely identify a user, a file storage service cannot have more than one file with the same name, and two people cannot book the same seat on a flight or in a theater.

Other kinds of constraints are very similar: for example, ensuring that an account balance never goes negative, that you don’t sell more items than you have in stock in the warehouse, or that a meeting room does not have overlapping bookings. Techni‐ ques that enforce uniqueness can often be used for these kinds of constraints as well.

## Uniqueness constraints require consensus

In Chapter 9 we saw that in a distributed setting, enforcing a uniqueness constraint requires consensus: if there are several concurrent requests with the same value, the system somehow needs to decide which one of the conflicting operations is accepted, and reject the others as violations of the constraint.

The most common way of achieving this consensus is to make a single node the leader, and put it in charge of making all the decisions. That works fine as long as you don’t mind funneling all requests through a single node (even if the client is on the other side of the world), and as long as that node doesn’t fail. If you need to tolerate the leader failing, you’re back at the consensus problem again (see “Single-leader rep‐ lication and consensus” on page 367).

Uniqueness checking can be scaled out by partitioning based on the value that needs to be unique. For example, if you need to ensure uniqueness by request ID, as in Example 12-2, you can ensure all requests with the same request ID are routed to the same partition (see Chapter 6). If you need usernames to be unique, you can partition by hash of username.

However, asynchronous multi-master replication is ruled out, because it could hap‐ pen that different masters concurrently accept conflicting writes, and thus the values are no longer unique (see “Implementing Linearizable Systems” on page 332). If you want to be able to immediately reject any writes that would violate the constraint, synchronous coordination is unavoidable [56].

<!-- page 544 -->

## Uniqueness in log-based messaging

