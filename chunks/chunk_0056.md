In this chapter we will assume that your dataset is so small that each machine can hold a copy of the entire dataset. In Chapter 6 we will relax that assumption and dis‐ cuss partitioning (sharding) of datasets that are too big for a single machine. In later chapters we will discuss various kinds of faults that can occur in a replicated data sys‐ tem, and how to deal with them.

If the data that you’re replicating does not change over time, then replication is easy: you just need to copy the data to every node once, and you’re done. All of the diffi‐ culty in replication lies in handling changes to replicated data, and that’s what this chapter is about. We will discuss three popular algorithms for replicating changes between nodes: single-leader, multi-leader, and leaderless replication. Almost all dis‐ tributed databases use one of these three approaches. They all have various pros and cons, which we will examine in detail.

<!-- page 174 -->

i. Different people have different definitions for hot, warm, and cold standby servers. In PostgreSQL, for example, hot standby is used to refer to a replica that accepts reads from clients, whereas a warm standby processes changes from the leader but doesn’t process any queries from clients. For purposes of this book, the difference isn’t important.

There are many trade-offs to consider with replication: for example, whether to use synchronous or asynchronous replication, and how to handle failed replicas. Those are often configuration options in databases, and although the details vary by data‐ base, the general principles are similar across many different implementations. We will discuss the consequences of such choices in this chapter.

Replication of databases is an old topic—the principles haven’t changed much since they were studied in the 1970s [1], because the fundamental constraints of networks have remained the same. However, outside of research, many developers continued to assume for a long time that a database consisted of just one node. Mainstream use of distributed databases is more recent. Since many application developers are new to this area, there has been a lot of misunderstanding around issues such as eventual consistency. In “Problems with Replication Lag” on page 161 we will get more precise about eventual consistency and discuss things like the read-your-writes and mono‐ tonic reads guarantees.

## Leaders and Followers

Each node that stores a copy of the database is called a replica. With multiple replicas, a question inevitably arises: how do we ensure that all the data ends up on all the rep‐ licas?

Every write to the database needs to be processed by every replica; otherwise, the rep‐ licas would no longer contain the same data. The most common solution for this is called leader-based replication (also known as active/passive or master–slave replica‐ tion) and is illustrated in Figure 5-1. It works as follows:

1. One of the replicas is designated the leader (also known as master or primary). When clients want to write to the database, they must send their requests to the leader, which first writes the new data to its local storage.
2. The other replicas are known as followers (read replicas, slaves, secondaries, or hot standbys).i Whenever the leader writes new data to its local storage, it also sends the data change to all of its followers as part of a replication log or change stream. Each follower takes the log from the leader and updates its local copy of the data‐ base accordingly, by applying all writes in the same order as they were processed on the leader.

<!-- page 175 -->

3. When a client wants to read from the database, it can query either the leader or any of the followers. However, writes are only accepted on the leader (the follow‐ ers are read-only from the client’s point of view).

<table>
<tr><th>User 1234</th><th></th></tr>
<tr><td></td><td>Leader</td></tr>
<tr><td>configures new</td><td></td></tr>
<tr><td>profile picture</td><td>rep</td></tr>
<tr><td>re</td><td>queries</td></tr>
<tr><td>N  upda</td><td></td></tr>
<tr><td></td><td>set picture_url = ‘me-new.jp</td></tr>
<tr><td></td><td>where user_id = 1234</td></tr>
</table>

old_ transaction: 987654321

r 2345 ws user 34’s profile

Figure 5-1. Leader-based (master–slave) replication.

This mode of replication is a built-in feature of many relational databases, such as PostgreSQL (since version 9.0), MySQL, Oracle Data Guard [2], and SQL Server’s AlwaysOn Availability Groups [3]. It is also used in some nonrelational databases, including MongoDB, RethinkDB, and Espresso [4]. Finally, leader-based replication is not restricted to only databases: distributed message brokers such as Kafka [5] and RabbitMQ highly available queues [6] also use it. Some network filesystems and replicated block devices such as DRBD are similar.

## Synchronous Versus Asynchronous Replication

An important detail of a replicated system is whether the replication happens syn‐ chronously or asynchronously. (In relational databases, this is often a configurable option; other systems are often hardcoded to be either one or the other.)

Think about what happens in Figure 5-1, where the user of a website updates their profile image. At some point in time, the client sends the update request to the leader; shortly afterward, it is received by the leader. At some point, the leader forwards the data change to the followers. Eventually, the leader notifies the client that the update was successful.

Figure 5-2 shows the communication between various components of the system: the user’s client, the leader, and two followers. Time flows from left to right. A request or response message is shown as a thick arrow.

<!-- page 176 -->

<table>
<tr><th></th><th>update users</th><th></th><th></th></tr>
<tr><td></td><td colspan="2">set picture_url = ’me-new.jpg’</td><td></td></tr>
<tr><td>9 User 1234</td><td>where user_id = 1234</td><td></td><td>time</td></tr>
<tr><td></td><td></td><td></td><td>k</td></tr>
<tr><td>Leader</td><td>-.</td><td>4</td><td>waiting for follower’s ok</td></tr>
<tr><td></td><td></td><td>data change</td><td>ok</td></tr>
<tr><td>Follower 1</td><td>.</td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td>data chan</td></tr>
<tr><td>Follower 2</td><td></td><td></td><td></td></tr>
</table>

Figure 5-2. Leader-based replication with one synchronous and one asynchronous fol‐ lower.

In the example of Figure 5-2, the replication to follower 1 is synchronous: the leader waits until follower 1 has confirmed that it received the write before reporting success to the user, and before making the write visible to other clients. The replication to follower 2 is asynchronous: the leader sends the message, but doesn’t wait for a response from the follower.

The diagram shows that there is a substantial delay before follower 2 processes the message. Normally, replication is quite fast: most database systems apply changes to followers in less than a second. However, there is no guarantee of how long it might take. There are circumstances when followers might fall behind the leader by several minutes or more; for example, if a follower is recovering from a failure, if the system is operating near maximum capacity, or if there are network problems between the nodes.

