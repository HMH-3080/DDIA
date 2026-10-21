When the application makes a query (e.g., “How many doctors are currently on call?”), the database doesn’t know how the application logic uses the result of that query. To be safe, the database needs to assume that any change in the query result (the premise) means that writes in that transaction may be invalid. In other words, there may be a causal dependency between the queries and the writes in the transac‐ tion. In order to provide serializable isolation, the database must detect situations in

<!-- page 285 -->

which a transaction may have acted on an outdated premise and abort the transac‐ tion in that case.

How does the database know if a query result might have changed? There are two cases to consider:

• Detecting reads of a stale MVCC object version (uncommitted write occurred before the read)
• Detecting writes that affect prior reads (the write occurs after the read)

## Detecting stale MVCC reads

Recall that snapshot isolation is usually implemented by multi-version concurrency control (MVCC; see Figure 7-10). When a transaction reads from a consistent snap‐ shot in an MVCC database, it ignores writes that were made by any other transac‐ tions that hadn’t yet committed at the time when the snapshot was taken. In Figure 7-10, transaction 43 sees Alice as having on_call = true, because transaction 42 (which modified Alice’s on-call status) is uncommitted. However, by the time transaction 43 wants to commit, transaction 42 has already committed. This means that the write that was ignored when reading from the consistent snapshot has now taken effect, and transaction 43’s premise is no longer true.

<table>
<tr><th>select count(*)</th><th>update doctors</th><th></th></tr>
<tr><td>from doctors</td><td>set on_call = false</td><td></td></tr>
<tr><td>where on_call = true</td><td>where name = ‘Alice’</td><td></td></tr>
<tr><td>and shift_id = 1234 Transaction 42 ·</td><td>and shift_id = 1234</td><td>time</td></tr>
</table>

## Database

<table>
<tr><th>Transaction 43 -    -</th><th></th><th></th><th></th><th></th></tr>
<tr><td></td><td></td><td></td><td>select count(*)</td><td>update doctors commit retry…</td></tr>
<tr><td></td><td></td><td></td><td>from doctors</td><td>set on_call = false</td></tr>
<tr><td></td><td></td><td></td><td>where on_call = true</td><td>where name = ‘Bob’</td></tr>
<tr><td></td><td></td><td></td><td>and shift_id = 1234</td><td>and shift_id = 1234</td></tr>
<tr><td colspan="4">shift_id name on_call created_by deleted_by</td><td></td></tr>
<tr><td>1234</td><td>Alice</td><td>true</td><td>42</td><td>Transaction 42 hasn’t committed yet,</td></tr>
<tr><td>1234</td><td>Alice</td><td>false</td><td>42</td><td>so transaction 43 sees Alice as still</td></tr>
<tr><td></td><td></td><td></td><td></td><td>being on call. However, the transaction</td></tr>
<tr><td>1234</td><td>Bob</td><td>true</td><td></td><td>manager notes that this value is no</td></tr>
<tr><td>1234</td><td>Carol</td><td>- false</td><td></td><td>longer up-to-date.</td></tr>
</table>

Figure 7-10. Detecting when a transaction reads outdated values from an MVCC snapshot.

<!-- page 286 -->

In order to prevent this anomaly, the database needs to track when a transaction ignores another transaction’s writes due to MVCC visibility rules. When the transac‐ tion wants to commit, the database checks whether any of the ignored writes have now been committed. If so, the transaction must be aborted.

Why wait until committing? Why not abort transaction 43 immediately when the stale read is detected? Well, if transaction 43 was a read-only transaction, it wouldn’t need to be aborted, because there is no risk of write skew. At the time when transac‐ tion 43 makes its read, the database doesn’t yet know whether that transaction is going to later perform a write. Moreover, transaction 42 may yet abort or may still be uncommitted at the time when transaction 43 is committed, and so the read may turn out not to have been stale after all. By avoiding unnecessary aborts, SSI preserves snapshot isolation’s support for long-running reads from a consistent snapshot.

