graph databases versus, 60 imperative query APIs, 46 Network Time Protocol (see NTP) networks congestion and queueing, 282 datacenter network topologies, 276 faults (see faults) linearizability and network delays, 338 network partitions, 279, 337 timeouts and unbounded delays, 281 next-key locking, 260 nodes (in graphs) (see vertices) nodes (processes), 556 handling outages in leader-based replica‐ tion, 156 system models for failure, 307 noisy neighbors, 284 nonblocking atomic commit, 359 nondeterministic operations accidental nondeterminism, 423 partial failures in distributed systems, 275 nonfunctional requirements, 22 nonrepeatable reads, 238 (see also read skew) normalization (data representation), 33, 556 executing joins, 39, 42, 403 foreign key references, 231 in systems of record, 386 versus denormalization, 462 NoSQL, 29, 499 transactions and, 223 Notation3 (N3), 56 npm (package manager), 428 NTP (Network Time Protocol), 287 accuracy, 289, 293 adjustments to monotonic clocks, 289 multiple server addresses, 306 numbers, in XML and JSON encodings, 114 O

object-relational mapping (ORM) frameworks, 30 error handling and aborted transactions, 232 unsafe read-modify-write cycle code, 244 object-relational mismatch, 29 observer pattern, 506 offline systems, 390 (see also batch processing)

stateful, offline-capable clients, 170, 511 offline-first applications, 511 offsets consumer offsets in partitioned logs, 449 messages in partitioned logs, 447 OLAP (online analytic processing), 91, 556 data cubes, 102 OLTP (online transaction processing), 90, 556 analytics queries versus, 411 workload characteristics, 253 one-to-many relationships, 30 JSON representation, 32 online systems, 389 (see also services) Oozie (workflow scheduler), 402 OpenAPI (service definition format), 133 OpenStack Nova (cloud infrastructure) use of ZooKeeper, 370 Swift (object storage), 398 operability, 19 operating systems versus databases, 499 operation identifiers, 518, 522 operational transformation, 174 operators, 421 flow of data between, 424 in stream processing, 464 optimistic concurrency control, 261 Oracle (database) distributed transaction support, 361 GoldenGate (change data capture), 161, 170, 455 lack of serializability, 226 leader-based replication, 153 multi-table index cluster tables, 41 not preventing write skew, 248 partitioned indexes, 209 PL/SQL language, 255 preventing lost updates, 245 read committed isolation, 236 Real Application Clusters (RAC), 330 recursive query support, 54 snapshot isolation support, 239, 242 TimesTen (in-memory database), 89 WAL-based replication, 160 XML support, 30 ordering, 339-352 by sequence numbers, 343-348 causal ordering, 339-343

<!-- page 601 -->

partial order, 341 limits of total ordering, 493 total order broadcast, 348-352 Orleans (actor framework), 139 outliers (response time), 14 Oz (programming language), 504

P package managers, 428, 505 packet switching, 285 packets corruption of, 306 sending via UDP, 442 PageRank (algorithm), 49, 424 paging (see virtual memory) ParAccel (database), 93 parallel databases (see massively parallel pro‐ cessing) parallel execution of graph analysis algorithms, 426 queries in MPP databases, 216 Parquet (data format), 96, 131 (see also column-oriented storage) use in Hadoop, 414 partial failures, 275, 310 limping, 311 partial order, 341 partitioning, 199-218, 556 and replication, 200 in batch processing, 429 multi-partition operations, 514 enforcing constraints, 522 secondary index maintenance, 495 of key-value data, 201-205 by key range, 202 skew and hot spots, 205 rebalancing partitions, 209-214 automatic or manual rebalancing, 213 problems with hash mod N, 210 using dynamic partitioning, 212 using fixed number of partitions, 210 using N partitions per node, 212 replication and, 147 request routing, 214-216 secondary indexes, 206-209 document-based partitioning, 206 term-based partitioning, 208 serial execution of transactions and, 255

Paxos (consensus algorithm), 366

