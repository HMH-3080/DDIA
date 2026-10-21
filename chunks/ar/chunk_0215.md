لـtransactions الموزّعة, 362-364 transaction atomicity, 223, 354-361 أعطال, 6 أعطال Byzantine, 304-306 failures في المقابل, 7 معالجتها بواسطة transactions, 221 معالجتها في الحواسيب الخارقة والحوسبة السحابية, 275 hardware, 7 في batch processing مقابل distributed database, 417 في الأنظمة الموزّعة, 274-277 استحداثها المتعمَّد, 7, 280 أعطال الشبكة, 279-281 أعطال غير متناظرة, 300 اكتشافها, 280 تحمّلها في multi-leader replication, 169 أخطاء البرمجيات, 8 تحمُّلها (انظر fault tolerance) federated database, 501 fence (تعليمة CPU), 338 fencing (منع split brain), 158, 302-304 توليد fencing tokens, 349, 370 خصائص fencing tokens, 308 معالجات stream التي تكتب إلى databases, 478, 517 Fibre Channel (شبكات), 398 field tags (Thrift وProtocol Buffers), 119-121 file descriptors (Unix), 395 البيانات المالية, 460 Firebase (قاعدة بيانات), 456 Flink (إطار معالجة), 421-423 dataflow APIs, 427 fault tolerance, 422, 477, 479 Gelly API (معالجة الرسوم البيانية), 425 تكامل batch processing وstream processing, 495, 498 machine learning, 428 query optimizer, 427 stream processing, 466 flow control, 282, 441, 555 نتيجة FLP (بشأن consensus), 353 FlumeJava (مكتبة dataflow), 403, 427 followers, 152, 555 (انظر أيضًا leader-based replication) foreign keys, 38, 403 forward compatibility, 112 forward decay (خوارزمية), 16

<!-- page 592 -->

Fossil (نظام version control), 463 shunning (حذف البيانات), 463 FoundationDB (قاعدة بيانات) serializable transactions, 261, 265, 364 fractal trees, 83 full table scans, 403 full-text search, 555 وfuzzy indexes, 88 building search indexes, 411 Lucene storage engine, 79 functional reactive programming (FRP), 504 المتطلبات الوظيفية, 22 futures (عمليات غير متزامنة), 135 fuzzy search (انظر similarity search)

## G

garbage collection immutability و, 463 process pauses لـ, 14, 296-299, 301 (انظر أيضًا process pauses) تحليل الجينوم, 63, 429 datacenters الموزّعة جغرافيًا, 145, 164, 278, 493 geospatial indexes, 87 Giraph (معالجة الرسوم البيانية), 425 Git (نظام version control), 174, 342, 463 GitHub, postmortems, 157, 158, 309 global indexes (انظر term-partitioned indexes) GlusterFS (نظام ملفات موزّع), 398 GNU Coreutils (Linux), 394 GoldenGate (التقاط تغيّر البيانات), 161, 170, 455 (انظر أيضًا Oracle) Google Bigtable (قاعدة بيانات) data model (انظر Bigtable data model) partitioning scheme, 199, 202 storage layout, 78 Chubby (خدمة قفل), 370 Cloud Dataflow (معالج stream), 466, 477, 498 (انظر أيضًا Beam) Cloud Pub/Sub (messaging), 444, 448 Docs (محرّر تعاوني), 170 Dremel (محرّك استعلامات), 93, 96 FlumeJava (مكتبة dataflow), 403, 427 GFS (نظام ملفات موزّع), 398 gRPC (إطار RPC), 135 MapReduce (batch processing), 390

(انظر أيضًا MapReduce) building search indexes, 411 task preemption, 418 Pregel (معالجة الرسوم البيانية), 425 Spanner (انظر Spanner) TrueTime (واجهة برمجة الساعة), 294 gossip protocol, 216 استخدام البيانات في القطاع الحكومي, 541 GPS (Global Positioning System) استخدامه في مزامنة الساعات, 287, 290, 294, 295 GraphChi (معالجة الرسوم البيانية), 426 graphs, 555 كنماذج بيانات, 49-63 مثال على بيانات ذات بنية بيانية, 49 property graphs, 50 RDF وtriple-stores, 55-59 مقابل نموذج الشبكة, 60 المعالجة والتحليل, 424-426 fault tolerance, 425 Pregel processing model, 425 query languages

