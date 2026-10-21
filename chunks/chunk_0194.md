One of the most effective approaches is to make the operation idempotent (see “Idempotence” on page 478); that is, to ensure that it has the same effect, no matter whether it is executed once or multiple times. However, taking an operation that is not naturally idempotent and making it idempotent requires some effort and care: you may need to maintain some additional metadata (such as the set of operation IDs that have updated a value), and ensure fencing when failing over from one node to another (see “The leader and the lock” on page 301).

## Duplicate suppression

The same pattern of needing to suppress duplicates occurs in many other places besides stream processing. For example, TCP uses sequence numbers on packets to put them in the correct order at the recipient, and to determine whether any packets were lost or duplicated on the network. Any lost packets are retransmitted and any duplicates are removed by the TCP stack before it hands the data to an application.

However, this duplicate suppression only works within the context of a single TCP connection. Imagine the TCP connection is a client’s connection to a database, and it is currently executing the transaction in Example 12-1. In many databases, a transac‐ tion is tied to a client connection (if the client sends several queries, the database knows that they belong to the same transaction because they are sent on the same TCP connection). If the client suffers a network interruption and connection timeout after sending the COMMIT, but before hearing back from the database server, it does not know whether the transaction has been committed or aborted (Figure 8-1).

## Example 12-1. A nonidempotent transfer of money from one account to another

BEGIN TRANSACTION;

UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;

UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;

COMMIT;

The client can reconnect to the database and retry the transaction, but now it is out‐ side of the scope of TCP duplicate suppression. Since the transaction in Example 12-1 is not idempotent, it could happen that $22 is transferred instead of the desired $11. Thus, even though Example 12-1 is a standard example for transaction atomicity, it is actually not correct, and real banks do not work like this [3].

Two-phase commit (see “Atomic Commit and Two-Phase Commit (2PC)” on page 354) protocols break the 1:1 mapping between a TCP connection and a transaction, since they must allow a transaction coordinator to reconnect to a database after a net‐

<!-- page 540 -->

work fault, and tell it whether to commit or abort an in-doubt transaction. Is this suf‐ ficient to ensure that the transaction will only be executed once? Unfortunately not.

Even if we can suppress duplicate transactions between the database client and server, we still need to worry about the network between the end-user device and the application server. For example, if the end-user client is a web browser, it probably uses an HTTP POST request to submit an instruction to the server. Perhaps the user is on a weak cellular data connection, and they succeed in sending the POST, but the signal becomes too weak before they are able to receive the response from the server.

In this case, the user will probably be shown an error message, and they may retry manually. Web browsers warn, “Are you sure you want to submit this form again?”— and the user says yes, because they wanted the operation to happen. (The Post/Redi‐ rect/Get pattern [54] avoids this warning message in normal operation, but it doesn’t help if the POST request times out.) From the web server’s point of view the retry is a separate request, and from the database’s point of view it is a separate transaction. The usual deduplication mechanisms don’t help.

## Operation identifiers

To make the operation idempotent through several hops of network communication, it is not sufficient to rely just on a transaction mechanism provided by a database — you need to consider the end-to-end flow of the request.

For example, you could generate a unique identifier for an operation (such as a UUID) and include it as a hidden form field in the client application, or calculate a hash of all the relevant form fields to derive the operation ID [3]. If the web browser submits the POST request twice, the two requests will have the same operation ID. You can then pass that operation ID all the way through to the database and check that you only ever execute one operation with a given ID, as shown in Example 12-2.

Example 12-2. Suppressing duplicate requests using a unique ID

ALTER TABLE requests ADD UNIQUE (request_id);

BEGIN TRANSACTION;

INSERT INTO requests

(request_id, from_account, to_account, amount)

VALUES('0286FDB8-D7E1-423F-B40B-792B3608036C', 4321, 1234, 11.00);

UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;

UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;

COMMIT;

<!-- page 541 -->

Example 12-2 relies on a uniqueness constraint on the request_id column. If a transaction attempts to insert an ID that already exists, the INSERT fails and the trans‐ action is aborted, preventing it from taking effect twice. Relational databases can gen‐ erally maintain a uniqueness constraint correctly, even at weak isolation levels (whereas an application-level check-then-insert may fail under nonserializable isola‐ tion, as discussed in “Write Skew and Phantoms” on page 246).

Besides suppressing duplicate requests, the requests table in Example 12-2 acts as a kind of event log, hinting in the direction of event sourcing (see “Event Sourcing” on page 457). The updates to the account balances don’t actually have to happen in the same transaction as the insertion of the event, since they are redundant and could be derived from the request event in a downstream consumer—as long as the event is processed exactly once, which can again be enforced using the request ID.

## The end-to-end argument

This scenario of suppressing duplicate transactions is just one example of a more general principle called the end-to-end argument, which was articulated by Saltzer, Reed, and Clark in 1984 [55]:

The function in question can completely and correctly be implemented only with the knowledge and help of the application standing at the endpoints of the communica‐ tion system. Therefore, providing that questioned function as a feature of the commu‐ nication system itself is not possible. (Sometimes an incomplete version of the function provided by the communication system may be useful as a performance enhance‐ ment.)

