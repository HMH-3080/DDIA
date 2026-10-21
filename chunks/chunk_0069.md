Thus, whenever you have two operations A and B, there are three possibilities: either A happened before B, or B happened before A, or A and B are concurrent. What we need is an algorithm to tell us whether two operations are concurrent or not. If one operation happened before another, the later operation should overwrite the earlier operation, but if the operations are concurrent, we have a conflict that needs to be resolved.

## Concurrency, Time, and Relativity

It may seem that two operations should be called concurrent if they occur “at the same time”—but in fact, it is not important whether they literally overlap in time. Because of problems with clocks in distributed systems, it is actually quite difficult to tell whether two things happened at exactly the same time—an issue we will discuss in more detail in Chapter 8.

For defining concurrency, exact time doesn’t matter: we simply call two operations concurrent if they are both unaware of each other, regardless of the physical time at which they occurred. People sometimes make a connection between this principle and the special theory of relativity in physics [54], which introduced the idea that information cannot travel faster than the speed of light. Consequently, two events that occur some distance apart cannot possibly affect each other if the time between the events is shorter than the time it takes light to travel the distance between them.

In computer systems, two operations might be concurrent even though the speed of light would in principle have allowed one operation to affect the other. For example, if the network was slow or interrupted at the time, two operations can occur some time apart and still be concurrent, because the network problems prevented one operation from being able to know about the other.

## Capturing the happens-before relationship

Let’s look at an algorithm that determines whether two operations are concurrent, or whether one happened before another. To keep things simple, let’s start with a data‐

<!-- page 210 -->

base that has only one replica. Once we have worked out how to do this on a single replica, we can generalize the approach to a leaderless database with multiple replicas.

Figure 5-13 shows two clients concurrently adding items to the same shopping cart. (If that example strikes you as too inane, imagine instead two air traffic controllers concurrently adding aircraft to the sector they are tracking.) Initially, the cart is empty. Between them, the clients make five writes to the database:

1. Client 1 adds milk to the cart. This is the first write to that key, so the server suc‐ cessfully stores it and assigns it version 1. The server also echoes the value back to the client, along with the version number.
2. Client 2 adds eggs to the cart, not knowing that client 1 concurrently added milk (client 2 thought that its eggs were the only item in the cart). The server assigns version 2 to this write, and stores eggs and milk as two separate values. It then returns both values to the client, along with the version number of 2.
3. Client 1, oblivious to client 2’s write, wants to add flour to the cart, so it thinks the current cart contents should be [milk, flour]. It sends this value to the server, along with the version number 1 that the server gave client 1 previously. The server can tell from the version number that the write of [milk, flour] supersedes the prior value of [milk] but that it is concurrent with [eggs]. Thus, the server assigns version 3 to [milk, flour], overwrites the version 1 value [milk], but keeps the version 2 value [eggs] and returns both remaining values to the client.
4. Meanwhile, client 2 wants to add ham to the cart, unaware that client 1 just added flour. Client 2 received the two values [milk] and [eggs] from the server in the last response, so the client now merges those values and adds ham to form a new value, [eggs, milk, ham]. It sends that value to the server, along with the previ‐ ous version number 2. The server detects that version 2 overwrites [eggs] but is concurrent with [milk, flour], so the two remaining values are [milk, flour] with version 3, and [eggs, milk, ham] with version 4.
5. Finally, client 1 wants to add bacon. It previously received [milk, flour] and [eggs] from the server at version 3, so it merges those, adds bacon, and sends the final value [milk, flour, eggs, bacon] to the server, along with the version number 3. This overwrites [milk, flour] (note that [eggs] was already over‐ written in the last step) but is concurrent with [eggs, milk, ham], so the server keeps those two concurrent values.

<!-- page 211 -->

<table>
<tr><th></th><th></th><th>set key: cart</th><th>set key: cart</th></tr>
<tr><td>set key: cart</td><td>3</td><td>value: [milk, flour]</td><td>value: [milk, flour, eggs, bacon]</td></tr>
<tr><td>value: [milk] + Client 1</td><td></td><td>version: 1</td><td>version: 3 - &gt; time</td></tr>
<tr><td></td><td>ok</td><td></td><td>ok</td></tr>
<tr><td></td><td>version: 1</td><td>version: 3</td><td>version: 5</td></tr>
<tr><td></td><td>value: [milk]</td><td>value: [milk, flour]</td><td>value: [milk, flour,</td></tr>
<tr><td></td><td></td><td>value: [eggs]</td><td>eggs, bacon]</td></tr>
<tr><td></td><td></td><td></td><td>value: [eggs, milk, ham]</td></tr>
<tr><td>Database</td><td></td><td></td><td>- &gt;</td></tr>
<tr><td></td><td></td><td>ok</td><td>ok</td></tr>
<tr><td></td><td></td><td>e</td><td>version: 4</td></tr>
<tr><td></td><td></td><td>valu</td><td>value: [eggs, milk, ham]</td></tr>
<tr><td></td><td></td><td>valu</td><td>value: [milk, flour]</td></tr>
<tr><td></td><td>set key:</td><td>et key:</td><td></td></tr>
<tr><td></td><td>value: [e</td><td>gs] value: [eggs, milk, ham]</td><td></td></tr>
<tr><td></td><td></td><td>version: 2</td><td></td></tr>
</table>

Figure 5-13. Capturing causal dependencies between two clients concurrently editing a shopping cart.

The dataflow between the operations in Figure 5-13 is illustrated graphically in Figure 5-14. The arrows indicate which operation happened before which other oper‐ ation, in the sense that the later operation knew about or depended on the earlier one. In this example, the clients are never fully up to date with the data on the server, since there is always another operation going on concurrently. But old versions of the value do get overwritten eventually, and no writes are lost.

Figure 5-14. Graph of causal dependencies in Figure 5-13.

Note that the server can determine whether two operations are concurrent by looking at the version numbers—it does not need to interpret the value itself (so the value could be any data structure). The algorithm works as follows:

<!-- page 212 -->

