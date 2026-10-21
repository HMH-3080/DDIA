<table>
<tr><th>Alice:</th><th></th><th></th><th>Bob:</th></tr>
<tr><td>^ begin transaction</td><td></td><td></td><td>o begin transaction</td></tr>
<tr><td></td><td>name</td><td>on call</td><td></td></tr>
<tr><td>o currently_on_call = (</td><td>Alice</td><td>true</td><td>o currently_on_call = (</td></tr>
<tr><td>select count(*) from doctors</td><td>Bob</td><td>true</td><td>select count(*) from doctors</td></tr>
<tr><td>where on_call = true</td><td>Carol</td><td>false</td><td>where on_call = true</td></tr>
<tr><td>and shift_id = 1234</td><td></td><td></td><td>and shift_id = 1234</td></tr>
<tr><td>)</td><td></td><td></td><td>)</td></tr>
<tr><td>Now currently_on_call = 2</td><td></td><td></td><td>Now currently_on_call = 2</td></tr>
<tr><td>o if (currently_on_call &gt;= 2) {</td><td></td><td></td><td></td></tr>
<tr><td>update doctors</td><td></td><td></td><td></td></tr>
<tr><td>Alice set on_call = false</td><td>false</td><td></td><td></td></tr>
<tr><td>where name = ‘Alice’</td><td></td><td></td><td></td></tr>
<tr><td>and shift_id = 1234</td><td></td><td></td><td>o if (currently_on_call &gt;=2){</td></tr>
<tr><td>J</td><td></td><td></td><td>update doctors</td></tr>
<tr><td></td><td></td><td>false Bob</td><td>set on_call = false</td></tr>
<tr><td></td><td></td><td></td><td>where name = ‘Bob’</td></tr>
<tr><td>o commit transaction</td><td></td><td></td><td></td></tr>
<tr><td></td><td>name</td><td>on_call</td><td>and shift_id = 1234</td></tr>
<tr><td></td><td></td><td></td><td>J</td></tr>
<tr><td></td><td>Alice</td><td>false</td><td></td></tr>
<tr><td></td><td>Bob</td><td>false</td><td></td></tr>
<tr><td></td><td></td><td></td><td>o commit transaction</td></tr>
<tr><td></td><td>Carol</td><td>false</td><td></td></tr>
</table>

Figure 7-8. Example of write skew causing an application bug.

In each transaction, your application first checks that two or more doctors are cur‐ rently on call; if yes, it assumes it’s safe for one doctor to go off call. Since the data‐ base is using snapshot isolation, both checks return 2, so both transactions proceed to the next stage. Alice updates her own record to take herself off call, and Bob updates his own record likewise. Both transactions commit, and now no doctor is on call. Your requirement of having at least one doctor on call has been violated.

## Characterizing write skew

This anomaly is called write skew [28]. It is neither a dirty write nor a lost update, because the two transactions are updating two different objects (Alice’s and Bob’s oncall records, respectively). It is less obvious that a conflict occurred here, but it’s defi‐ nitely a race condition: if the two transactions had run one after another, the second

<!-- page 270 -->

doctor would have been prevented from going off call. The anomalous behavior was only possible because the transactions ran concurrently.

You can think of write skew as a generalization of the lost update problem. Write skew can occur if two transactions read the same objects, and then update some of those objects (different transactions may update different objects). In the special case where different transactions update the same object, you get a dirty write or lost update anomaly (depending on the timing).

We saw that there are various different ways of preventing lost updates. With write skew, our options are more restricted:

• Atomic single-object operations don’t help, as multiple objects are involved.
• The automatic detection of lost updates that you find in some implementations of snapshot isolation unfortunately doesn’t help either: write skew is not auto‐ matically detected in PostgreSQL’s repeatable read, MySQL/InnoDB’s repeatable read, Oracle’s serializable, or SQL Server’s snapshot isolation level [23]. Auto‐ matically preventing write skew requires true serializable isolation (see “Serializa‐ bility” on page 251).
• Some databases allow you to configure constraints, which are then enforced by the database (e.g., uniqueness, foreign key constraints, or restrictions on a partic‐ ular value). However, in order to specify that at least one doctor must be on call, you would need a constraint that involves multiple objects. Most databases do not have built-in support for such constraints, but you may be able to implement them with triggers or materialized views, depending on the database [42].
• If you can’t use a serializable isolation level, the second-best option in this case is probably to explicitly lock the rows that the transaction depends on. In the doc‐ tors example, you could write something like the following:

BEGIN TRANSACTION;

SELECT * FROM doctors WHERE on_call = true AND shift_id = 1234 FOR UPDATE;

UPDATE doctors SET on_call = false WHERE name = 'Alice' AND shift_id = 1234;

COMMIT;

As before, FOR UPDATE tells the database to lock all rows returned by this query.

<!-- page 271 -->

ix. In PostgreSQL you can do this more elegantly using range types, but they are not widely supported in other databases.

## More examples of write skew

Write skew may seem like an esoteric issue at first, but once you’re aware of it, you may notice more situations in which it can occur. Here are some more examples:

## Meeting room booking system

Say you want to enforce that there cannot be two bookings for the same meeting room at the same time [43]. When someone wants to make a booking, you first check for any conflicting bookings (i.e., bookings for the same room with an overlapping time range), and if none are found, you create the meeting (see Example 7-2).ix

Example 7-2. A meeting room booking system tries to avoid double-booking (not safe under snapshot isolation)

BEGIN TRANSACTION;

-- Check for any existing bookings that overlap with the period of noon-1pm SELECT COUNT(*) FROM bookings

WHERE room_id = 123 AND

end_time > '2015-01-01 12:00' AND start_time < '2015-01-01 13:00';

-- If the previous query returned zero:

INSERT INTO bookings

(room_id, start_time, end_time, user_id) VALUES (123, '2015-01-01 12:00', '2015-01-01 13:00', 666);

COMMIT;

Unfortunately, snapshot isolation does not prevent another user from concur‐ rently inserting a conflicting meeting. In order to guarantee you won’t get sched‐ uling conflicts, you once again need serializable isolation.

## Multiplayer game

In Example 7-1, we used a lock to prevent lost updates (that is, making sure that two players can’t move the same figure at the same time). However, the lock doesn’t prevent players from moving two different figures to the same position on the board or potentially making some other move that violates the rules of the game. Depending on the kind of rule you are enforcing, you might be able to use a unique constraint, but otherwise you’re vulnerable to write skew.

<!-- page 272 -->

## Claiming a username

On a website where each user has a unique username, two users may try to create accounts with the same username at the same time. You may use a transaction to check whether a name is taken and, if not, create an account with that name. However, like in the previous examples, that is not safe under snapshot isolation. Fortunately, a unique constraint is a simple solution here (the second transaction that tries to register the username will be aborted due to violating the constraint).

## Preventing double-spending

A service that allows users to spend money or points needs to check that a user doesn’t spend more than they have. You might implement this by inserting a ten‐ tative spending item into a user’s account, listing all the items in the account, and checking that the sum is positive [44]. With write skew, it could happen that two spending items are inserted concurrently that together cause the balance to go negative, but that neither transaction notices the other.

## Phantoms causing write skew

All of these examples follow a similar pattern:

