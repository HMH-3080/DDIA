Although the system can be more reliable than its underlying parts, there is always a limit to how much more reliable it can be. For example, error-correcting codes can deal with a small number of single-bit errors, but if your signal is swamped by inter‐ ference, there is a fundamental limit to how much data you can get through your communication channel [13]. TCP can hide packet loss, duplication, and reordering from you, but it cannot magically remove delays in the network.

Although the more reliable higher-level system is not perfect, it’s still useful because it takes care of some of the tricky low-level faults, and so the remaining faults are usu‐ ally easier to reason about and deal with. We will explore this matter further in “The end-to-end argument” on page 519.

## Unreliable Networks

As discussed in the introduction to Part II, the distributed systems we focus on in this book are shared-nothing systems: i.e., a bunch of machines connected by a network. The network is the only way those machines can communicate—we assume that each

<!-- page 300 -->

machine has its own memory and disk, and one machine cannot access another machine’s memory or disk (except by making requests to a service over the network).

Shared-nothing is not the only way of building systems, but it has become the domi‐ nant approach for building internet services, for several reasons: it’s comparatively cheap because it requires no special hardware, it can make use of commoditized cloud computing services, and it can achieve high reliability through redundancy across multiple geographically distributed datacenters.

The internet and most internal networks in datacenters (often Ethernet) are asyn‐ chronous packet networks. In this kind of network, one node can send a message (a packet) to another node, but the network gives no guarantees as to when it will arrive, or whether it will arrive at all. If you send a request and expect a response, many things could go wrong (some of which are illustrated in Figure 8-1):

1. Your request may have been lost (perhaps someone unplugged a network cable).
2. Your request may be waiting in a queue and will be delivered later (perhaps the network or the recipient is overloaded).
3. The remote node may have failed (perhaps it crashed or it was powered down).
4. The remote node may have temporarily stopped responding (perhaps it is expe‐ riencing a long garbage collection pause; see “Process Pauses” on page 295), but it will start responding again later.
5. The remote node may have processed your request, but the response has been lost on the network (perhaps a network switch has been misconfigured).
6. The remote node may have processed your request, but the response has been delayed and will be delivered later (perhaps the network or your own machine is overloaded).

<table>
<tr><th>(a)</th><th>(b)</th><th>(c)</th></tr>
<tr><td>m</td><td>???</td><td>??</td></tr>
<tr><td>-. Network _</td><td></td><td></td></tr>
<tr><td>Service</td><td>ode unresponsive</td><td></td></tr>
</table>

Figure 8-1. If you send a request and don’t get a response, it’s not possible to distinguish whether (a) the request was lost, (b) the remote node is down, or (c) the response was lost.

<!-- page 301 -->

The sender can’t even tell whether the packet was delivered: the only option is for the recipient to send a response message, which may in turn be lost or delayed. These issues are indistinguishable in an asynchronous network: the only information you have is that you haven’t received a response yet. If you send a request to another node and don’t receive a response, it is impossible to tell why.

The usual way of handling this issue is a timeout: after some time you give up waiting and assume that the response is not going to arrive. However, when a timeout occurs, you still don’t know whether the remote node got your request or not (and if the request is still queued somewhere, it may still be delivered to the recipient, even if the sender has given up on it).

## Network Faults in Practice

We have been building computer networks for decades—one might hope that by now we would have figured out how to make them reliable. However, it seems that we have not yet succeeded.

There are some systematic studies, and plenty of anecdotal evidence, showing that network problems can be surprisingly common, even in controlled environments like a datacenter operated by one company [14]. One study in a medium-sized datacenter found about 12 network faults per month, of which half disconnected a single machine, and half disconnected an entire rack [15]. Another study measured the fail‐ ure rates of components like top-of-rack switches, aggregation switches, and load bal‐ ancers [16]. It found that adding redundant networking gear doesn’t reduce faults as much as you might hope, since it doesn’t guard against human error (e.g., misconfig‐ ured switches), which is a major cause of outages.

Public cloud services such as EC2 are notorious for having frequent transient net‐ work glitches [14], and well-managed private datacenter networks can be stabler environments. Nevertheless, nobody is immune from network problems: for exam‐ ple, a problem during a software upgrade for a switch could trigger a network topol‐ ogy reconfiguration, during which network packets could be delayed for more than a minute [17]. Sharks might bite undersea cables and damage them [18]. Other surpris‐ ing faults include a network interface that sometimes drops all inbound packets but sends outbound packets successfully [19]: just because a network link works in one direction doesn’t guarantee it’s also working in the opposite direction.

Network partitions When one part of the network is cut off from the rest due to a net‐ work fault, that is sometimes called a network partition or netsplit. In this book we’ll generally stick with the more general term net‐ work fault, to avoid confusion with partitions (shards) of a storage system, as discussed in Chapter 6.

<!-- page 302 -->

Even if network faults are rare in your environment, the fact that faults can occur means that your software needs to be able to handle them. Whenever any communi‐ cation happens over a network, it may fail—there is no way around it.

If the error handling of network faults is not defined and tested, arbitrarily bad things could happen: for example, the cluster could become deadlocked and permanently unable to serve requests, even when the network recovers [20], or it could even delete all of your data [21]. If software is put in an unanticipated situation, it may do arbi‐ trary unexpected things.

