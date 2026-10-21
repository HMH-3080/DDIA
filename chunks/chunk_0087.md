Snapshot isolation is a popular feature: it is supported by PostgreSQL, MySQL with the InnoDB storage engine, Oracle, SQL Server, and others [23, 31, 32].

## Implementing snapshot isolation

Like read committed isolation, implementations of snapshot isolation typically use write locks to prevent dirty writes (see “Implementing read committed” on page 236), which means that a transaction that makes a write can block the progress of another transaction that writes to the same object. However, reads do not require any locks. From a performance point of view, a key principle of snapshot isolation is readers never block writers, and writers never block readers. This allows a database to handle long-running read queries on a consistent snapshot at the same time as processing writes normally, without any lock contention between the two.

To implement snapshot isolation, databases use a generalization of the mechanism we saw for preventing dirty reads in Figure 7-4. The database must potentially keep several different committed versions of an object, because various in-progress trans‐ actions may need to see the state of the database at different points in time. Because it maintains several versions of an object side by side, this technique is known as multiversion concurrency control (MVCC).

If a database only needed to provide read committed isolation, but not snapshot iso‐ lation, it would be sufficient to keep two versions of an object: the committed version and the overwritten-but-not-yet-committed version. However, storage engines that support snapshot isolation typically use MVCC for their read committed isolation level as well. A typical approach is that read committed uses a separate snapshot for each query, while snapshot isolation uses the same snapshot for an entire transaction.

Figure 7-7 illustrates how MVCC-based snapshot isolation is implemented in Post‐ greSQL [31] (other implementations are similar). When a transaction is started, it is given a unique, always-increasingvii transaction ID (txid). Whenever a transaction writes anything to the database, the data it writes is tagged with the transaction ID of the writer.

<!-- page 262 -->

<table>
<tr><th>select balance</th><th></th><th>select balance</th></tr>
<tr><td>from accounts</td><td></td><td>from accounts</td></tr>
<tr><td>where id = 1 Transaction Q</td><td>where id = 2</td><td>time</td></tr>
<tr><td></td><td></td><td>---&gt;</td></tr>
<tr><td>人 txid = 12</td><td></td><td>commit</td></tr>
<tr><td>00</td><td></td><td></td></tr>
<tr><td>Account 1</td><td></td><td></td></tr>
<tr><td>created by = 3 created by = 3</td><td></td><td></td></tr>
<tr><td>deleted by = 13 deleted by = nil</td><td></td><td></td></tr>
<tr><td>id = 1 id = 1</td><td></td><td></td></tr>
<tr><td>balance = 500 balance = 500</td><td></td><td>500</td></tr>
<tr><td>created by = 13</td><td></td><td></td></tr>
<tr><td>deleted by = nil</td><td></td><td></td></tr>
<tr><td>id = 1</td><td></td><td></td></tr>
<tr><td>balance = 600</td><td></td><td></td></tr>
<tr><td></td><td></td><td>V</td></tr>
<tr><td>Account 2</td><td></td><td></td></tr>
<tr><td>created by = 5</td><td></td><td>created by = 5</td></tr>
<tr><td>deleted by = nil</td><td></td><td>deleted by = 13</td></tr>
<tr><td>id = 2</td><td></td><td>id = 2</td></tr>
<tr><td>balance = 500</td><td></td><td>balance = 500</td></tr>
<tr><td></td><td></td><td>created by = 13</td></tr>
<tr><td></td><td></td><td>deleted by = nil</td></tr>
<tr><td>ok</td><td>ok</td><td>id = 2</td></tr>
<tr><td></td><td></td><td>balance = 400</td></tr>
<tr><td>Transaction Q</td><td></td><td></td></tr>
<tr><td>txid = 13</td><td></td><td></td></tr>
<tr><td>update accounts</td><td>update accounts commit</td><td></td></tr>
<tr><td>set balance =</td><td>set balance =</td><td></td></tr>
<tr><td>balance + 100</td><td>balance - 100</td><td></td></tr>
<tr><td>where id = 1</td><td>where id = 2</td><td></td></tr>
</table>

Figure 7-7. Implementing snapshot isolation using multi-version objects.

Each row in a table has a created_by field, containing the ID of the transaction that inserted this row into the table. Moreover, each row has a deleted_by field, which is initially empty. If a transaction deletes a row, the row isn’t actually deleted from the database, but it is marked for deletion by setting the deleted_by field to the ID of the transaction that requested the deletion. At some later time, when it is certain that no transaction can any longer access the deleted data, a garbage collection process in the database removes any rows marked for deletion and frees their space.

An update is internally translated into a delete and a create. For example, in Figure 7-7, transaction 13 deducts $100 from account 2, changing the balance from $500 to $400. The accounts table now actually contains two rows for account 2: a row with a balance of $500 which was marked as deleted by transaction 13, and a row with a balance of $400 which was created by transaction 13.

## Visibility rules for observing a consistent snapshot

When a transaction reads from the database, transaction IDs are used to decide which objects it can see and which are invisible. By carefully defining visibility rules,

<!-- page 263 -->

the database can present a consistent snapshot of the database to the application. This works as follows:

1. At the start of each transaction, the database makes a list of all the other transac‐ tions that are in progress (not yet committed or aborted) at that time. Any writes that those transactions have made are ignored, even if the transactions subse‐ quently commit.
2. Any writes made by aborted transactions are ignored.
3. Any writes made by transactions with a later transaction ID (i.e., which started after the current transaction started) are ignored, regardless of whether those transactions have committed.
4. All other writes are visible to the application’s queries.

These rules apply to both creation and deletion of objects. In Figure 7-7, when trans‐ action 12 reads from account 2, it sees a balance of $500 because the deletion of the $500 balance was made by transaction 13 (according to rule 3, transaction 12 cannot see a deletion made by transaction 13), and the creation of the $400 balance is not yet visible (by the same rule).

Put another way, an object is visible if both of the following conditions are true:

• At the time when the reader’s transaction started, the transaction that created the object had already committed.
• The object is not marked for deletion, or if it is, the transaction that requested deletion had not yet committed at the time when the reader’s transaction started.

A long-running transaction may continue using a snapshot for a long time, continu‐ ing to read values that (from other transactions’ point of view) have long been over‐ written or deleted. By never updating values in place but instead creating a new version every time a value is changed, the database can provide a consistent snapshot while incurring only a small overhead.

## Indexes and snapshot isolation

How do indexes work in a multi-version database? One option is to have the index simply point to all versions of an object and require an index query to filter out any object versions that are not visible to the current transaction. When garbage collec‐ tion removes old object versions that are no longer visible to any transaction, the cor‐ responding index entries can also be removed.

In practice, many implementation details determine the performance of multiversion concurrency control. For example, PostgreSQL has optimizations for avoid‐ ing index updates if different versions of the same object can fit on the same page [31].

