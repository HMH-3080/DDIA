of distributed transactions, 362-364 transaction atomicity, 223, 354-361 faults, 6 Byzantine faults, 304-306 failures versus, 7 handled by transactions, 221 handling in supercomputers and cloud computing, 275 hardware, 7 in batch processing versus distributed data‐ bases, 417 in distributed systems, 274-277 introducing deliberately, 7, 280 network faults, 279-281 asymmetric faults, 300 detecting, 280 tolerance of, in multi-leader replication, 169 software errors, 8 tolerating (see fault tolerance) federated databases, 501 fence (CPU instruction), 338 fencing (preventing split brain), 158, 302-304 generating fencing tokens, 349, 370 properties of fencing tokens, 308 stream processors writing to databases, 478, 517 Fibre Channel (networks), 398 field tags (Thrift and Protocol Buffers), 119-121 file descriptors (Unix), 395 financial data, 460 Firebase (database), 456 Flink (processing framework), 421-423 dataflow APIs, 427 fault tolerance, 422, 477, 479 Gelly API (graph processing), 425 integration of batch and stream processing, 495, 498 machine learning, 428 query optimizer, 427 stream processing, 466 flow control, 282, 441, 555 FLP result (on consensus), 353 FlumeJava (dataflow library), 403, 427 followers, 152, 555 (see also leader-based replication) foreign keys, 38, 403 forward compatibility, 112 forward decay (algorithm), 16

<!-- page 592 -->

Fossil (version control system), 463 shunning (deleting data), 463 FoundationDB (database) serializable transactions, 261, 265, 364 fractal trees, 83 full table scans, 403 full-text search, 555 and fuzzy indexes, 88 building search indexes, 411 Lucene storage engine, 79 functional reactive programming (FRP), 504 functional requirements, 22 futures (asynchronous operations), 135 fuzzy search (see similarity search)

## G

garbage collection immutability and, 463 process pauses for, 14, 296-299, 301 (see also process pauses) genome analysis, 63, 429 geographically distributed datacenters, 145, 164, 278, 493 geospatial indexes, 87 Giraph (graph processing), 425 Git (version control system), 174, 342, 463 GitHub, postmortems, 157, 158, 309 global indexes (see term-partitioned indexes) GlusterFS (distributed filesystem), 398 GNU Coreutils (Linux), 394 GoldenGate (change data capture), 161, 170, 455 (see also Oracle) Google Bigtable (database) data model (see Bigtable data model) partitioning scheme, 199, 202 storage layout, 78 Chubby (lock service), 370 Cloud Dataflow (stream processor), 466, 477, 498 (see also Beam) Cloud Pub/Sub (messaging), 444, 448 Docs (collaborative editor), 170 Dremel (query engine), 93, 96 FlumeJava (dataflow library), 403, 427 GFS (distributed file system), 398 gRPC (RPC framework), 135 MapReduce (batch processing), 390

(see also MapReduce) building search indexes, 411 task preemption, 418 Pregel (graph processing), 425 Spanner (see Spanner) TrueTime (clock API), 294 gossip protocol, 216 government use of data, 541 GPS (Global Positioning System) use for clock synchronization, 287, 290, 294, 295 GraphChi (graph processing), 426 graphs, 555 as data models, 49-63 example of graph-structured data, 49 property graphs, 50 RDF and triple-stores, 55-59 versus the network model, 60 processing and analysis, 424-426 fault tolerance, 425 Pregel processing model, 425 query languages

Cypher, 52 Datalog, 60-63 recursive SQL queries, 53 SPARQL, 59-59

Gremlin (graph query language), 50 grep (Unix tool), 392

GROUP BY clause (SQL), 406

grouping records in MapReduce, 406 handling skew, 407

## H

Hadoop (data infrastructure) comparison to distributed databases, 390 comparison to MPP databases, 414-418 comparison to Unix, 413-414, 499 diverse processing models in ecosystem, 417 HDFS distributed filesystem (see HDFS) higher-level tools, 403 join algorithms, 403-410 (see also MapReduce) MapReduce (see MapReduce)

YARN (see YARN)

happens-before relationship, 340 capturing, 187 concurrency and, 186

hard disks

access patterns, 84

<!-- page 593 -->

detecting corruption, 519, 530 faults in, 7, 227 sequential write throughput, 75, 450 hardware faults, 7 hash indexes, 72-75 broadcast hash joins, 409 partitioned hash joins, 409 hash partitioning, 203-205, 217 consistent hashing, 204 problems with hash mod N, 210 range queries, 204 suitable hash functions, 203 with fixed number of partitions, 210 HAWQ (database), 428 HBase (database) bug due to lack of fencing, 302 bulk loading, 413 column-family data model, 41, 99 dynamic partitioning, 212 key-range partitioning, 202 log-structured storage, 78 request routing, 216 size-tiered compaction, 79 use of HDFS, 417 use of ZooKeeper, 370 HDFS (Hadoop Distributed File System), 398-399 (see also distributed filesystems) checking data integrity, 530 decoupling from query engines, 417 indiscriminately dumping data into, 415 metadata about datasets, 410 NameNode, 398 use by Flink, 479 use by HBase, 212 use by MapReduce, 402 HdrHistogram (numerical library), 16 head (Unix tool), 392 head vertex (property graphs), 51 head-of-line blocking, 15 heap files (databases), 86 Helix (cluster manager), 216 heterogeneous distributed transactions, 360, 364 heuristic decisions (in 2PC), 363 Hibernate (object-relational mapper), 30 hierarchical model, 36 high availability (see fault tolerance) high-frequency trading, 290, 299 high-performance computing (HPC), 275 hinted handoff, 183 histograms, 16 Hive (query engine), 419, 427 for data warehouses, 93 HCatalog and metastore, 410 map-side joins, 409 query optimizer, 427 skewed joins, 408 workflows, 403 Hollerith machines, 390 hopping windows (stream processing), 472 (see also windows) horizontal scaling (see scaling out) HornetQ (messaging), 137, 444 distributed transaction support, 361 hot spots, 201 due to celebrities, 205 for time-series data, 203 in batch processing, 407 relieving, 205 hot standbys (see leader-based replication) HTTP, use in APIs (see services) human errors, 9, 279, 414 HyperDex (database), 88 HyperLogLog (algorithm), 466 I/O operations, waiting for, 297 IBM DB2 (database) distributed transaction support, 361 recursive query support, 54 serializable isolation, 242, 257 XML and JSON support, 30, 42 electromechanical card-sorting machines, 390 IMS (database), 36 imperative query APIs, 46 InfoSphere Streams (CEP engine), 466 MQ (messaging), 444 distributed transaction support, 361 System R (database), 222 WebSphere (messaging), 137 idempotence, 134, 478, 555 by giving operations unique IDs, 518, 522 idempotent operations, 517 immutability advantages of, 460, 531

<!-- page 594 -->

