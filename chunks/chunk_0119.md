If Alice and Bob had hit reload at the same time, it would have been less surprising if they had gotten two different query results, because they wouldn’t know at exactly what time their respective requests were processed by the server. However, Bob knows that he hit the reload button (initiated his query) after he heard Alice exclaim the final score, and therefore he expects his query result to be at least as recent as Alice’s. The fact that his query returned a stale result is a violation of linearizability.

## What Makes a System Linearizable?

The basic idea behind linearizability is simple: to make a system appear as if there is only a single copy of the data. However, nailing down precisely what that means actually requires some care. In order to understand linearizability better, let’s look at some more examples.

Figure 9-2 shows three clients concurrently reading and writing the same key x in a linearizable database. In the distributed systems literature, x is called a register—in practice, it could be one key in a key-value store, one row in a relational database, or one document in a document database, for example.

<table>
<tr><th></th><th></th><th>time</th></tr>
<tr><td>read(x)</td><td>=1</td><td>-&gt;</td></tr>
<tr><td>- - read(x) = 0 or 1</td><td></td><td></td></tr>
</table>

= ok

Figure 9-2. If a read request is concurrent with a write request, it may return either the old or the new value.

For simplicity, Figure 9-2 shows only the requests from the clients’ point of view, not the internals of the database. Each bar is a request made by a client, where the start of a bar is the time when the request was sent, and the end of a bar is when the response was received by the client. Due to variable network delays, a client doesn’t know

<!-- page 348 -->

i. A subtle detail of this diagram is that it assumes the existence of a global clock, represented by the horizon‐ tal axis. Even though real systems typically don’t have accurate clocks (see “Unreliable Clocks” on page 287), this assumption is okay: for the purposes of analyzing a distributed algorithm, we may pretend that an accu‐ rate global clock exists, as long as the algorithm doesn’t have access to it [47]. Instead, the algorithm can only see a mangled approximation of real time, as produced by a quartz oscillator and NTP.

ii. A register in which reads may return either the old or the new value if they are concurrent with a write is known as a regular register [7, 25].

exactly when the database processed its request—it only knows that it must have hap‐ pened sometime between the client sending the request and receiving the response.i In this example, the register has two types of operations:

• read(x) ⇒ v means the client requested to read the value of register x, and the database returned the value v.
• write(x, v) ⇒ r means the client requested to set the register x to value v, and the database returned response r (which could be ok or error).

In Figure 9-2, the value of x is initially 0, and client C performs a write request to set it to 1. While this is happening, clients A and B are repeatedly polling the database to read the latest value. What are the possible responses that A and B might get for their read requests?

• The first read operation by client A completes before the write begins, so it must definitely return the old value 0.
• The last read by client A begins after the write has completed, so it must defi‐ nitely return the new value 1 if the database is linearizable: we know that the write must have been processed sometime between the start and end of the write operation, and the read must have been processed sometime between the start and end of the read operation. If the read started after the write ended, then the read must have been processed after the write, and therefore it must see the new value that was written.
• Any read operations that overlap in time with the write operation might return either 0 or 1, because we don’t know whether or not the write has taken effect at the time when the read operation is processed. These operations are concurrent with the write.

However, that is not yet sufficient to fully describe linearizability: if reads that are concurrent with a write can return either the old or the new value, then readers could see a value flip back and forth between the old and the new value several times while a write is going on. That is not what we expect of a system that emulates a “single copy of the data.”ii

<!-- page 349 -->

To make the system linearizable, we need to add another constraint, illustrated in Figure 9-3.

<table>
<tr><th></th><th></th><th></th><th></th><th></th><th>time</th></tr>
<tr><td></td><td>-</td><td>--</td><td>read(x)</td><td></td><td>&gt;1|--»</td></tr>
<tr><td>0</td><td>-</td><td>- - - read(x)</td><td>-</td><td>--</td><td>----»</td></tr>
<tr><td></td><td></td><td></td><td>=ok-</td><td></td><td>-»</td></tr>
</table>

Figure 9-3. After any one read has returned the new value, all following reads (on the same or other clients) must also return the new value.

In a linearizable system we imagine that there must be some point in time (between the start and end of the write operation) at which the value of x atomically flips from 0 to 1. Thus, if one client’s read returns the new value 1, all subsequent reads must also return the new value, even if the write operation has not yet completed.

This timing dependency is illustrated with an arrow in Figure 9-3. Client A is the first to read the new value, 1. Just after A’s read returns, B begins a new read. Since B’s read occurs strictly after A’s read, it must also return 1, even though the write by C is still ongoing. (It’s the same situation as with Alice and Bob in Figure 9-1: after Alice has read the new value, Bob also expects to read the new value.)

We can further refine this timing diagram to visualize each operation taking effect atomically at some point in time. A more complex example is shown in Figure 9-4 [10].

In Figure 9-4 we add a third type of operation besides read and write:

• cas(x, vold, vnew) ⇒ r means the client requested an atomic compare-and-set oper‐ ation (see “Compare-and-set” on page 245). If the current value of the register x equals vold, it should be atomically set to vnew. If x ≠ vold then the operation should leave the register unchanged and return an error. r is the database’s response (ok or error).

