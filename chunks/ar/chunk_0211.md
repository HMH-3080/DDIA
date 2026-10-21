خوارزمية تحقق عزلًا قابلًا للتسلسل (serializable isolation) تعمل بأن تكتسب المعاملة (transaction) قفلًا على كل البيانات التي تقرأها أو تكتبها، وتُبقي القفل محفوظًا حتى نهاية المعاملة. انظر «Two-Phase Locking (2PL)» في الصفحة 257.

## غير محدود (unbounded)

لا يوجد له حدّ أعلى أو حجم معروف.

العكس من bounded.

<!-- page 581 -->

## A

aborts (transactions), 222, 224 في two-phase commit, 356 أداء optimistic concurrency control, 266 إعادة محاولة المعاملات المُجهَضة, 231 abstraction, 21, 27, 222, 266, 321 مسار الوصول (في network model), 37, 60 إزالة التعقيد العرضي, 21 المساءلة, 535 ACID properties (transactions), 90, 223 atomicity, 223, 228 consistency, 224, 529 durability, 226 isolation, 225, 228 acknowledgements (messaging), 445 active/active replication (انظر multi-leader replication) active/passive replication (انظر leader-based replication) ActiveMQ (messaging), 137, 444 دعم المعاملات الموزّعة, 361 ActiveRecord (object-relational mapper), 30, 232 actor model, 138 (انظر أيضًا message-passing) المقارنة مع نموذج Pregel, 425 المقارنة مع stream processing, 468 Advanced Message Queuing Protocol (انظر AMQP) أنظمة الطيران والفضاء, 6, 10, 305, 372 aggregation data cubes وmaterialized views, 101 في batch processes, 406

في stream processes, 466 aggregation pipeline query language, 48 Agile, 22 تقليل ما لا يمكن التراجع عنه, 414, 497 التحرك بسرعة مع الثقة, 532 فلسفة Unix, 394 agreement, 365 (انظر أيضًا consensus) Airflow (workflow scheduler), 402 Ajax, 131 Akka (actor framework), 139 algorithms صحة الخوارزمية, 308 B-trees, 79-83 للأنظمة الموزّعة, 306 hash indexes, 72-75 mergesort, 76, 402, 405 red-black trees, 78 SSTables وLSM-trees, 76-79 all-to-all replication topologies, 175 AllegroGraph (database), 50 ALTER TABLE statement (SQL), 40, 111 Amazon Dynamo (database), 177 Amazon Web Services (AWS), 8 Kinesis Streams (messaging), 448 موثوقية الشبكة, 279 postmortems, 9 RedShift (database), 93 S3 (object storage), 398 التحقق من سلامة البيانات, 530 amplification للـbias, 534 للأعطال, 364, 495

<!-- page 582 -->

