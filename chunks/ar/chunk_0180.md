التسهيلات الخاصة بالحفاظ على الحالة في هيئة streams وإعادة تشغيل الرسائل هي أيضًا الأساس الذي تقوم عليه التقنيات التي تتيح stream joins وتحَمّل الأعطال (fault tolerance) في مختلف أطر stream processing. وقد ناقشنا عدة أغراض لـstream processing، منها البحث عن أنماط الأحداث (complex event processing)، وحساب التجميعات ذات النوافذ (stream analytics)، وإبقاء أنظمة البيانات المشتقّة محدَّثة (materialized views).

ثم ناقشنا الصعوبات التي تنشأ عند التفكير في الزمن داخل مُعالج الـstream، بما في ذلك التمييز بين processing time وطوابع زمن الأحداث (event timestamps)، ومشكلة التعامل مع أحداث straggler التي تصل بعد أن كنت تظنّ أن نافذتك (window) قد اكتملت.

ميّزنا ثلاثة أنواع من عمليات join قد تظهر في عمليات stream:

## عمليات join بين streams

يتكوّن كلٌّ من مُدخَلا الـjoin من أحداث نشاط، ويبحث مُشغّل الـjoin عن أحداث مرتبطة تقع ضمن نافذة زمنية ما. فمثلًا، قد يطابق فعلين قام بهما المستخدم نفسه خلال 30 دقيقة من بعضهما. وقد يكون

<!-- page 503 -->

مُدخَلا الـjoin في الواقع هو التيار نفسه (self-join) إذا أردت العثور على أحداث مرتبطة داخل ذلك التيار الواحد.

## عمليات join بين stream وtable

يتكوّن أحد مُدخَلات الـstream من أحداث نشاط، بينما الآخر هو سجل تغييرات (changelog) لقاعدة بيانات. ويحرص الـchangelog على الإبقاء على نسخة محلية من قاعدة البيانات محدَّثة. ولكل حدث نشاط، يستعلم مُشغّل الـjoin من قاعدة البيانات ويُخرِج حدث نشاط مُثرًى.

## عمليات join بين table وtable

كلا مُدخَلا الـstream هما سجلَّا تغييرات (changelogs) لقاعدتَي بيانات. وفي هذه الحالة، يُضمّ كل تغيير في أحد الجانبين مع أحدث حالة في الجانب الآخر. والنتيجة هي stream من التغييرات على الـmaterialized view الخاص بعملية الـjoin بين الجدولين.

وأخيرًا، ناقشنا تقنيات تحقيق تحمّل الأعطال (fault tolerance) ودلالات exactly-once في مُعالج الـstream. وكما في batch processing، نحتاج إلى التخلص من الناتج الجزئي لأي مهمة فاشلة. لكن بما أن عملية stream طويلة التشغيل وتُنتج مخرجات باستمرار، فلا يمكننا ببساطة التخلص من كل المخرجات. وبدلًا من ذلك، يمكن استخدام آلية استعادة أدقّ التدرّج، تقوم على microbatching أو حفظ نقاط التحقّق (checkpointing) أو transactions أو idempotent writes.

## المراجع

[1] Tyler Akidau وRobert Bradshaw وCraig Chambers وآخرون: «نموذج Dataflow: نهج عملي للموازنة بين الصحّة (correctness) والlatency والتكلفة في معالجة بيانات ضخمة الحجم وغير محدودة وخارجة عن الترتيب»، Proceedings of the VLDB Endowment، المجلد 8، العدد 12، الصفحات 1792–1803، أغسطس 2015. doi:10.14778/2824032.2824076 [2] Harold Abelson وGerald Jay Sussman وJulie Sussman: بنية وتفسير برامج الحاسوب، الطبعة الثانية. MIT Press، 1996. ISBN: 978-0-262-51087-5، متاح على الإنترنت على mitpress.mit.edu

[3] Patrick Th. Eugster وPascal A. Felber وRachid Guerraoui وAnne-Marie Kermarrec: «أوجه كثيرة لـpublish/subscribe»، ACM Computing Surveys، المجلد 35، العدد 2، الصفحات 114–131، يونيو 2003. doi:10.1145/857076.857078

[4] Joseph M. Hellerstein وMichael Stonebraker: قراءات في أنظمة قواعد البيانات، الطبعة الرابعة. MIT Press، 2005. ISBN: 978-0-262-69314-1، متاح على الإنترنت على red‐ book.cs.berkeley.edu

[5] Don Carney وUğur Çetintemel وMitch Cherniack وآخرون: «مراقبة streams – فئة جديدة من تطبيقات إدارة البيانات»، في 28th International Conference on Very Large Data Bases (VLDB)، أغسطس 2002.

[6] Matthew Sackman: «الدفع إلى الخلف»، lshift.net، 5 مايو 2016.

<!-- page 504 -->

