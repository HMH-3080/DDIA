[9] “XML Is a Poor Copy of S-Expressions,” c2.com wiki. [10] Matt Harris: “Snowflake: An Update and Some Very Important Information,” email to Twitter Development Talk mailing list, October 19, 2010. [11] Shudi (Sandy) Gao, C. M. Sperberg-McQueen, and Henry S. Thompson: “XML Schema 1.1,” W3C Recommendation, May 2001. [12] Francis Galiegue, Kris Zyp, and Gary Court: “JSON Schema,” IETF Internet- Draft, February 2013. [13] Yakov Shafranovich: “RFC 4180: Common Format and MIME Type for Comma-Separated Values (CSV) Files,” October 2005. [14] “MessagePack Specification,” msgpack.org. [15] Mark Slee, Aditya Agarwal, and Marc Kwiatkowski: “Thrift: Scalable Cross- Language Services Implementation,” Facebook technical report, April 2007. [16] “Protocol Buffers Developer Guide,” Google, Inc., developers.google.com. [17] Igor Anishchenko: “Thrift vs Protocol Buffers vs Avro - Biased Comparison,” slideshare.net, September 17, 2012. [18] “A Matrix of the Features Each Individual Language Library Supports,” wiki.apache.org. [19] Martin Kleppmann: “Schema Evolution in Avro, Protocol Buffers and Thrift,” martin.kleppmann.com, December 5, 2012. [20] “Apache Avro 1.7.7 Documentation,” avro.apache.org, July 2014. [21] Doug Cutting, Chad Walters, Jim Kellerman, et al.: “[PROPOSAL] New Subpro‐ ject: Avro,” email thread on hadoop-general mailing list, mail-archives.apache.org, April 2009. [22] Tony Hoare: “Null References: The Billion Dollar Mistake,” at QCon London, March 2009. [23] Aditya Auradkar and Tom Quiggle: “Introducing Espresso—LinkedIn’s Hot New Distributed Document Store,” engineering.linkedin.com, January 21, 2015. [24] Jay Kreps: “Putting Apache Kafka to Use: A Practical Guide to Building a Stream Data Platform (Part 2),” blog.confluent.io, February 25, 2015. [25] Gwen Shapira: “The Problem of Managing Schemas,” radar.oreilly.com, Novem‐ ber 4, 2014. [26] “Apache Pig 0.14.0 Documentation,” pig.apache.org, November 2014. [27] John Larmouth: ASN.1 Complete. Morgan Kaufmann, 1999. ISBN: 978-0-122-33435-1

<!-- page 164 -->

[28] Russell Housley, Warwick Ford, Tim Polk, and David Solo: “RFC 2459: Internet X.509 Public Key Infrastructure: Certificate and CRL Profile,” IETF Network Work‐ ing Group, Standards Track, January 1999. [29] Lev Walkin: “Question: Extensibility and Dropping Fields,” lionet.info, Septem‐ ber 21, 2010. [30] Jesse James Garrett: “Ajax: A New Approach to Web Applications,” adaptive‐ path.com, February 18, 2005. [31] Sam Newman: Building Microservices. O’Reilly Media, 2015. ISBN: 978-1-491-95035-7 [32] Chris Richardson: “Microservices: Decomposing Applications for Deployability and Scalability,” infoq.com, May 25, 2014. [33] Pat Helland: “Data on the Outside Versus Data on the Inside,” at 2nd Biennial Conference on Innovative Data Systems Research (CIDR), January 2005. [34] Roy Thomas Fielding: “Architectural Styles and the Design of Network-Based Software Architectures,” PhD Thesis, University of California, Irvine, 2000. [35] Roy Thomas Fielding: “REST APIs Must Be Hypertext-Driven,” roy.gbiv.com, October 20 2008. [36] “REST in Peace, SOAP,” royal.pingdom.com, October 15, 2010. [37] “Web Services Standards as of Q1 2007,” innoq.com, February 2007. [38] Pete Lacey: “The S Stands for Simple,” harmful.cat-v.org, November 15, 2006. [39] Stefan Tilkov: “Interview: Pete Lacey Criticizes Web Services,” infoq.com, December 12, 2006. [40] “OpenAPI Specification (fka Swagger RESTful API Documentation Specifica‐ tion) Version 2.0,” swagger.io, September 8, 2014. [41] Michi Henning: “The Rise and Fall of CORBA,” ACM Queue, volume 4, number 5, pages 28–34, June 2006. doi:10.1145/1142031.1142044 [42] Andrew D. Birrell and Bruce Jay Nelson: “Implementing Remote Procedure Calls,” ACM Transactions on Computer Systems (TOCS), volume 2, number 1, pages 39–59, February 1984. doi:10.1145/2080.357392 [43] Jim Waldo, Geoff Wyant, Ann Wollrath, and Sam Kendall: “A Note on Dis‐ tributed Computing,” Sun Microsystems Laboratories, Inc., Technical Report TR-94-29, November 1994. [44] Steve Vinoski: “Convenience over Correctness,” IEEE Internet Computing, vol‐ ume 12, number 4, pages 89–92, July 2008. doi:10.1109/MIC.2008.75

