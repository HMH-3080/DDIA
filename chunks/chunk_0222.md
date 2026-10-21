uncertain (transaction status) (see in doubt) uniform consensus, 365 (see also consensus) uniform interfaces, 395 union type (in Avro), 125 uniq (Unix tool), 392 uniqueness constraints asynchronously checked, 526 requiring consensus, 521 requiring linearizability, 330 uniqueness in log-based messaging, 522 Unix philosophy, 394-397 command-line batch processing, 391-394 Unix pipes versus dataflow engines, 423 comparison to Hadoop, 413-414 comparison to relational databases, 499, 501 comparison to stream processing, 464 composability and uniform interfaces, 395 loose coupling, 396 pipes, 394 relation to Hadoop, 499 UPDATE statement (SQL), 40 updates preventing lost updates, 242-246 atomic write operations, 243 automatically detecting lost updates, 245 compare-and-set operations, 245 conflict resolution and replication, 246 using explicit locking, 244 preventing write skew, 246-251

V validity (consensus), 365 vBuckets (partitioning), 199 vector clocks, 191 (see also version vectors) vectorized processing, 99, 428 verification, 528-533 avoiding blind trust, 530 culture of, 530 designing for auditability, 531 end-to-end integrity checks, 531 tools for auditable data systems, 532 version control systems, reliance on immutable data, 463 version vectors, 177, 191 capturing causal dependencies, 343 versus vector clocks, 191 Vertica (database), 93

handling writes, 101 replicas using different sort orders, 100 vertical scaling (see scaling up) vertices (in graphs), 49 property graph model, 50 Viewstamped Replication (consensus algo‐ rithm), 366 view number, 368 virtual machines, 146 (see also cloud computing) context switches, 297 network performance, 282 noisy neighbors, 284 reliability in cloud services, 8 virtualized clocks in, 290 virtual memory process pauses due to page faults, 14, 297 versus memory management by databases, 89 VisiCalc (spreadsheets), 504 vnodes (partitioning), 199 Voice over IP (VoIP), 283

## Voldemort (database)

building read-only stores in batch processes, 413 hash partitioning, 203-204, 211 leaderless replication, 177 multi-datacenter support, 184 rebalancing, 213 reliance on read repair, 179 sloppy quorums, 184

## VoltDB (database)

cross-partition serializability, 256 deterministic stored procedures, 255 in-memory storage, 89

output streams, 456

secondary indexes, 207

serial execution of transactions, 253 statement-based replication, 159, 479 transactions in stream processing, 477

W

WAL (write-ahead log), 82

web services (see services) Web Services Description Language (WSDL), 133

webhooks, 443

webMethods (messaging), 137

WebSocket (protocol), 512

<!-- page 612 -->

windows (stream processing), 466, 468-472 infinite windows for changelogs, 467, 474 knowing when all events have arrived, 470 stream joins within a window, 473 types of windows, 472 winners (conflict resolution), 173 WITH RECURSIVE syntax (SQL), 54 workflows (MapReduce), 402 outputs, 411-414 key-value stores, 412 search indexes, 411 with map-side joins, 410 working set, 393 write amplification, 84 write path (derived data), 509 write skew (transaction isolation), 246-251 characterizing, 246-251, 262 examples of, 247, 249 materializing conflicts, 251 occurrence in practice, 529 phantoms, 250 preventing in snapshot isolation, 262-265 in two-phase locking, 259-261 options for, 248 write-ahead log (WAL), 82, 159 writes (database) atomic write operations, 243 detecting writes affecting prior reads, 264 preventing dirty writes with read commit‐ ted, 235 WS-* framework, 133 (see also services) WS-AtomicTransaction (2PC), 355

## X

XA transactions, 355, 361-364 heuristic decisions, 363 limitations of, 363 xargs (Unix tool), 392, 396

## XML

binary variants, 115 encoding RDF data, 57 for application data, issues with, 114 in relational databases, 30, 41

XSL/XPath, 45

## Y

## Yahoo!

Pistachio (database), 461

Sherpa (database), 455

YARN (job scheduler), 416, 506 preemption of jobs, 418 use of ZooKeeper, 370

## Z

Zab (consensus algorithm), 366 use in ZooKeeper, 353 ZeroMQ (messaging library), 442 ZooKeeper (coordination service), 370-373 generating fencing tokens, 303, 349, 370 linearizable operations, 333, 351 locks and leader election, 330 service discovery, 372 use for partition assignment, 215, 371 use of Zab algorithm, 349, 353, 366

<!-- page 613 -->

## About the Author

Martin Kleppmann is a researcher in distributed systems at the University of Cam‐ bridge, UK. Previously he was a software engineer and entrepreneur at internet com‐ panies including LinkedIn and Rapportive, where he worked on large-scale data infrastructure. In the process he learned a few things the hard way, and he hopes this book will save you from repeating the same mistakes.

Martin is a regular conference speaker, blogger, and open source contributor. He believes that profound technical ideas should be accessible to everyone, and that deeper understanding will help us develop better software.

## Colophon

The animal on the cover of Designing Data-Intensive Applications is an Indian wild boar (Sus scrofa cristatus), a subspecies of wild boar found in India, Myanmar, Nepal, Sri Lanka, and Thailand. They are distinctive from European boars in that they have higher back bristles, no woolly undercoat, and a larger, straighter skull.

The Indian wild boar has a coat of gray or black hair, with stiff bristles running along the spine. Males have protruding canine teeth (called tushes) that are used to fight with rivals or fend off predators. Males are larger than females, but the species aver‐ ages 33–35 inches tall at the shoulder and 200–300 pounds in weight. Their natural predators include bears, tigers, and various big cats.

These animals are nocturnal and omnivorous—they eat a wide variety of things, including roots, insects, carrion, nuts, berries, and small animals. Wild boars are also known to root through garbage and crop fields, causing a great deal of destruction and earning the enmity of farmers. They need to eat 4,000–4,500 calories a day. Boars have a well-developed sense of smell, which helps them forage for underground plant material and burrowing animals. However, their eyesight is poor.

Wild boars have long held significance in human culture. In Hindu lore, the boar is an avatar of the god Vishnu. In ancient Greek funerary monuments, it was a symbol of a gallant loser (in contrast to the victorious lion). Due to its aggression, it was depicted on the armor and weapons of Scandinavian, Germanic, and Anglo-Saxon warriors. In the Chinese zodiac, it symbolizes determination and impetuosity.

Many of the animals on O’Reilly covers are endangered; all of them are important to the world. To learn more about how you can help, go to animals.oreilly.com.

The cover image is from Shaw’s Zoology. The cover fonts are URW Typewriter and Guardian Sans. The text font is Adobe Minion Pro; the font in diagrams is Adobe Myriad Pro; the heading font is Adobe Myriad Condensed; and the code font is Dal‐ ton Maag’s Ubuntu Mono.