## Detecting writes that affect prior reads

The second case to consider is when another transaction modifies data after it has been read. This case is illustrated in Figure 7-11.

<table>
<tr><th>select count(*)</th><th>update doctors</th><th></th><th></th><th></th><th></th></tr>
<tr><td>from doctors</td><td>set on</td><td>call = false</td><td></td><td></td><td></td></tr>
<tr><td></td><td>all = tru e</td><td></td><td></td><td></td><td></td></tr>
<tr><td>nd sh Transaction 42</td><td>234 d</td><td></td><td></td><td></td><td>m</td></tr>
<tr><td>tabase Dat</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>ABORT</td></tr>
<tr><td>Transaction 43 · -</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>select count(*)</td><td></td><td colspan="2">update doctors</td><td></td><td>commit retry…</td></tr>
<tr><td>from doctors</td><td></td><td colspan="2">set on_call = false</td><td></td><td></td></tr>
<tr><td></td><td>where on_call = true</td><td colspan="2">where name = ‘Bob’</td><td></td><td></td></tr>
<tr><td></td><td>and shift_id = 1234</td><td colspan="2">and shift_id = 1234</td><td></td><td></td></tr>
<tr><td>key range</td><td>information</td><td></td><td colspan="3">shift_id name on_call</td></tr>
<tr><td>1234</td><td>read by transaction 42</td><td>old</td><td>1234</td><td>Alice</td><td>true</td></tr>
<tr><td>1234</td><td>read by transaction 43</td><td>new</td><td>1234</td><td>Alice</td><td>false</td></tr>
<tr><td colspan="2">Index-range locks on</td><td colspan="4">Note: update by transaction 42</td></tr>
<tr><td colspan="2">doctors.shift_id index</td><td colspan="4">affects read by transaction 43</td></tr>
</table>

Figure 7-11. In serializable snapshot isolation, detecting when one transaction modifies another transaction’s reads.

In the context of two-phase locking we discussed index-range locks (see “Index-range locks” on page 260), which allow the database to lock access to all rows matching some search query, such as WHERE shift_id = 1234. We can use a similar technique here, except that SSI locks don’t block other transactions.

<!-- page 287 -->

In Figure 7-11, transactions 42 and 43 both search for on-call doctors during shift 1234. If there is an index on shift_id, the database can use the index entry 1234 to record the fact that transactions 42 and 43 read this data. (If there is no index, this information can be tracked at the table level.) This information only needs to be kept for a while: after a transaction has finished (committed or aborted), and all concur‐ rent transactions have finished, the database can forget what data it read.

When a transaction writes to the database, it must look in the indexes for any other transactions that have recently read the affected data. This process is similar to acquiring a write lock on the affected key range, but rather than blocking until the readers have committed, the lock acts as a tripwire: it simply notifies the transactions that the data they read may no longer be up to date.

In Figure 7-11, transaction 43 notifies transaction 42 that its prior read is outdated, and vice versa. Transaction 42 is first to commit, and it is successful: although trans‐ action 43’s write affected 42, 43 hasn’t yet committed, so the write has not yet taken effect. However, when transaction 43 wants to commit, the conflicting write from 42 has already been committed, so 43 must abort.

## Performance of serializable snapshot isolation

As always, many engineering details affect how well an algorithm works in practice. For example, one trade-off is the granularity at which transactions’ reads and writes are tracked. If the database keeps track of each transaction’s activity in great detail, it can be precise about which transactions need to abort, but the bookkeeping overhead can become significant. Less detailed tracking is faster, but may lead to more transac‐ tions being aborted than strictly necessary.

In some cases, it’s okay for a transaction to read information that was overwritten by another transaction: depending on what else happened, it’s sometimes possible to prove that the result of the execution is nevertheless serializable. PostgreSQL uses this theory to reduce the number of unnecessary aborts [11, 41].