<!-- page 165 -->

[45] Marius Eriksen: “Your Server as a Function,” at 7th Workshop on Programming Languages and Operating Systems (PLOS), November 2013. doi: 10.1145/2525528.2525538 [46] “grpc-common Documentation,” Google, Inc., github.com, February 2015. [47] Aditya Narayan and Irina Singh: “Designing and Versioning Compatible Web Services,” ibm.com, March 28, 2007. [48] Troy Hunt: “Your API Versioning Is Wrong, Which Is Why I Decided to Do It 3 Different Wrong Ways,” troyhunt.com, February 10, 2014. [49] “API Upgrades,” Stripe, Inc., April 2015. [50] Jonas Bonér: “Upgrade in an Akka Cluster,” email to akka-user mailing list, grok‐ base.com, August 28, 2013. [51] Philip A. Bernstein, Sergey Bykov, Alan Geller, et al.: “Orleans: Distributed Vir‐ tual Actors for Programmability and Scalability,” Microsoft Research Technical Report MSR-TR-2014-41, March 2014. [52] “Microsoft Project Orleans Documentation,” Microsoft Research, dotnet.git‐ hub.io, 2015. [53] David Mercer, Sean Hinde, Yinso Chen, and Richard A O’Keefe: “beginner: Updating Data Structures,” email thread on erlang-questions mailing list, erlang.com, October 29, 2007. [54] Fred Hebert: “Postscript: Maps,” learnyousomeerlang.com, April 9, 2014.

<!-- page 166 -->

<!-- page 167 -->

## PART II Distributed Data

For a successful technology, reality must take precedence over public relations, for nature cannot be fooled.

—Richard Feynman, Rogers Commission Report (1986)

In Part I of this book, we discussed aspects of data systems that apply when data is stored on a single machine. Now, in Part II, we move up a level and ask: what hap‐ pens if multiple machines are involved in storage and retrieval of data?

There are various reasons why you might want to distribute a database across multi‐ ple machines:

## Scalability

If your data volume, read load, or write load grows bigger than a single machine can handle, you can potentially spread the load across multiple machines.

## Fault tolerance/high availability

If your application needs to continue working even if one machine (or several machines, or the network, or an entire datacenter) goes down, you can use multi‐ ple machines to give you redundancy. When one fails, another one can take over.

## Latency

If you have users around the world, you might want to have servers at various locations worldwide so that each user can be served from a datacenter that is geo‐ graphically close to them. That avoids the users having to wait for network pack‐ ets to travel halfway around the world.

<!-- page 168 -->

i. In a large machine, although any CPU can access any part of memory, some banks of memory are closer to one CPU than to others (this is called nonuniform memory access, or NUMA [1]). To make efficient use of this architecture, the processing needs to be broken down so that each CPU mostly accesses memory that is nearby—which means that partitioning is still required, even when ostensibly running on one machine.

ii. Network Attached Storage (NAS) or Storage Area Network (SAN).

## Scaling to Higher Load

