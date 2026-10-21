Most commonly, the quorum is an absolute majority of more than half the nodes (although other kinds of quorums are possible). A majority quorum allows the sys‐ tem to continue working if individual nodes have failed (with three nodes, one failure can be tolerated; with five nodes, two failures can be tolerated). However, it is still safe, because there can only be only one majority in the system—there cannot be two majorities with conflicting decisions at the same time. We will discuss the use of quo‐ rums in more detail when we get to consensus algorithms in Chapter 9.

## The leader and the lock

Frequently, a system requires there to be only one of some thing. For example:

• Only one node is allowed to be the leader for a database partition, to avoid split brain (see “Handling Node Outages” on page 156).
• Only one transaction or client is allowed to hold the lock for a particular resource or object, to prevent concurrently writing to it and corrupting it.

<!-- page 324 -->

• Only one user is allowed to register a particular username, because a username must uniquely identify a user.

Implementing this in a distributed system requires care: even if a node believes that it is “the chosen one” (the leader of the partition, the holder of the lock, the request handler of the user who successfully grabbed the username), that doesn’t necessarily mean a quorum of nodes agrees! A node may have formerly been the leader, but if the other nodes declared it dead in the meantime (e.g., due to a network interruption or GC pause), it may have been demoted and another leader may have already been elected.

If a node continues acting as the chosen one, even though the majority of nodes have declared it dead, it could cause problems in a system that is not carefully designed. Such a node could send messages to other nodes in its self-appointed capacity, and if other nodes believe it, the system as a whole may do something incorrect.

For example, Figure 8-4 shows a data corruption bug due to an incorrect implemen‐ tation of locking. (The bug is not theoretical: HBase used to have this problem [74, 75].) Say you want to ensure that a file in a storage service can only be accessed by one client at a time, because if multiple clients tried to write to it, the file would become corrupted. You try to implement this by requiring a client to obtain a lease from a lock service before accessing the file.

<table>
<tr><th>client Lock</th><th></th><th>time client</th></tr>
<tr><td>service</td><td></td><td></td></tr>
<tr><td>Iease</td><td></td><td></td></tr>
<tr><td>top-the-w IG C paus</td><td></td><td></td></tr>
<tr><td></td><td></td><td>write</td></tr>
<tr><td></td><td></td><td>data</td></tr>
<tr><td></td><td>write</td><td></td></tr>
<tr><td></td><td>dat</td><td></td></tr>
<tr><td>Storage ]</td><td></td><td></td></tr>
</table>

Figure 8-4. Incorrect implementation of a distributed lock: client 1 believes that it still has a valid lease, even though it has expired, and thus corrupts a file in storage.

The problem is an example of what we discussed in “Process Pauses” on page 295: if the client holding the lease is paused for too long, its lease expires. Another client can obtain a lease for the same file, and start writing to the file. When the paused client comes back, it believes (incorrectly) that it still has a valid lease and proceeds to also write to the file. As a result, the clients’ writes clash and corrupt the file.

<!-- page 325 -->

## Fencing tokens

When using a lock or lease to protect access to some resource, such as the file storage in Figure 8-4, we need to ensure that a node that is under a false belief of being “the chosen one” cannot disrupt the rest of the system. A fairly simple technique that ach‐ ieves this goal is called fencing, and is illustrated in Figure 8-5.

<table>
<tr><th>Lock f service</th><th>lock held by client 1</th><th></th><th>lock held by client 2 time</th></tr>
<tr><td></td><td>get</td><td></td><td></td></tr>
<tr><td></td><td>lease token: 33</td><td></td><td></td></tr>
<tr><td></td><td></td><td>stop-the-world GC pause</td><td></td></tr>
<tr><td></td><td></td><td>leas</td><td></td></tr>
<tr><td></td><td></td><td></td><td>ken: 3 d token</td></tr>
<tr><td>Storage</td><td>- --</td><td></td><td></td></tr>
</table>

Figure 8-5. Making access to storage safe by allowing writes only in the order of increas‐ ing fencing tokens.

Let’s assume that every time the lock server grants a lock or lease, it also returns a fencing token, which is a number that increases every time a lock is granted (e.g., incremented by the lock service). We can then require that every time a client sends a write request to the storage service, it must include its current fencing token.

In Figure 8-5, client 1 acquires the lease with a token of 33, but then it goes into a long pause and the lease expires. Client 2 acquires the lease with a token of 34 (the number always increases) and then sends its write request to the storage service, including the token of 34. Later, client 1 comes back to life and sends its write to the storage service, including its token value 33. However, the storage server remembers that it has already processed a write with a higher token number (34), and so it rejects the request with token 33.

If ZooKeeper is used as lock service, the transaction ID zxid or the node version cversion can be used as fencing token. Since they are guaranteed to be monotoni‐ cally increasing, they have the required properties [74].

Note that this mechanism requires the resource itself to take an active role in check‐ ing tokens by rejecting any writes with an older token than one that has already been processed—it is not sufficient to rely on clients checking their lock status themselves. For resources that do not explicitly support fencing tokens, you might still be able work around the limitation (for example, in the case of a file storage service you could include the fencing token in the filename). However, some kind of check is necessary to avoid processing requests outside of the lock’s protection.

<!-- page 326 -->

Checking a token on the server side may seem like a downside, but it is arguably a good thing: it is unwise for a service to assume that its clients will always be well behaved, because the clients are often run by people whose priorities are very differ‐ ent from the priorities of the people running the service [76]. Thus, it is a good idea for any service to protect itself from accidentally abusive clients.

## Byzantine Faults

