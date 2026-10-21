This can happen if a user makes several reads from different replicas. For example, Figure 5-4 shows user 2345 making the same query twice, first to a follower with little lag, then to a follower with greater lag. (This scenario is quite likely if the user refreshes a web page, and each request is routed to a random server.) The first query returns a comment that was recently added by user 1234, but the second query doesn’t return anything because the lagging follower has not yet picked up that write. In effect, the second query is observing the system at an earlier point in time than the first query. This wouldn’t be so bad if the first query hadn’t returned anything, because user 2345 probably wouldn’t know that user 1234 had recently added a com‐

<!-- page 187 -->

ment. However, it’s very confusing for user 2345 if they first see user 1234’s comment appear, and then see it disappear again.

<table>
<tr><th></th><th>insert into comments</th></tr>
<tr><td></td><td>(author, reply_to, message)</td></tr>
<tr><td>User 1234</td><td>time Sounds good!’)</td></tr>
<tr><td></td><td>sert</td></tr>
<tr><td>Leader</td><td></td></tr>
<tr><td></td><td>insert into</td></tr>
<tr><td></td><td>comments..</td></tr>
<tr><td>Follower1</td><td>--</td></tr>
<tr><td></td><td>t into</td></tr>
<tr><td></td><td>I result</td></tr>
<tr><td></td><td>ent</td></tr>
<tr><td>Follower 2  ]</td><td></td></tr>
</table>

<table>
<tr><th>select * from comments</th><th>select * from comments</th></tr>
<tr><td>where reply_to = 55555</td><td>where reply_to = 55555</td></tr>
</table>

Figure 5-4. A user first reads from a fresh replica, then from a stale replica. Time appears to go backward. To prevent this anomaly, we need monotonic reads.

Monotonic reads [23] is a guarantee that this kind of anomaly does not happen. It’s a lesser guarantee than strong consistency, but a stronger guarantee than eventual con‐ sistency. When you read data, you may see an old value; monotonic reads only means that if one user makes several reads in sequence, they will not see time go backward— i.e., they will not read older data after having previously read newer data.

One way of achieving monotonic reads is to make sure that each user always makes their reads from the same replica (different users can read from different replicas). For example, the replica can be chosen based on a hash of the user ID, rather than randomly. However, if that replica fails, the user’s queries will need to be rerouted to another replica.

## Consistent Prefix Reads

Our third example of replication lag anomalies concerns violation of causality. Imag‐ ine the following short dialog between Mr. Poons and Mrs. Cake:

## Mr. Poons

How far into the future can you see, Mrs. Cake?

Mrs. Cake

About ten seconds usually, Mr. Poons.

<!-- page 188 -->

There is a causal dependency between those two sentences: Mrs. Cake heard Mr. Poons’s question and answered it.

Now, imagine a third person is listening to this conversation through followers. The things said by Mrs. Cake go through a follower with little lag, but the things said by Mr. Poons have a longer replication lag (see Figure 5-5). This observer would hear the following:

## Mrs. Cake

About ten seconds usually, Mr. Poons.

## Mr. Poons

How far into the future can you see, Mrs. Cake?

To the observer it looks as though Mrs. Cake is answering the question before Mr. Poons has even asked it. Such psychic powers are impressive, but very confusing [25].

<table>
<tr><th></th><th></th><th>time</th></tr>
<tr><td>Mr. Poo</td><td></td><td></td></tr>
<tr><td>Partition 1 f</td><td></td><td></td></tr>
<tr><td>Leader</td><td></td><td></td></tr>
<tr><td>Partition 1</td><td></td><td></td></tr>
<tr><td>Follower</td><td></td><td></td></tr>
<tr><td></td><td></td><td>“About ten seconds</td></tr>
<tr><td></td><td></td><td>◦ usually, Mr. Poons.”</td></tr>
<tr><td>Partition 2</td><td></td><td></td></tr>
<tr><td>Leader</td><td></td><td></td></tr>
<tr><td>Partition 2 Follower</td><td>—</td><td>.</td></tr>
<tr><td colspan="2">Observer }</td><td>-</td></tr>
<tr><td></td><td></td><td>“About ten seconds “How far into the future</td></tr>
<tr><td></td><td></td><td>can you see, Mrs. Cake?” usually, Mr. Poons.”</td></tr>
</table>

Figure 5-5. If some partitions are replicated slower than others, an observer may see the answer before they see the question.

Preventing this kind of anomaly requires another type of guarantee: consistent prefix reads [23]. This guarantee says that if a sequence of writes happens in a certain order, then anyone reading those writes will see them appear in the same order.

This is a particular problem in partitioned (sharded) databases, which we will discuss in Chapter 6. If the database always applies writes in the same order, reads always see a consistent prefix, so this anomaly cannot happen. However, in many distributed

<!-- page 189 -->

databases, different partitions operate independently, so there is no global ordering of writes: when a user reads from the database, they may see some parts of the database in an older state and some in a newer state.

One solution is to make sure that any writes that are causally related to each other are written to the same partition—but in some applications that cannot be done effi‐ ciently. There are also algorithms that explicitly keep track of causal dependencies, a topic that we will return to in “The “happens-before” relationship and concurrency” on page 186.

## Solutions for Replication Lag

When working with an eventually consistent system, it is worth thinking about how the application behaves if the replication lag increases to several minutes or even hours. If the answer is “no problem,” that’s great. However, if the result is a bad expe‐ rience for users, it’s important to design the system to provide a stronger guarantee, such as read-after-write. Pretending that replication is synchronous when in fact it is asynchronous is a recipe for problems down the line.

As discussed earlier, there are ways in which an application can provide a stronger guarantee than the underlying database—for example, by performing certain kinds of reads on the leader. However, dealing with these issues in application code is com‐ plex and easy to get wrong.

It would be better if application developers didn’t have to worry about subtle replica‐ tion issues and could just trust their databases to “do the right thing.” This is why transactions exist: they are a way for a database to provide stronger guarantees so that the application can be simpler.

Single-node transactions have existed for a long time. However, in the move to dis‐ tributed (replicated and partitioned) databases, many systems have abandoned them, claiming that transactions are too expensive in terms of performance and availability, and asserting that eventual consistency is inevitable in a scalable system. There is some truth in that statement, but it is overly simplistic, and we will develop a more nuanced view over the course of the rest of this book. We will return to the topic of transactions in Chapters 7 and 9, and we will discuss some alternative mechanisms in Part III.

<!-- page 190 -->

iv. If the database is partitioned (see Chapter 6), each partition has one leader. Different partitions may have their leaders on different nodes, but each partition must nevertheless have one leader node.

## Multi-Leader Replication

