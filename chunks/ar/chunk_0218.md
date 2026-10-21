graph databases مقابل, 60 imperative query APIs, 46 Network Time Protocol (انظر NTP) networks الازدحام والانتظار في الطوابير, 282 طوبولوجيات شبكات datacenter, 276 faults (انظر faults) linearizability وتأخيرات الشبكة, 338 network partitions, 279, 337 timeouts والتأخيرات غير المحدودة, 281 next-key locking, 260 nodes (في الرسوم البيانية) (انظر vertices) nodes (عمليات), 556 التعامل مع انقطاع الخدمة في leader-based replication, 156 نماذج النظام considerate للفشل, 307 noisy neighbors, 284 atomic commit غير حاجب, 359 عمليات غير حتمية عدم الحتمية العرضية, 423 الأعطال الجزئية في الأنظمة الموزعة, 275 المتطلبات غير الوظيفية, 22 القراءات غير المتكررة, 238 (انظر أيضًا read skew) normalization (تمثيل البيانات), 33, 556 تنفيذ joins, 39, 42, 403 مراجع foreign key, 231 في system of record, 386 مقابل denormalization, 462 NoSQL, 29, 499 transactions و, 223 Notation3 (N3), 56 npm (مدير الحزم), 428 NTP (Network Time Protocol), 287 الدقة, 289, 293 تعديلات على monotonic clocks, 289 عناوين server متعددة, 306 الأرقام, في ترميز XML و JSON, 114 O

أطر object-relational mapping (ORM), 30 معالجة الأخطاء والمعاملات المُجهَضة, 232 شفرة دورات read-modify-write غير الآمنة, 244 عدم التطابق الكائني-العلائقي, 29 observer pattern, 506 الأنظمة دون اتصال, 390 (انظر أيضًا batch processing)

العملاء ذوو الحالة والقادرون على العمل دون اتصال, 170, 511 تطبيقات offline-first, 511 offsets consumer offsets في logs مقسّمة, 449 messages في logs مقسّمة, 447 OLAP (online analytic processing), 91, 556 مكعبات البيانات, 102 OLTP (online transaction processing), 90, 556 استعلامات analytics مقابل, 411 خصائص عبء العمل, 253 علاقات واحد-إلى-متعدد, 30 تمثيل JSON, 32 الأنظمة المتصلة, 389 (انظر أيضًا services) Oozie (مُجدول سير العمل), 402 OpenAPI (صيغة تعريف الخدمة), 133 OpenStack Nova (بنية تحتية سحابية) استخدام ZooKeeper, 370 Swift (تخزين كائنات), 398 قابلية التشغيل, 19 أنظمة التشغيل مقابل قواعد البيانات, 499 معرّفات العمليات, 518, 522 التحويل التشغيلي, 174 operators, 421 تدفّق البيانات بينها, 424 في stream processing, 464 التحكم المتزامن المتفائل, 261 Oracle (قاعدة بيانات) دعم المعاملات الموزّعة, 361 GoldenGate (change data capture), 161, 170, 455 غياب serializability, 226 leader-based replication, 153 multi-table index cluster tables, 41 عدم منع write skew, 248 الفهارس المقسّمة, 209 لغة PL/SQL, 255 منع فقدان التحديثات, 245 عزل read committed, 236 Real Application Clusters (RAC), 330 دعم الاستعلامات التكرارية, 54 دعم snapshot isolation, 239, 242 TimesTen (قاعدة بيانات في الذاكرة), 89 replication القائمة على WAL, 160 دعم XML, 30 ordering, 339-352 بأرقام التسلسل, 343-348 causal ordering, 339-343

<!-- page 601 -->

partial order, 341 حدود total ordering, 493 total order broadcast, 348-352 Orleans (actor framework), 139 outliers (زمن الاستجابة), 14 Oz (لغة برمجة), 504

P مديرو الحزم, 428, 505 تبديل الحزم, 285 الحزم تلفها, 306 إرسالها عبر UDP, 442 PageRank (خوارزمية), 49, 424 paging (انظر virtual memory) ParAccel (قاعدة بيانات), 93 قواعد البيانات المتوازية (انظر massively parallel processing) التنفيذ المتوازي لخوارزميات تحليل الرسوم البيانية, 426 الاستعلامات في قواعد بيانات MPP, 216 Parquet (صيغة بيانات), 96, 131 (انظر أيضًا column-oriented storage) استخدامها في Hadoop, 414 الأعطال الجزئية, 275, 310 التعرّج, 311 partial order, 341 partitioning, 199-218, 556 و replication, 200 في batch processing, 429 عمليات multi-partition, 514 فرض القيود, 522 صيانة الفهرس, 495 من بيانات key-value, 201-205 بنطاق المفتاح, 202 skew و hot spots, 205 إعادة توازن partitioning, 209-214 إعادة التوازن التلقائي أو اليدوي, 213 مشكلات hash mod N, 210 باستخدام partitioning الديناميكي, 212 باستخدام عدد ثابت من الأجزاء, 210 باستخدام عدد ثابت من الأجزاء لكل عقدة, 212 و replication, 147 توجيه الطلبات, 214-216 الفهارس الثانوية, 206-209 partitioning حسب المستند, 206 partitioning حسب المصطلح, 208 التنفيذ التسلسلي للمعاملات و, 255