<table>
<tr><th>لـtail latency, 16, 207</th><th>Apache Storm (انظر Storm)</th></tr>
<tr><td>write amplification, 84</td><td>Apache Tajo (انظر Tajo)</td></tr>
<tr><td>AMQP (Advanced Message Queuing Protocol),</td><td>Apache Tez (انظر Tez)</td></tr>
<tr><td>444</td><td>Apache Thrift (انظر Thrift)</td></tr>
<tr><td>(انظر أيضًا messaging systems)</td><td>Apache ZooKeeper (انظر ZooKeeper)</td></tr>
<tr><td>المقارنة مع log-based messaging, 448,</td><td>Apama (stream analytics), 466</td></tr>
<tr><td>451</td><td>append-only B-trees, 82, 242</td></tr>
<tr><td>ترتيب الرسائل, 446</td><td>append-only files (انظر logs)</td></tr>
<tr><td>analytics, 90</td><td>Application Programming Interfaces (APIs), 5,</td></tr>
<tr><td>المقارنة مع transaction processing, 91</td><td>27</td></tr>
<tr><td>data warehousing (انظر data warehousing)</td><td>لـbatch processing, 403</td></tr>
<tr><td>التنفيذ المتوازي للاستعلامات في MPP databases,</td><td>لـchange streams, 456</td></tr>
<tr><td>415</td><td>لـdistributed transactions, 361</td></tr>
<tr><td>predictive (انظر predictive analytics)</td><td>لـgraph processing, 425</td></tr>
<tr><td>علاقته بـbatch processing, 411</td><td>لـservices, 131-136</td></tr>
<tr><td>schemas الخاصة به, 93-95</td><td>(انظر أيضًا services)</td></tr>
<tr><td>snapshot isolation للاستعلامات, 238</td><td>evolvability, 136</td></tr>
<tr><td>stream analytics, 466</td><td>RESTful, 133</td></tr>
<tr><td>باستخدام MapReduce, تحليل أحداث نشاط المستخدمين</td><td>SOAP, 133</td></tr>
<tr><td>(مثال), 404</td><td>application state (انظر state)</td></tr>
<tr><td>anti-caching (قواعد بيانات in-memory), 89</td><td>approximate search (انظر similarity search)</td></tr>
<tr><td>anti-entropy, 178</td><td>archival storage, بيانات من قواعد البيانات, 131</td></tr>
<tr><td>Apache ActiveMQ (انظر ActiveMQ)</td><td>arcs (انظر edges)</td></tr>
<tr><td>Apache Avro (انظر Avro)</td><td>arithmetic mean, 14</td></tr>
<tr><td>Apache Beam (انظر Beam)</td><td>ASCII text, 119, 395</td></tr>
<tr><td>Apache BookKeeper (انظر BookKeeper)</td><td>ASN.1 (لغة schema), 127</td></tr>
<tr><td>Apache Cassandra (انظر Cassandra)</td><td>asynchronous networks, 278, 553</td></tr>
<tr><td>Apache CouchDB (انظر CouchDB)</td><td>المقارنة مع synchronous networks, 284</td></tr>
<tr><td>Apache Curator (انظر Curator)</td><td>النموذج الرسمي, 307</td></tr>
<tr><td>Apache Drill (انظر Drill)</td><td>asynchronous replication, 154, 553</td></tr>
<tr><td>Apache Flink (انظر Flink)</td><td>conflict detection, 172</td></tr>
<tr><td>Apache Giraph (انظر Giraph)</td><td>فقدان البيانات عند failover, 157</td></tr>
<tr><td>Apache Hadoop (انظر Hadoop)</td><td>القراءات من follower غير متزامن, 162</td></tr>
<tr><td>Apache HAWQ (انظر HAWQ)</td><td>Asynchronous Transfer Mode (ATM), 285</td></tr>
<tr><td>Apache HBase (انظر HBase)</td><td>atomic broadcast (انظر total order broadcast)</td></tr>
<tr><td>Apache Helix (انظر Helix)</td><td>atomic clocks (caesium clocks), 294, 295</td></tr>
<tr><td>Apache Hive (انظر Hive)</td><td>(انظر أيضًا clocks)</td></tr>
<tr><td>Apache Impala (انظر Impala)</td><td>atomicity (concurrency), 553</td></tr>
<tr><td>Apache Jena (انظر Jena)</td><td>atomic increment-and-get, 351</td></tr>
<tr><td>Apache Kafka (انظر Kafka)</td><td>compare-and-set, 245, 327</td></tr>
<tr><td>Apache Lucene (انظر Lucene)</td><td>(انظر أيضًا compare-and-set operations)</td></tr>
<tr><td>Apache MADlib (انظر MADlib)</td><td>العمليات المنسوخة, 246</td></tr>
<tr><td>Apache Mahout (انظر Mahout)</td><td>write operations, 243</td></tr>
<tr><td>Apache Oozie (انظر Oozie)</td><td>atomicity (transactions), 223, 228, 553</td></tr>
<tr><td>Apache Parquet (انظر Parquet)</td><td>atomic commit, 353</td></tr>
<tr><td>Apache Qpid (انظر Qpid)</td><td>تجنّبها, 523, 528</td></tr>
<tr><td>Apache Samza (انظر Samza)</td><td>حاجبة وغير حاجبة, 359</td></tr>
<tr><td>Apache Solr (انظر Solr)</td><td>في stream processing, 360, 477</td></tr>
<tr><td>Apache Spark (انظر Spark)</td><td>صيانة البيانات المشتقة, 453</td></tr>
</table>

