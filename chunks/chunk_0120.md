Each operation in Figure 9-4 is marked with a vertical line (inside the bar for each operation) at the time when we think the operation was executed. Those markers are joined up in a sequential order, and the result must be a valid sequence of reads and writes for a register (every read must return the value set by the most recent write).

The requirement of linearizability is that the lines joining up the operation markers always move forward in time (from left to right), never backward. This requirement

<!-- page 350 -->

ensures the recency guarantee we discussed earlier: once a new value has been written or read, all subsequent reads see the value that was written, until it is overwritten again.

<table>
<tr><th></th><th>= k</th><th></th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td></td><td colspan="2">= 1 ][ cas(x, 1,2)</td><td></td><td></td><td></td><td>read(x)</td><td></td></tr>
<tr><td>read(x)</td><td>= 1]$</td><td>- read(x)</td><td>&gt; 2</td><td>-</td><td>cas(x, 2, 4)</td><td>= ok -</td><td>--</td></tr>
<tr><td></td><td>&gt; ok</td><td></td><td>(x, 0, 3)</td><td>z error</td><td></td><td></td><td></td></tr>
<tr><td>Database ]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>x=0 x=1 read read</td><td></td><td></td><td></td><td>read</td><td>x=4 read</td><td>ad</td><td></td></tr>
</table>

Figure 9-4. Visualizing the points in time at which the reads and writes appear to have taken effect. The final read by B is not linearizable.

There are a few interesting details to point out in Figure 9-4:

• First client B sent a request to read x, then client D sent a request to set x to 0, and then client A sent a request to set x to 1. Nevertheless, the value returned to B’s read is 1 (the value written by A). This is okay: it means that the database first processed D’s write, then A’s write, and finally B’s read. Although this is not the order in which the requests were sent, it’s an acceptable order, because the three requests are concurrent. Perhaps B’s read request was slightly delayed in the net‐ work, so it only reached the database after the two writes.
• Client B’s read returned 1 before client A received its response from the database, saying that the write of the value 1 was successful. This is also okay: it doesn’t mean the value was read before it was written, it just means the ok response from the database to client A was slightly delayed in the network.
• This model doesn’t assume any transaction isolation: another client may change a value at any time. For example, C first reads 1 and then reads 2, because the value was changed by B between the two reads. An atomic compare-and-set (cas) operation can be used to check the value hasn’t been concurrently changed by another client: B and C’s cas requests succeed, but D’s cas request fails (by the time the database processes it, the value of x is no longer 0).
• The final read by client B (in a shaded bar) is not linearizable. The operation is concurrent with C’s cas write, which updates x from 2 to 4. In the absence of

<!-- page 351 -->

other requests, it would be okay for B’s read to return 2. However, client A has already read the new value 4 before B’s read started, so B is not allowed to read an older value than A. Again, it’s the same situation as with Alice and Bob in Figure 9-1.

That is the intuition behind linearizability; the formal definition [6] describes it more precisely. It is possible (though computationally expensive) to test whether a system’s behavior is linearizable by recording the timings of all requests and responses, and checking whether they can be arranged into a valid sequential order [11].

## Linearizability Versus Serializability

Linearizability is easily confused with serializability (see “Serializability” on page 251), as both words seem to mean something like “can be arranged in a sequential order.” However, they are two quite different guarantees, and it is important to distinguish between them:

## Serializability

Serializability is an isolation property of transactions, where every transaction may read and write multiple objects (rows, documents, records)—see “Single- Object and Multi-Object Operations” on page 228. It guarantees that transac‐ tions behave the same as if they had executed in some serial order (each transaction running to completion before the next transaction starts). It is okay for that serial order to be different from the order in which transactions were actually run [12].

## Linearizability

Linearizability is a recency guarantee on reads and writes of a register (an indi‐ vidual object). It doesn’t group operations together into transactions, so it does not prevent problems such as write skew (see “Write Skew and Phantoms” on page 246), unless you take additional measures such as materializing conflicts (see “Materializing conflicts” on page 251).

A database may provide both serializability and linearizability, and this combination is known as strict serializability or strong one-copy serializability (strong-1SR) [4, 13]. Implementations of serializability based on two-phase locking (see “Two-Phase Lock‐ ing (2PL)” on page 257) or actual serial execution (see “Actual Serial Execution” on page 252) are typically linearizable.

However, serializable snapshot isolation (see “Serializable Snapshot Isolation (SSI)” on page 261) is not linearizable: by design, it makes reads from a consistent snapshot, to avoid lock contention between readers and writers. The whole point of a consistent snapshot is that it does not include writes that are more recent than the snapshot, and thus reads from the snapshot are not linearizable.

<!-- page 352 -->

iii. Strictly speaking, ZooKeeper and etcd provide linearizable writes, but reads may be stale, since by default they can be served by any one of the replicas. You can optionally request a linearizable read: etcd calls this a quorum read [16], and in ZooKeeper you need to call sync() before the read [15]; see “Implementing linear‐ izable storage using total order broadcast” on page 350.

## Relying on Linearizability

In what circumstances is linearizability useful? Viewing the final score of a sporting match is perhaps a frivolous example: a result that is outdated by a few seconds is unlikely to cause any real harm in this situation. However, there a few areas in which linearizability is an important requirement for making a system work correctly.

## Locking and leader election

A system that uses single-leader replication needs to ensure that there is indeed only one leader, not several (split brain). One way of electing a leader is to use a lock: every node that starts up tries to acquire the lock, and the one that succeeds becomes the leader [14]. No matter how this lock is implemented, it must be linearizable: all nodes must agree which node owns the lock; otherwise it is useless.