Cypher, 52 Datalog, 60-63 recursive SQL queries, 53 SPARQL, 59-59

Gremlin (لغة استعلام الرسوم البيانية), 50 grep (أداة Unix), 392

GROUP BY clause (SQL), 406

تجميع السجلات في MapReduce, 406 معالجة skew, 407

## H

Hadoop (بنية تحتية للبيانات) مقارنته مع distributed database, 390 مقارنته مع MPP database, 414-418 مقارنته مع Unix, 413-414, 499 نماذج معالجة متنوّعة في النظام البيئي, 417 HDFS نظام الملفات الموزّع (انظر HDFS) higher-level tools, 403 خوارزميات join, 403-410 (انظر أيضًا MapReduce) MapReduce (انظر MapReduce)

YARN (انظر YARN)

happens-before relationship, 340 capturing, 187 concurrency و, 186

hard disks

access patterns, 84

<!-- page 593 -->

اكتشاف التلف, 519, 530 الأعطال فيها, 7, 227 sequential write throughput, 75, 450 hardware faults, 7 hash indexes, 72-75 broadcast hash joins, 409 partitioned hash joins, 409 hash partitioning, 203-205, 217 consistent hashing, 204 مشكلات hash mod N, 210 range queries, 204 دوال hash مناسبة, 203 مع عدد ثابت من التقسيمات, 210 HAWQ (قاعدة بيانات), 428 HBase (قاعدة بيانات) خلل بسبب غياب fencing, 302 bulk loading, 413 column-family data model, 41, 99 dynamic partitioning, 212 key-range partitioning, 202 log-structured storage, 78 request routing, 216 size-tiered compaction, 79 استخدام HDFS, 417 استخدام ZooKeeper, 370 HDFS (Hadoop Distributed File System), 398-399 (انظر أيضًا distributed filesystems) فحص سلامة البيانات, 530 فصلها عن محرّكات الاستعلامات, 417 صبّ البيانات فيها بلا تمييز, 415 metadata عن datasets, 410 NameNode, 398 استخدام Flink لها, 479 استخدام HBase لها, 212 استخدام MapReduce لها, 402 HdrHistogram (مكتبة رقمية), 16 head (أداة Unix), 392 head vertex (property graphs), 51 head-of-line blocking, 15 heap files (قواعد بيانات), 86 Helix (مدير العنقود), 216 heterogeneous distributed transactions, 360, 364 heuristic decisions (في 2PC), 363 Hibernate (object-relational mapper), 30 hierarchical model, 36 high availability (انظر fault tolerance) high-frequency trading, 290, 299 high-performance computing (HPC), 275 hinted handoff, 183 histograms, 16 Hive (محرّك استعلامات), 419, 427 لمستودعات data warehouse, 93 HCatalog وmetastore, 410 map-side joins, 409 query optimizer, 427 skewed joins, 408 workflows, 403 آلات Hollerith, 390 hopping windows (stream processing), 472 (انظر أيضًا windows) horizontal scaling (انظر scaling out) HornetQ (messaging), 137, 444 دعم distributed transactions, 361 hot spots, 201 بسبب المشاهير, 205 لبيانات time-series, 203 في batch processing, 407 تخفيفها, 205 hot standbys (انظر leader-based replication) HTTP, استخدامه في APIs (انظر services) أخطاء بشرية, 9, 279, 414 HyperDex (قاعدة بيانات), 88 HyperLogLog (خوارزمية), 466 عمليات I/O, انتظارها, 297 IBM DB2 (قاعدة بيانات) دعم distributed transactions, 361 دعم الاستعلامات التكرارية, 54 serializable isolation, 242, 257 دعم XML وJSON, 30, 42 آلات الفرز الكهروميكانيكية للبطاقات, 390 IMS (قاعدة بيانات), 36 imperative query APIs, 46 InfoSphere Streams (محرّك CEP), 466 MQ (messaging), 444 دعم distributed transactions, 361 System R (قاعدة بيانات), 222 WebSphere (messaging), 137 idempotence, 134, 478, 555 بمنح العمليات مُعرّفات فريدة, 518, 522 idempotent operations, 517 مزايا immutability, 460, 531

<!-- page 594 -->