<!-- page 583 -->

لـmulti-object transactions, 229 للكتابات أحادية الكائن, 230 auditability (قابلية التدقيق), 528-533 التصميم من أجلها, 531 الأنظمة ذات التدقيق الذاتي, 530 عبر immutability, 460 أدوات لأنظمة بيانات قابلة للتدقيق, 532 availability, 8 (انظر أيضًا fault tolerance) في CAP theorem, 337 في service level agreements (SLAs), 15 Avro (data format), 122-127 توليد الشيفرة, 127 schemas مولّدة ديناميكيًا, 126 object container files, 125, 131, 414 القارئ الذي يحدّد schema الكاتب, 125 تطوّر schema, 123 استخدامه في Hadoop, 414 awk (Unix tool), 391 AWS (انظر Amazon Web Services) Azure (انظر Microsoft)

B B-trees (indexes), 79-83 صيغ append-only/copy-on-write, 82, 242 معامل التفرّع, 81 المقارنة مع LSM-trees, 83-85 التعافي من الانهيار, 82 النمو بتقسيم صفحة, 81 تحسينات, 82 تشابهه مع dynamic partitioning, 212 backpressure, 441, 553 في TCP, 282 backups لقطة database للـreplication, 156 سلامتها, 530 snapshot isolation لها, 238 استخدامها في عمليات ETL, 405 التوافق مع الإصدارات الأقدم, 112 BASE, في مقابل ACID, 223 bash shell (Unix), 70, 395, 503 batch processing, 28, 389-431, 553 الدمج مع stream processing lambda architecture, 497 technologies الموحِّدة, 498 المقارنة مع MPP databases, 414-418 المقارنة مع stream processing, 464 المقارنة مع Unix, 413-414

dataflow engines, 421-423 fault tolerance, 406, 414, 422, 442 لـdata integration, 494-498 الرسوم البيانية والمعالجة التكرارية, 424-426 APIs ولغات عالية المستوى, 403, 426-429 log-based messaging و, 451 صيانة الحالة المشتقة, 495 MapReduce وأنظمة الملفات الموزّعة, 397-413 (انظر أيضًا MapReduce) قياس الأداء, 13, 390 المخرجات, 411-413 key-value stores, 412 فهارس البحث, 411 استخدام أدوات Unix (مثال), 391-394 Bayou (database), 522 Beam (مكتبة dataflow), 498 bias, 534 big ball of mud, 20 Bigtable data model, 41, 99 ترميزات البيانات الثنائية, 115-128 Avro, 122-127 MessagePack, 116-117 Thrift وProtocol Buffers, 117-121 الترميز الثنائي المبني على schemas, 127 بواسطة network drivers, 128 السلاسل الثنائية, عدم دعمها في JSON وXML, 114 ترميز BinaryProtocol (Thrift), 118 Bitcask (محرك تخزين), 72 التعافي من الانهيار, 74 Bitcoin (عملة رقمية), 532 Byzantine fault tolerance, 305 أخطاء التزامن في البورصات, 233 فهارس bitmap, 97 blockchains, 532 Byzantine fault tolerance, 305 atomic commit حاجب, 359 Bloom (لغة برمجة), 504 Bloom filter (خوارزمية), 79, 466 BookKeeper (replicated log), 372 Bottled Water (change data capture), 455 bounded datasets, 430, 439, 553 (انظر أيضًا batch processing) bounded delays, 553 في الشبكات, 285 توقف العمليات (process pauses), 298 broadcast hash joins, 409

<!-- page 584 -->

brokerless messaging, 442 Brubeck (مُجمِّع metrics), 442 BTM (منسّق المعاملات), 356 نموذج bulk synchronous parallel (BSP), 425 أنماط حركة مرور الشبكة المتقطّعة, 285 معالجة بيانات الأعمال, 28, 90, 390 byte sequence, ترميز البيانات فيه, 112 أعطال Byzantine, 304-306, 307, 553 أنظمة متسامحة مع أعطال Byzantine, 305, 532 مسألة الجنرالات البيزنطية, 304 وخوارزميات consensus, 366

## C

