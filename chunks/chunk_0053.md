Location transparency works better in the actor model than in RPC, because the actor model already assumes that messages may be lost, even within a single process. Although latency over the network is likely higher than within the same process, there is less of a fundamental mismatch between local and remote communication when using the actor model.

A distributed actor framework essentially integrates a message broker and the actor programming model into a single framework. However, if you want to perform roll‐ ing upgrades of your actor-based application, you still have to worry about forward and backward compatibility, as messages may be sent from a node running the new version to a node running the old version, and vice versa.

Three popular distributed actor frameworks handle message encoding as follows:

<!-- page 161 -->

• Akka uses Java’s built-in serialization by default, which does not provide forward or backward compatibility. However, you can replace it with something like Pro‐ tocol Buffers, and thus gain the ability to do rolling upgrades [50].
• Orleans by default uses a custom data encoding format that does not support rolling upgrade deployments; to deploy a new version of your application, you need to set up a new cluster, move traffic from the old cluster to the new one, and shut down the old one [51, 52]. Like with Akka, custom serialization plug-ins can be used.
• In Erlang OTP it is surprisingly hard to make changes to record schemas (despite the system having many features designed for high availability); rolling upgrades are possible but need to be planned carefully [53]. An experimental new maps datatype (a JSON-like structure, introduced in Erlang R17 in 2014) may make this easier in the future [54].

## Summary

In this chapter we looked at several ways of turning data structures into bytes on the network or bytes on disk. We saw how the details of these encodings affect not only their efficiency, but more importantly also the architecture of applications and your options for deploying them.

In particular, many services need to support rolling upgrades, where a new version of a service is gradually deployed to a few nodes at a time, rather than deploying to all nodes simultaneously. Rolling upgrades allow new versions of a service to be released without downtime (thus encouraging frequent small releases over rare big releases) and make deployments less risky (allowing faulty releases to be detected and rolled back before they affect a large number of users). These properties are hugely benefi‐ cial for evolvability, the ease of making changes to an application.

During rolling upgrades, or for various other reasons, we must assume that different nodes are running the different versions of our application’s code. Thus, it is impor‐ tant that all data flowing around the system is encoded in a way that provides back‐ ward compatibility (new code can read old data) and forward compatibility (old code can read new data).

We discussed several data encoding formats and their compatibility properties:

• Programming language–specific encodings are restricted to a single program‐ ming language and often fail to provide forward and backward compatibility.
• Textual formats like JSON, XML, and CSV are widespread, and their compatibil‐ ity depends on how you use them. They have optional schema languages, which are sometimes helpful and sometimes a hindrance. These formats are somewhat

<!-- page 162 -->

vague about datatypes, so you have to be careful with things like numbers and binary strings.

• Binary schema–driven formats like Thrift, Protocol Buffers, and Avro allow compact, efficient encoding with clearly defined forward and backward compati‐ bility semantics. The schemas can be useful for documentation and code genera‐ tion in statically typed languages. However, they have the downside that data needs to be decoded before it is human-readable.

We also discussed several modes of dataflow, illustrating different scenarios in which data encodings are important:

• Databases, where the process writing to the database encodes the data and the process reading from the database decodes it
• RPC and REST APIs, where the client encodes a request, the server decodes the request and encodes a response, and the client finally decodes the response
• Asynchronous message passing (using message brokers or actors), where nodes communicate by sending each other messages that are encoded by the sender and decoded by the recipient

We can conclude that with a bit of care, backward/forward compatibility and rolling upgrades are quite achievable. May your application’s evolution be rapid and your deployments be frequent.

## References

[1] “Java Object Serialization Specification,” docs.oracle.com, 2010. [2] “Ruby 2.2.0 API Documentation,” ruby-doc.org, Dec 2014. [3] “The Python 3.4.3 Standard Library Reference Manual,” docs.python.org, Febru‐ ary 2015. [4] “EsotericSoftware/kryo,” github.com, October 2014. [5] “CWE-502: Deserialization of Untrusted Data,” Common Weakness Enumera‐ tion, cwe.mitre.org, July 30, 2014. [6] Steve Breen: “What Do WebLogic, WebSphere, JBoss, Jenkins, OpenNMS, and Your Application Have in Common? This Vulnerability,” foxglovesecurity.com, November 6, 2015. [7] Patrick McKenzie: “What the Rails Security Issue Means for Your Startup,” kalzu‐ meus.com, January 31, 2013. [8] Eishay Smith: “jvm-serializers wiki,” github.com, November 2014.

<!-- page 163 -->