ballot number, 368 Multi-Paxos (total order broadcast), 367 percentiles, 14, 556 calculating efficiently, 16 importance of high percentiles, 16 use in service level agreements (SLAs), 15 Percona XtraBackup (MySQL tool), 156

## performance

describing, 13 of distributed transactions, 360 of in-memory databases, 89 of linearizability, 338 of multi-leader replication, 169 perpetual inconsistency, 525 pessimistic concurrency control, 261 phantoms (transaction isolation), 250 materializing conflicts, 251 preventing, in serializability, 259 physical clocks (see clocks) pickle (Python), 113

Pig (dataflow language), 419, 427 replicated joins, 409 skewed joins, 407 workflows, 403

Pinball (workflow scheduler), 402

pipelined execution, 423 in Unix, 394

point in time, 287

polyglot persistence, 29

polystores, 501

PostgreSQL (database)

BDR (multi-leader replication), 170 causal ordering of writes, 177 Bottled Water (change data capture), 455 Bucardo (trigger-based replication), 161, 173 distributed transaction support, 361 foreign data wrappers, 501 full text search support, 490 leader-based replication, 153 log sequence number, 156 MVCC implementation, 239, 241 PL/pgSQL language, 255 PostGIS geospatial indexes, 87 preventing lost updates, 245 preventing write skew, 248, 261 read committed isolation, 236 recursive query support, 54 representing graphs, 51

<!-- page 602 -->

serializable snapshot isolation (SSI), 261 snapshot isolation support, 239, 242 WAL-based replication, 160 XML and JSON support, 30, 42 pre-splitting, 212 Precision Time Protocol (PTP), 290 predicate locks, 259 predictive analytics, 533-536 amplifying bias, 534 ethics of (see ethics) feedback loops, 536 preemption of datacenter resources, 418 of threads, 298 Pregel processing model, 425 primary keys, 85, 556 compound primary key (Cassandra), 204 primary-secondary replication (see leaderbased replication) privacy, 536-543 consent and freedom of choice, 538 data as assets and power, 540 deleting data, 463 ethical considerations (see ethics) legislation and self-regulation, 542 meaning of, 539 surveillance, 537 tracking behavioral data, 536 probabilistic algorithms, 16, 466 process pauses, 295-299 processing time (of events), 469 producers (message streams), 440 programming languages dataflow languages, 504 for stored procedures, 255 functional reactive programming (FRP), 504

logic programming, 504 Prolog (language), 61 (see also Datalog) promises (asynchronous operations), 135 property graphs, 50 Cypher query language, 52 Protocol Buffers (data format), 117-121 field tags and schema evolution, 120 provenance of data, 531 publish/subscribe model, 441 publishers (message streams), 440 punch card tabulating machines, 390

pure functions, 48 putting computation near data, 400

## Q

Qpid (messaging), 444 quality of service (QoS), 285 Quantcast File System (distributed filesystem), 398 query languages, 42-48 aggregation pipeline, 48 CSS and XSL, 44 Cypher, 52 Datalog, 60 Juttle, 504 MapReduce querying, 46-48 recursive SQL queries, 53 relational algebra and SQL, 42 SPARQL, 59 query optimizers, 37, 427 queueing delays (networks), 282 head-of-line blocking, 15 latency and response time, 14 queues (messaging), 137 quorums, 179-182, 556 for leaderless replication, 179 in consensus algorithms, 368 limitations of consistency, 181-183, 334 making decisions in distributed systems, 301 monitoring staleness, 182 multi-datacenter replication, 184 relying on durability, 309 sloppy quorums and hinted handoff, 183

## R

R-trees (indexes), 87

RabbitMQ (messaging), 137, 444 leader-based replication, 153 race conditions, 225 (see also concurrency) avoiding with linearizability, 331 caused by dual writes, 452 dirty writes, 235 in counter increments, 235 lost updates, 242-246 preventing with event logs, 462, 507 preventing with serializable isolation, 252 write skew, 246-251

Raft (consensus algorithm), 366

<!-- page 603 -->

