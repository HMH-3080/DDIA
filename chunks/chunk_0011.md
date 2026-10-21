If you want to add response time percentiles to the monitoring dashboards for your services, you need to efficiently calculate them on an ongoing basis. For example, you may want to keep a rolling window of response times of requests in the last 10 minutes. Every minute, you calculate the median and various percentiles over the val‐ ues in that window and plot those metrics on a graph.

The naïve implementation is to keep a list of response times for all requests within the time window and to sort that list every minute. If that is too inefficient for you, there are algorithms that can calculate a good approximation of percentiles at minimal CPU and memory cost, such as forward decay [25], t-digest [26], or HdrHistogram [27]. Beware that averaging percentiles, e.g., to reduce the time resolution or to com‐ bine data from several machines, is mathematically meaningless—the right way of aggregating response time data is to add the histograms [28].

<!-- page 39 -->

<table>
<tr><th>End-user request</th></tr>
<tr><td>92 ms</td></tr>
<tr><td>76 ms</td></tr>
<tr><td>103 ms</td></tr>
<tr><td>Q</td></tr>
<tr><td>143 ms</td></tr>
<tr><td>86 m</td></tr>
<tr><td>487 ms</td></tr>
</table>

<table>
<tr><th></th><th>Web application</th><th></th><th></th><th></th></tr>
<tr><td>103 ms</td><td>43 m</td><td></td><td>487 m</td><td>3 m</td></tr>
<tr><td>Backend 3</td><td>Backend 4</td><td>ackend 5</td><td>Backend 6</td><td>Backe</td></tr>
</table>

Figure 1-5. When several backend calls are needed to serve a request, it takes just a sin‐ gle slow backend request to slow down the entire end-user request.

## Approaches for Coping with Load

Now that we have discussed the parameters for describing load and metrics for meas‐ uring performance, we can start discussing scalability in earnest: how do we maintain good performance even when our load parameters increase by some amount?

An architecture that is appropriate for one level of load is unlikely to cope with 10 times that load. If you are working on a fast-growing service, it is therefore likely that you will need to rethink your architecture on every order of magnitude load increase —or perhaps even more often than that.

People often talk of a dichotomy between scaling up (vertical scaling, moving to a more powerful machine) and scaling out (horizontal scaling, distributing the load across multiple smaller machines). Distributing load across multiple machines is also known as a shared-nothing architecture. A system that can run on a single machine is often simpler, but high-end machines can become very expensive, so very intensive workloads often can’t avoid scaling out. In reality, good architectures usually involve a pragmatic mixture of approaches: for example, using several fairly powerful machines can still be simpler and cheaper than a large number of small virtual machines.

Some systems are elastic, meaning that they can automatically add computing resour‐ ces when they detect a load increase, whereas other systems are scaled manually (a human analyzes the capacity and decides to add more machines to the system). An elastic system can be useful if load is highly unpredictable, but manually scaled sys‐ tems are simpler and may have fewer operational surprises (see “Rebalancing Parti‐ tions” on page 209).

<!-- page 40 -->

While distributing stateless services across multiple machines is fairly straightfor‐ ward, taking stateful data systems from a single node to a distributed setup can intro‐ duce a lot of additional complexity. For this reason, common wisdom until recently was to keep your database on a single node (scale up) until scaling cost or highavailability requirements forced you to make it distributed.

As the tools and abstractions for distributed systems get better, this common wisdom may change, at least for some kinds of applications. It is conceivable that distributed data systems will become the default in the future, even for use cases that don’t han‐ dle large volumes of data or traffic. Over the course of the rest of this book we will cover many kinds of distributed data systems, and discuss how they fare not just in terms of scalability, but also ease of use and maintainability.

The architecture of systems that operate at large scale is usually highly specific to the application—there is no such thing as a generic, one-size-fits-all scalable architecture (informally known as magic scaling sauce). The problem may be the volume of reads, the volume of writes, the volume of data to store, the complexity of the data, the response time requirements, the access patterns, or (usually) some mixture of all of these plus many more issues.

For example, a system that is designed to handle 100,000 requests per second, each 1 kB in size, looks very different from a system that is designed for 3 requests per minute, each 2 GB in size—even though the two systems have the same data through‐ put.

An architecture that scales well for a particular application is built around assump‐ tions of which operations will be common and which will be rare—the load parame‐ ters. If those assumptions turn out to be wrong, the engineering effort for scaling is at best wasted, and at worst counterproductive. In an early-stage startup or an unpro‐ ven product it’s usually more important to be able to iterate quickly on product fea‐ tures than it is to scale to some hypothetical future load.

Even though they are specific to a particular application, scalable architectures are nevertheless usually built from general-purpose building blocks, arranged in familiar patterns. In this book we discuss those building blocks and patterns.

## Maintainability

It is well known that the majority of the cost of software is not in its initial develop‐ ment, but in its ongoing maintenance—fixing bugs, keeping its systems operational, investigating failures, adapting it to new platforms, modifying it for new use cases, repaying technical debt, and adding new features.

Yet, unfortunately, many people working on software systems dislike maintenance of so-called legacy systems—perhaps it involves fixing other people’s mistakes, or work‐

<!-- page 41 -->

ing with platforms that are now outdated, or systems that were forced to do things they were never intended for. Every legacy system is unpleasant in its own way, and so it is difficult to give general recommendations for dealing with them.

However, we can and should design software in such a way that it will hopefully min‐ imize pain during maintenance, and thus avoid creating legacy software ourselves. To this end, we will pay particular attention to three design principles for software systems:

## Operability

Make it easy for operations teams to keep the system running smoothly.

## Simplicity

Make it easy for new engineers to understand the system, by removing as much complexity as possible from the system. (Note this is not the same as simplicity of the user interface.)

## Evolvability

