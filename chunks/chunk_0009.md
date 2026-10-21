To make this idea more concrete, let’s consider Twitter as an example, using data published in November 2012 [16]. Two of Twitter’s main operations are:

## Post tweet

A user can publish a new message to their followers (4.6k requests/sec on aver‐ age, over 12k requests/sec at peak).

## Home timeline

A user can view tweets posted by the people they follow (300k requests/sec).

Simply handling 12,000 writes per second (the peak rate for posting tweets) would be fairly easy. However, Twitter’s scaling challenge is not primarily due to tweet volume, but due to fan-outii—each user follows many people, and each user is followed by many people. There are broadly two ways of implementing these two operations:

1. Posting a tweet simply inserts the new tweet into a global collection of tweets. When a user requests their home timeline, look up all the people they follow, find all the tweets for each of those users, and merge them (sorted by time). In a relational database like in Figure 1-2, you could write a query such as:

SELECT tweets.*, users.* FROM tweets JOIN users ON tweets.sender_id = users.id JOIN follows ON follows.followee_id = users.id WHERE follows.follower_id = current_user

<!-- page 34 -->

2. Maintain a cache for each user’s home timeline—like a mailbox of tweets for each recipient user (see Figure 1-3). When a user posts a tweet, look up all the people who follow that user, and insert the new tweet into each of their home timeline caches. The request to read the home timeline is then cheap, because its result has been computed ahead of time.

<table>
<tr><th>Q currently logged-in</th><th></th><th>tweets table</th><th></th><th></th><th></th></tr>
<tr><td>user: 17055506</td><td></td><td>id</td><td>sender_id</td><td>text</td><td>timestamp</td></tr>
<tr><td>follower_id</td><td>followee_id</td><td>20</td><td>12</td><td>just setting up my twttr</td><td>1142974214</td></tr>
<tr><td>► 17055506</td><td>12.</td><td></td><td></td><td></td><td></td></tr>
<tr><td>follows table</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>/ users table</td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>id screen_name</td><td></td><td>profile_image</td><td></td><td></td></tr>
<tr><td></td><td>*12 jack</td><td></td><td>1234567.jpg</td><td></td><td></td></tr>
</table>

Figure 1-2. Simple relational schema for implementing a Twitter home timeline.

<table>
<tr><th></th><th>Fan-out: deliver tweet to</th><th>Get home timeline</th></tr>
<tr><td></td><td>s for</td><td>ent</td></tr>
<tr><td></td><td>each follower (up to 31M</td><td>(website, API)</td></tr>
<tr><td>followers per user)</td><td></td><td></td></tr>
<tr><td>User posts tweet</td><td></td><td></td></tr>
<tr><td>All tw</td><td>ets for recipient 2</td><td></td></tr>
<tr><td>Q</td><td></td><td></td></tr>
<tr><td>T T7</td><td></td><td></td></tr>
<tr><td>八</td><td></td><td></td></tr>
<tr><td>4.6k writes/sec</td><td>345k writes/se</td><td>300k reads/sec</td></tr>
</table>

Figure 1-3. Twitter’s data pipeline for delivering tweets to followers, with load parame‐ ters as of November 2012 [16].

The first version of Twitter used approach 1, but the systems struggled to keep up with the load of home timeline queries, so the company switched to approach 2. This works better because the average rate of published tweets is almost two orders of magnitude lower than the rate of home timeline reads, and so in this case it’s prefera‐ ble to do more work at write time and less at read time.

However, the downside of approach 2 is that posting a tweet now requires a lot of extra work. On average, a tweet is delivered to about 75 followers, so 4.6k tweets per second become 345k writes per second to the home timeline caches. But this average hides the fact that the number of followers per user varies wildly, and some users

<!-- page 35 -->

iii. In an ideal world, the running time of a batch job is the size of the dataset divided by the throughput. In practice, the running time is often longer, due to skew (data not being spread evenly across worker processes) and needing to wait for the slowest task to complete.

have over 30 million followers. This means that a single tweet may result in over 30 million writes to home timelines! Doing this in a timely manner—Twitter tries to deliver tweets to followers within five seconds—is a significant challenge.

In the example of Twitter, the distribution of followers per user (maybe weighted by how often those users tweet) is a key load parameter for discussing scalability, since it determines the fan-out load. Your application may have very different characteristics, but you can apply similar principles to reasoning about its load.

The final twist of the Twitter anecdote: now that approach 2 is robustly implemented, Twitter is moving to a hybrid of both approaches. Most users’ tweets continue to be fanned out to home timelines at the time when they are posted, but a small number of users with a very large number of followers (i.e., celebrities) are excepted from this fan-out. Tweets from any celebrities that a user may follow are fetched separately and merged with that user’s home timeline when it is read, like in approach 1. This hybrid approach is able to deliver consistently good performance. We will revisit this exam‐ ple in Chapter 12 after we have covered some more technical ground.

## Describing Performance

Once you have described the load on your system, you can investigate what happens when the load increases. You can look at it in two ways:

• When you increase a load parameter and keep the system resources (CPU, mem‐ ory, network bandwidth, etc.) unchanged, how is the performance of your system affected?
• When you increase a load parameter, how much do you need to increase the resources if you want to keep performance unchanged?

Both questions require performance numbers, so let’s look briefly at describing the performance of a system.

In a batch processing system such as Hadoop, we usually care about throughput—the number of records we can process per second, or the total time it takes to run a job on a dataset of a certain size.iii In online systems, what’s usually more important is the service’s response time—that is, the time between a client sending a request and receiving a response.

<!-- page 36 -->

## Latency and response time

Latency and response time are often used synonymously, but they are not the same. The response time is what the client sees: besides the actual time to process the request (the service time), it includes network delays and queueing delays. Latency is the duration that a request is waiting to be handled—during which it is latent, await‐ ing service [17].

Even if you only make the same request over and over again, you’ll get a slightly dif‐ ferent response time on every try. In practice, in a system handling a variety of requests, the response time can vary a lot. We therefore need to think of response time not as a single number, but as a distribution of values that you can measure.

