If you add a new consumer to a messaging system, it typically only starts receiving messages sent after the time it was registered; any prior messages are already gone and cannot be recovered. Contrast this with files and databases, where you can add a new client at any time, and it can read data written arbitrarily far in the past (as long as it has not been explicitly overwritten or deleted by the application).

Why can we not have a hybrid, combining the durable storage approach of databases with the low-latency notification facilities of messaging? This is the idea behind logbased message brokers.

## Using logs for message storage

A log is simply an append-only sequence of records on disk. We previously discussed logs in the context of log-structured storage engines and write-ahead logs in Chap‐ ter 3, and in the context of replication in Chapter 5.

The same structure can be used to implement a message broker: a producer sends a message by appending it to the end of the log, and a consumer receives messages by reading the log sequentially. If a consumer reaches the end of the log, it waits for a notification that a new message has been appended. The Unix tool tail -f, which watches a file for data being appended, essentially works like this.

In order to scale to higher throughput than a single disk can offer, the log can be partitioned (in the sense of Chapter 6). Different partitions can then be hosted on dif‐ ferent machines, making each partition a separate log that can be read and written independently from other partitions. A topic can then be defined as a group of parti‐ tions that all carry messages of the same type. This approach is illustrated in Figure 11-3.

Within each partition, the broker assigns a monotonically increasing sequence num‐ ber, or offset, to every message (in Figure 11-3, the numbers in boxes are message off‐ sets). Such a sequence number makes sense because a partition is append-only, so the messages within a partition are totally ordered. There is no ordering guarantee across different partitions.

<!-- page 470 -->

<table>
<tr><th>&lt;</th><th>Parton0 1 | 2 | 3 | 4 | 3</th><th>•]</th><th>2]</th><th>•</th><th>9 |10]</th><th>append</th><th>Producer client</th></tr>
<tr><td>5</td><td colspan="4">Pantton1 | 1 | 2 | 3 | 4 5 | 6 | 7 | 8</td><td></td><td></td><td>Producer client</td></tr>
</table>

<table>
<tr><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th>Consumer group</th></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>onsumer client</td></tr>
<tr><td colspan="3">1]2 . Pammon1 | 1|2| 3 | §</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>fset for B.0 = 4 offset for B.1 = 5</td></tr>
<tr><td>Partition 2 1</td><td>2.</td><td>(3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>nt</td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>read sequentially</td><td></td></tr>
</table>

Figure 11-3. Producers send messages by appending them to a topic-partition file, and consumers read these files sequentially.

Apache Kafka [17, 18], Amazon Kinesis Streams [19], and Twitter’s DistributedLog [20, 21] are log-based message brokers that work like this. Google Cloud Pub/Sub is architecturally similar but exposes a JMS-style API rather than a log abstraction [16]. Even though these message brokers write all messages to disk, they are able to achieve throughput of millions of messages per second by partitioning across multiple machines, and fault tolerance by replicating messages [22, 23].

## Logs compared to traditional messaging

The log-based approach trivially supports fan-out messaging, because several con‐ sumers can independently read the log without affecting each other—reading a mes‐ sage does not delete it from the log. To achieve load balancing across a group of consumers, instead of assigning individual messages to consumer clients, the broker can assign entire partitions to nodes in the consumer group.

Each client then consumes all the messages in the partitions it has been assigned. Typically, when a consumer has been assigned a log partition, it reads the messages in the partition sequentially, in a straightforward single-threaded manner. This coarsegrained load balancing approach has some downsides:

<!-- page 471 -->

i. It’s possible to create a load balancing scheme in which two consumers share the work of processing a par‐ tition by having both read the full set of messages, but one of them only considers messages with evennumbered offsets while the other deals with the odd-numbered offsets. Alternatively, you could spread message processing over a thread pool, but that approach complicates consumer offset management. In gen‐ eral, single-threaded processing of a partition is preferable, and parallelism can be increased by using more partitions.

• The number of nodes sharing the work of consuming a topic can be at most the number of log partitions in that topic, because messages within the same parti‐ tion are delivered to the same node.i
• If a single message is slow to process, it holds up the processing of subsequent messages in that partition (a form of head-of-line blocking; see “Describing Per‐ formance” on page 13).

Thus, in situations where messages may be expensive to process and you want to par‐ allelize processing on a message-by-message basis, and where message ordering is not so important, the JMS/AMQP style of message broker is preferable. On the other hand, in situations with high message throughput, where each message is fast to pro‐ cess and where message ordering is important, the log-based approach works very well.

## Consumer offsets

Consuming a partition sequentially makes it easy to tell which messages have been processed: all messages with an offset less than a consumer’s current offset have already been processed, and all messages with a greater offset have not yet been seen. Thus, the broker does not need to track acknowledgments for every single message — it only needs to periodically record the consumer offsets. The reduced bookkeeping overhead and the opportunities for batching and pipelining in this approach help increase the throughput of log-based systems.

This offset is in fact very similar to the log sequence number that is commonly found in single-leader database replication, and which we discussed in “Setting Up New Followers” on page 155. In database replication, the log sequence number allows a follower to reconnect to a leader after it has become disconnected, and resume repli‐ cation without skipping any writes. Exactly the same principle is used here: the mes‐ sage broker behaves like a leader database, and the consumer like a follower.

If a consumer node fails, another node in the consumer group is assigned the failed consumer’s partitions, and it starts consuming messages at the last recorded offset. If the consumer had processed subsequent messages but not yet recorded their offset, those messages will be processed a second time upon restart. We will discuss ways of dealing with this issue later in the chapter.

<!-- page 472 -->

## Disk space usage

