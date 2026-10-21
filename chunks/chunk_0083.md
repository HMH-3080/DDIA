In practice, there is no one technique that can provide absolute guarantees. There are only various risk-reduction techniques, including writing to disk, replicating to remote machines, and backups—and they can and should be used together. As always, it’s wise to take any theoretical “guarantees” with a healthy grain of salt.

<!-- page 250 -->

ii. Arguably, an incorrect counter in an email application is not a particularly critical problem. Alternatively, think of a customer account balance instead of an unread counter, and a payment transaction instead of an email.

## Single-Object and Multi-Object Operations

To recap, in ACID, atomicity and isolation describe what the database should do if a client makes several writes within the same transaction:

## Atomicity

If an error occurs halfway through a sequence of writes, the transaction should be aborted, and the writes made up to that point should be discarded. In other words, the database saves you from having to worry about partial failure, by giv‐ ing an all-or-nothing guarantee.

## Isolation

Concurrently running transactions shouldn’t interfere with each other. For example, if one transaction makes several writes, then another transaction should see either all or none of those writes, but not some subset.

These definitions assume that you want to modify several objects (rows, documents, records) at once. Such multi-object transactions are often needed if several pieces of data need to be kept in sync. Figure 7-2 shows an example from an email application. To display the number of unread messages for a user, you could query something like:

## SELECT COUNT(*) FROM emails WHERE recipient_id = 2 AND unread_flag = true

However, you might find this query to be too slow if there are many emails, and decide to store the number of unread messages in a separate field (a kind of denorm‐ alization). Now, whenever a new message comes in, you have to increment the unread counter as well, and whenever a message is marked as read, you also have to decrement the unread counter.

In Figure 7-2, user 2 experiences an anomaly: the mailbox listing shows an unread message, but the counter shows zero unread messages because the counter increment has not yet happened.ii Isolation would have prevented this issue by ensuring that user 2 sees either both the inserted email and the updated counter, or neither, but not an inconsistent halfway point.

<!-- page 251 -->

<table>
<tr><th>insert into emails</th><th>update mailboxes</th><th></th></tr>
<tr><td>(recipient_id, body, unread_flag)</td><td>set unread = unread + 1</td><td></td></tr>
<tr><td>values(2, ‘Hello, true) User 1</td><td>where recipient_id = 2</td><td>time )</td></tr>
</table>

## Database

<table>
<tr><th>Hello, tr</th><th></th></tr>
<tr><td>body, unread_flag</td><td>select unread</td></tr>
<tr><td>from emails</td><td>from mailboxes</td></tr>
<tr><td>where recipient_id = 2</td><td>where recipient_id = 2</td></tr>
<tr><td>limit 50</td><td></td></tr>
</table>

Figure 7-2. Violating isolation: one transaction reads another transaction’s uncommit‐ ted writes (a “dirty read”).

Figure 7-3 illustrates the need for atomicity: if an error occurs somewhere over the course of the transaction, the contents of the mailbox and the unread counter might become out of sync. In an atomic transaction, if the update to the counter fails, the transaction is aborted and the inserted email is rolled back.

<table>
<tr><th>insert into emails</th><th>update mailboxes</th><th></th></tr>
<tr><td>(recipient_id, body, unread_flag)</td><td>set unread = unread + 1</td><td></td></tr>
<tr><td>values(2, ‘Hello, true) User 1</td><td>where recipient_id = 2</td><td>time</td></tr>
<tr><td></td><td>error or timeou</td><td></td></tr>
</table>

Database

Figure 7-3. Atomicity ensures that if an error occurs any prior writes from that transac‐ tion are undone, to avoid an inconsistent state.

Multi-object transactions require some way of determining which read and write operations belong to the same transaction. In relational databases, that is typically done based on the client’s TCP connection to the database server: on any particular connection, everything between a BEGIN TRANSACTION and a COMMIT statement is considered to be part of the same transaction.iii

iii. This is not ideal. If the TCP connection is interrupted, the transaction must be aborted. If the interruption happens after the client has requested a commit but before the server acknowledges that the commit hap‐ pened, the client doesn’t know whether the transaction was committed or not. To solve this issue, a transac‐ tion manager can group operations by a unique transaction identifier that is not bound to a particular TCP connection. We will return to this topic in “The End-to-End Argument for Databases” on page 516.

<!-- page 252 -->

iv. Strictly speaking, the term atomic increment uses the word atomic in the sense of multi-threaded pro‐ gramming. In the context of ACID, it should actually be called isolated or serializable increment. But that’s getting nitpicky.

On the other hand, many nonrelational databases don’t have such a way of grouping operations together. Even if there is a multi-object API (for example, a key-value store may have a multi-put operation that updates several keys in one operation), that doesn’t necessarily mean it has transaction semantics: the command may succeed for some keys and fail for others, leaving the database in a partially updated state.

## Single-object writes

Atomicity and isolation also apply when a single object is being changed. For exam‐ ple, imagine you are writing a 20 KB JSON document to a database:

• If the network connection is interrupted after the first 10 KB have been sent, does the database store that unparseable 10 KB fragment of JSON?
• If the power fails while the database is in the middle of overwriting the previous value on disk, do you end up with the old and new values spliced together?
• If another client reads that document while the write is in progress, will it see a partially updated value?

Those issues would be incredibly confusing, so storage engines almost universally aim to provide atomicity and isolation on the level of a single object (such as a keyvalue pair) on one node. Atomicity can be implemented using a log for crash recov‐ ery (see “Making B-trees reliable” on page 82), and isolation can be implemented using a lock on each object (allowing only one thread to access an object at any one time).

Some databases also provide more complex atomic operations,iv such as an increment operation, which removes the need for a read-modify-write cycle like that in Figure 7-1. Similarly popular is a compare-and-set operation, which allows a write to happen only if the value has not been concurrently changed by someone else (see “Compare-and-set” on page 245).