Paxos (خوارزمية consensus), 366

رقم ballot, 368 Multi-Paxos (total order broadcast), 367 percentiles, 14, 556 حسابها بكفاءة, 16 أهمية percentiles العالية, 16 استخدامها في service level agreements (SLAs), 15 Percona XtraBackup (أداة MySQL), 156

## الأداء

وصف, 13 لـ distributed transactions, 360 لقواعد بيانات in-memory, 89 لـ linearizability, 338 لـ multi-leader replication, 169 عدم الاتساق الدائم, 525 التحكم المتزامن المتشائم, 261 phantoms (عزل المعاملات), 250 تجسيد التعارضات, 251 منعه, في serializability, 259 physical clocks (انظر clocks) pickle (Python), 113

Pig (لغة dataflow), 419, 427 replicated joins, 409 skewed joins, 407 workflows, 403

Pinball (مُجدول سير العمل), 402

التنفيذ المتدفّق, 423 في Unix, 394

point in time, 287

polyglot persistence, 29

polystores, 501

PostgreSQL (قاعدة بيانات)

BDR (multi-leader replication), 170 causal ordering للكتابات, 177 Bottled Water (change data capture), 455 Bucardo (trigger-based replication), 161, 173 دعم المعاملات الموزّعة, 361 foreign data wrappers, 501 دعم البحث النصّي الكامل, 490 leader-based replication, 153 log sequence number, 156 تنفيذ MVCC, 239, 241 لغة PL/pgSQL, 255 فهارس PostGIS الجغرافية المكانية, 87 منع فقدان التحديثات, 245 منع write skew, 248, 261 عزل read committed, 236 دعم الاستعلامات التكرارية, 54 تمثيل الرسوم البيانية, 51

<!-- page 602 -->

عزل snapshot القابل للتسلسل (SSI), 261 دعم snapshot isolation, 239, 242 replication القائمة على WAL, 160 دعم XML و JSON, 30, 42 pre-splitting, 212 Precision Time Protocol (PTP), 290 أقفال predicate, 259 التحليلات التنبؤية, 533-536 تضخيم التحيّز, 534 أخلاقياته (انظر ethics) حلقات التغذية الراجعة, 536 استباحة موارد datacenter, 418 للخيوط, 298 نموذج المعالجة Pregel, 425 المفاتيح الأساسية, 85, 556 مفتاح أساسي مركّب (Cassandra), 204 replication الأساسي-الثانوي (انظر leader-based replication) الخصوصية, 536-543 الموافقة وحرية الاختيار, 538 البيانات كأصول وقوة, 540 حذف البيانات, 463 الاعتبارات الأخلاقية (انظر ethics) التشريعات والتنظيم الذاتي, 542 معناها, 539 المراقبة, 537 تتبّع البيانات السلوكية, 536 الخوارزميات الاحتمالية, 16, 466 توقفات العمليات, 295-299 زمن المعالجة (للأحداث), 469 المُنتِجون (message streams), 440 لغات البرمجة لغات dataflow, 504 لـ stored procedures, 255 functional reactive programming (FRP), 504

البرمجة المنطقية, 504 Prolog (لغة), 61 (انظر أيضًا Datalog) promises (عمليات غير متزامنة), 135 property graphs, 50 لغة استعلام Cypher, 52 Protocol Buffers (صيغة بيانات), 117-121 وسوم الحقول وتطور schema, 120 منشأ البيانات (provenance), 531 نموذج publish/subscribe, 441 المُنشرون (message streams), 440 آلات التبويب بالبطاقات المثقوبة, 390

الدوال الصافية, 48 وضع الحساب بالقرب من البيانات, 400

## Q

Qpid (messaging), 444 جودة الخدمة (QoS), 285 Quantcast File System (نظام ملفات موزّع), 398 لغات الاستعلام, 42-48 aggregation pipeline, 48 CSS و XSL, 44 Cypher, 52 Datalog, 60 Juttle, 504 الاستعلام في MapReduce, 46-48 استعلامات SQL التكرارية, 53 الجبر العلائقي و SQL, 42 SPARQL, 59 query optimizers, 37, 427 تأخيرات الاخدود (الشبكات), 282 head-of-line blocking, 15 latency وزمن الاستجابة, 14 queues (messaging), 137 quorums, 179-182, 556 لـ leaderless replication, 179 في خوارزميات consensus, 368 حدود الاتساق, 181-183, 334 اتخاذ القرارات في الأنظمة الموزعة, 301 مراقبة التقادم, 182 replication عبر مراكز بيانات متعددة, 184 الاعتماد على durability, 309 quorums المرنة و hinted handoff, 183

## R

R-trees (indexes), 87

RabbitMQ (messaging), 137, 444 leader-based replication, 153 race conditions, 225 (انظر أيضًا concurrency) تجنّبها باستخدام linearizability, 331 ناجمة عن الكتابة المزدوجة, 452 dirty writes, 235 في زيادة العدّادات, 235 فقدان التحديثات, 242-246 منعها باستخدام event logs, 462, 507 منعها باستخدام العزل القابل للتسلسل, 252 write skew, 246-251

Raft (خوارزمية consensus), 366

<!-- page 603 -->

