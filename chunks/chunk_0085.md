For that reason, databases have long tried to hide concurrency issues from applica‐ tion developers by providing transaction isolation. In theory, isolation should make your life easier by letting you pretend that no concurrency is happening: serializable isolation means that the database guarantees that transactions have the same effect as if they ran serially (i.e., one at a time, without any concurrency).

In practice, isolation is unfortunately not that simple. Serializable isolation has a per‐ formance cost, and many databases don’t want to pay that price [8]. It’s therefore common for systems to use weaker levels of isolation, which protect against some concurrency issues, but not all. Those levels of isolation are much harder to under‐ stand, and they can lead to subtle bugs, but they are nevertheless used in practice [23].

Concurrency bugs caused by weak transaction isolation are not just a theoretical problem. They have caused substantial loss of money [24, 25], led to investigation by financial auditors [26], and caused customer data to be corrupted [27]. A popular comment on revelations of such problems is “Use an ACID database if you’re han‐ dling financial data!”—but that misses the point. Even many popular relational data‐ base systems (which are usually considered “ACID”) use weak isolation, so they wouldn’t necessarily have prevented these bugs from occurring.

Rather than blindly relying on tools, we need to develop a good understanding of the kinds of concurrency problems that exist, and how to prevent them. Then we can build applications that are reliable and correct, using the tools at our disposal.

In this section we will look at several weak (nonserializable) isolation levels that are used in practice, and discuss in detail what kinds of race conditions can and cannot occur, so that you can decide what level is appropriate to your application. Once we’ve done that, we will discuss serializability in detail (see “Serializability” on page

<!-- page 256 -->

251). Our discussion of isolation levels will be informal, using examples. If you want rigorous definitions and analyses of their properties, you can find them in the aca‐ demic literature [28, 29, 30].

## Read Committed

The most basic level of transaction isolation is read committed. v It makes two guaran‐ tees:

1. When reading from the database, you will only see data that has been committed (no dirty reads).
2. When writing to the database, you will only overwrite data that has been com‐ mitted (no dirty writes).

Let’s discuss these two guarantees in more detail.

## No dirty reads

Imagine a transaction has written some data to the database, but the transaction has not yet committed or aborted. Can another transaction see that uncommitted data? If yes, that is called a dirty read [2].

Transactions running at the read committed isolation level must prevent dirty reads. This means that any writes by a transaction only become visible to others when that transaction commits (and then all of its writes become visible at once). This is illus‐ trated in Figure 7-4, where user 1 has set x = 3, but user 2’s get x still returns the old value, 2, while user 1 has not yet committed.

User 1

User 2

Figure 7-4. No dirty reads: user 2 sees the new value for x only after user 1’s transaction has committed.

v. Some databases support an even weaker isolation level called read uncommitted. It prevents dirty writes, but does not prevent dirty reads.

<!-- page 257 -->

There are a few reasons why it’s useful to prevent dirty reads:

• If a transaction needs to update several objects, a dirty read means that another transaction may see some of the updates but not others. For example, in Figure 7-2, the user sees the new unread email but not the updated counter. This is a dirty read of the email. Seeing the database in a partially updated state is con‐ fusing to users and may cause other transactions to take incorrect decisions.
• If a transaction aborts, any writes it has made need to be rolled back (like in Figure 7-3). If the database allows dirty reads, that means a transaction may see data that is later rolled back—i.e., which is never actually committed to the data‐ base. Reasoning about the consequences quickly becomes mind-bending.

## No dirty writes

What happens if two transactions concurrently try to update the same object in a database? We don’t know in which order the writes will happen, but we normally assume that the later write overwrites the earlier write.

However, what happens if the earlier write is part of a transaction that has not yet committed, so the later write overwrites an uncommitted value? This is called a dirty write [28]. Transactions running at the read committed isolation level must prevent dirty writes, usually by delaying the second write until the first write’s transaction has committed or aborted.

By preventing dirty writes, this isolation level avoids some kinds of concurrency problems:

• If transactions update multiple objects, dirty writes can lead to a bad outcome. For example, consider Figure 7-5, which illustrates a used car sales website on which two people, Alice and Bob, are simultaneously trying to buy the same car. Buying a car requires two database writes: the listing on the website needs to be updated to reflect the buyer, and the sales invoice needs to be sent to the buyer. In the case of Figure 7-5, the sale is awarded to Bob (because he performs the winning update to the listings table), but the invoice is sent to Alice (because she performs the winning update to the invoices table). Read committed pre‐ vents such mishaps.
• However, read committed does not prevent the race condition between two counter increments in Figure 7-1. In this case, the second write happens after the first transaction has committed, so it’s not a dirty write. It’s still incorrect, but for a different reason—in “Preventing Lost Updates” on page 242 we will discuss how to make such counter increments safe.

<!-- page 258 -->

<table>
<tr><th>update listings</th><th>update invoices</th><th></th></tr>
<tr><td>set buyer = ‘Alice’</td><td>set recipient = ’Alice’</td><td></td></tr>
<tr><td>where id = 1234 $Alce\frac{f}{z}$</td><td>where listing_id = 1234</td><td>time</td></tr>
<tr><td></td><td>commit</td><td></td></tr>
<tr><td></td><td></td><td>= ‘Bob')</td></tr>
</table>

<table>
<tr><th>te listings</th><th>update invoices</th><th>commi</th></tr>
<tr><td>t buyer = ‘Bob’</td><td>set recipient = ‘Bob’</td><td></td></tr>
<tr><td>where id = 1234</td><td>where listing_id = 1234</td><td></td></tr>
</table>

Figure 7-5. With dirty writes, conflicting writes from different transactions can be mixed up.

## Implementing read committed

Read committed is a very popular isolation level. It is the default setting in Oracle 11g, PostgreSQL, SQL Server 2012, MemSQL, and many other databases [8].