[7] Vicent Martí: «Brubeck، مُجمِّع metrics متوافق مع statsd»، githubengin‐ eering.com، 15 يونيو 2015. [8] Seth Lowenberger: «مواصفة بروتوكول MoldUDP64 الإصدار 1.00»، nasdaq‐ trader.com، يوليو 2009. [9] Pieter Hintjens: ZeroMQ – الدليل. O’Reilly Media، 2013. ISBN: 978-1-449-33404-8 [10] Ian Malpass: «قِس أي شيء، قِس كل شيء»، codeascraft.com، 15 فبراير 2011. [11] Dieter Plaetinck: «25 مَزْلقًا في Graphite وGrafana وstatsd»، blog.raintank.io، 3 مارس 2016. [12] Jeff Lindsay: «Web Hooks تُحدث ثورة في الويب»، progrium.com، 3 مايو 2007. [13] Jim N. Gray: «الطوابير قواعد بيانات»، Microsoft Research Technical Report MSR-TR-95-56، ديسمبر 1995. [14] Mark Hapner وRich Burridge وRahul Sharma وآخرون: «JSR-343 Java Message Service (JMS) 2.0 Specification»، jms-spec.java.net، مارس 2013. [15] Sanjay Aiyagari وMatthew Arrott وMark Atwell وآخرون: «AMQP: Advanced Message Queuing Protocol Specification»، Version 0-9-1، نوفمبر 2008. [16] «Google Cloud Pub/Sub: خدمة messaging بمقياس Google»، cloud.google.com، 2016. [17] «توثيق Apache Kafka 0.9»، kafka.apache.org، نوفمبر 2015. [18] Jay Kreps وNeha Narkhede وJun Rao: «Kafka: نظام messaging موزّع لمعالجة السجلات»، في 6th International Workshop on Networking Meets Databases (NetDB)، يونيو 2011. [19] «دليل المطوّرين لـAmazon Kinesis Streams»، docs.aws.amazon.com، أبريل 2016. [20] Leigh Stewart وSijie Guo: «بناء DistributedLog: خدمة سجلات مُكرَّرة عالية الأداء من Twitter»، blog.twitter.com، 16 سبتمبر 2015. [21] «توثيق DistributedLog»، Twitter, Inc.، distributedlog.io، مايو 2016. [22] Jay Kreps: «اختبار أداء Apache Kafka: مليونا كتابة في الثانية (على ثلاث أجهزة رخيصة)»، engineering.linkedin.com، 27 أبريل 2014. [23] Kartik Paramasivam: «كيف نُحسّن Kafka ونُطوّرها في LinkedIn»، engineering.linkedin.com، 2 سبتمبر 2015. [24] Jay Kreps: «السجل: ما ينبغي لكل مهندس برمجيات معرفته عن التجريد الموحِّد لبيانات real-time»، engineering.linkedin.com، 16 ديسمبر 2013.

<!-- page 505 -->

[25] Shirshanka Das وChavdar Botev وKapil Surlaker وآخرون: «كلنا على متن حافلة البيانات!»، في 3rd ACM Symposium on Cloud Computing (SoCC)، أكتوبر 2012. [26] Yogeshwer Sharma وPhilippe Ajoux وPetchean Ang وآخرون: «Wormhole: pub-sub موثوق لدعم خدمات إنترنت geo-replicated»، في 12th USENIX Symposium on Networked Systems Design and Implementation (NSDI)، مايو 2015. [27] P. P. S. Narayan: «تحديث Sherpa»، developer.yahoo.com، 8 يونيو، . [28] Martin Kleppmann: «Bottled Water: تكامل real-time بين PostgreSQL وKafka»، martin.kleppmann.com، 23 أبريل 2015. [29] Ben Osheroff: «تقديم Maxwell، معالِج binlog من mysql إلى kafka»، devel‐ oper.zendesk.com، 20 أغسطس 2015. [30] Randall Hauch: «إصدار Debezium 0.2.1»، debezium.io، 10 يونيو 2016. [31] Prem Santosh Udaya Shankar: «بثّ جداول MySQL إلى Kafka في real-time»، engineeringblog.yelp.com، 1 أغسطس 2016. [32] «Mongoriver»، Stripe, Inc.، github.com، سبتمبر 2014. [33] Dan Harvey: «Change Data Capture باستخدام Mongo + Kafka»، في Hadoop Users Group UK، أغسطس 2015. [34] «Oracle GoldenGate 12c: وصول real-time إلى معلومات real-time»، Oracle White Paper، مارس 2015. [35] «أساسيات Oracle GoldenGate: كيف يعمل Oracle GoldenGate»، Oracle Corporation، youtube.com، نوفمبر 2012. [36] Slava Akhmechet: «تطوير الويب realtime»، rethinkdb.com، 27 يناير 2015. [37] «توثيق Firebase Realtime Database»، Google, Inc.، firebase.google.com، مايو 2016. [38] «توثيق Apache CouchDB 1.6»، docs.couchdb.org، 2014. [39] Matt DeBergalis: «Meteor 0.7.0: استعلامات قواعد بيانات قابلة للتوسّع باستخدام MongoDB Oplog بدلًا من Poll-and-Diff»، info.meteor.com، 17 ديسمبر 2013. [40] «الفصل 15. استيراد البيانات الحيّة وتصديرها»، VoltDB 6.4 User Manual، docs.voltdb.com، يونيو 2016. [41] Neha Narkhede: «الإعلان عن Kafka Connect: بناء خطوط بيانات واسعة النطاق منخفضة latency»، confluent.io، 18 فبراير 2016. [42] Greg Young: «CQRS وEvent Sourcing»، في Code on the Beach، أغسطس 2014. [43] Martin Fowler: «Event Sourcing»، martinfowler.com، 12 ديسمبر 2005.

<!-- page 506 -->

[44] Vaughn Vernon: تطبيق التصميم القائم على النطاق (Domain-Driven Design). Addison-Wesley Profes‐ sional، 2013. ISBN: 978-0-321-83457-7

