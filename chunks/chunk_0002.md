Relational Versus Document Databases Today 38 Query Languages for Data 42 Declarative Queries on the Web 44 MapReduce Querying 46 Graph-Like Data Models 49 Property Graphs 50 The Cypher Query Language 52 Graph Queries in SQL 53 Triple-Stores and SPARQL 55 The Foundation: Datalog 60 Summary 63 3. Storage and Retrieval. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 69 Data Structures That Power Your Database 70 Hash Indexes 72 SSTables and LSM-Trees 76 B-Trees 79 Comparing B-Trees and LSM-Trees 83 Other Indexing Structures 85 Transaction Processing or Analytics? 90 Data Warehousing 91 Stars and Snowflakes: Schemas for Analytics 93 Column-Oriented Storage 95 97 Column Compression Sort Order in Column Storage 99 Writing to Column-Oriented Storage 101 Aggregation: Data Cubes and Materialized Views 101 Summary 103 4. Encoding and Evolution. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 111 Formats for Encoding Data 112 Language-Specific Formats 113 JSON, XML, and Binary Variants 114 Thrift and Protocol Buffers 117 Avro 122 The Merits of Schemas 127 Modes of Dataflow 128 Dataflow Through Databases 129 Dataflow Through Services: REST and RPC 131 Message-Passing Dataflow 136 Summary 139

<!-- page 11 -->

## Part II. Distributed Data

5. Replication. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 151 Leaders and Followers 152 Synchronous Versus Asynchronous Replication 153 155 Setting Up New Followers Handling Node Outages 156 Implementation of Replication Logs 158 Problems with Replication Lag 161 Reading Your Own Writes 162 Monotonic Reads 164 Consistent Prefix Reads 165 Solutions for Replication Lag 167 Multi-Leader Replication 168 Use Cases for Multi-Leader Replication 168 Handling Write Conflicts 171 Multi-Leader Replication Topologies 175 177 Leaderless Replication Writing to the Database When a Node Is Down 177 Limitations of Quorum Consistency 181 Sloppy Quorums and Hinted Handoff 183 Detecting Concurrent Writes 184 192 Summary 6. Partitioning. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 199 Partitioning and Replication 200 Partitioning of Key-Value Data 201 Partitioning by Key Range 202 Partitioning by Hash of Key 203 Skewed Workloads and Relieving Hot Spots 205 Partitioning and Secondary Indexes 206 Partitioning Secondary Indexes by Document 206 Partitioning Secondary Indexes by Term 208 209 Rebalancing Partitions Strategies for Rebalancing 210 Operations: Automatic or Manual Rebalancing 213 Request Routing 214 Parallel Query Execution 216 216 Summary 7. Transactions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 221 The Slippery Concept of a Transaction 222

<!-- page 12 -->

223 The Meaning of ACID Single-Object and Multi-Object Operations 228 Weak Isolation Levels 233 Read Committed 234 Snapshot Isolation and Repeatable Read 237 Preventing Lost Updates 242 Write Skew and Phantoms 246 Serializability 251 Actual Serial Execution 252 Two-Phase Locking (2PL) 257 Serializable Snapshot Isolation (SSI) 261 Summary 266 8. The Trouble with Distributed Systems. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 273 Faults and Partial Failures 274 Cloud Computing and Supercomputing 275 Unreliable Networks 277 Network Faults in Practice 279 Detecting Faults 280 Timeouts and Unbounded Delays 281 284 Synchronous Versus Asynchronous Networks Unreliable Clocks 287 Monotonic Versus Time-of-Day Clocks 288 Clock Synchronization and Accuracy 289 Relying on Synchronized Clocks 291 Process Pauses 295 Knowledge, Truth, and Lies 300 The Truth Is Defined by the Majority 300 304 Byzantine Faults System Model and Reality 306 Summary 310 9. Consistency and Consensus. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 321 Consistency Guarantees 322 Linearizability 324 What Makes a System Linearizable? 325 Relying on Linearizability 330 332 Implementing Linearizable Systems The Cost of Linearizability 335 Ordering Guarantees 339 Ordering and Causality 339 343 Sequence Number Ordering

<!-- page 13 -->

<table>
<tr><th>Total Order Broadcast</th><th>348</th></tr>
<tr><td>Distributed Transactions and Consensus</td><td>352</td></tr>
<tr><td>Atomic Commit and Two-Phase Commit (2PC)</td><td>354</td></tr>
<tr><td>Distributed Transactions in Practice</td><td>360</td></tr>
<tr><td>Fault-Tolerant Consensus</td><td>364</td></tr>
<tr><td>Membership and Coordination Services</td><td>370</td></tr>
<tr><td>Summary</td><td>373</td></tr>
</table>

## Part III. Derived Data

10. Batch Processing. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 389

<table>
<tr><th>Batch Processing with Unix Tools</th><th>391</th></tr>
<tr><td>Simple Log Analysis</td><td>391</td></tr>
<tr><td>The Unix Philosophy</td><td>394</td></tr>
<tr><td>MapReduce and Distributed Filesystems</td><td>397</td></tr>
<tr><td>MapReduce Job Execution</td><td>399</td></tr>
<tr><td>Reduce-Side Joins and Grouping</td><td>403</td></tr>
<tr><td>Map-Side Joins</td><td>408</td></tr>
<tr><td>The Output of Batch Workflows</td><td>411</td></tr>
<tr><td>Comparing Hadoop to Distributed Databases</td><td>414</td></tr>
<tr><td>Beyond MapReduce</td><td>419</td></tr>
<tr><td>Materialization of Intermediate State</td><td>419</td></tr>
<tr><td>Graphs and Iterative Processing</td><td>424</td></tr>
<tr><td>High-Level APIs and Languages</td><td>426</td></tr>
<tr><td>Summary</td><td>429</td></tr>
</table>

