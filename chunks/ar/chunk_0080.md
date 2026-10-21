[1] David J. DeWitt وJim N. Gray: «أنظمة قواعد البيانات المتوازية: مستقبل أنظمة قواعد البيانات عالية الأداء»، Communications of the ACM، المجلد 35، العدد 6، الصفحات 85–98، يونيو 1992. doi:10.1145/129888.129894 [2] Lars George: «مقارنة HBase مع BigTable»، larsgeorge.com، نوفمبر 2009. [3] «دليل Apache HBase المرجعي»، Apache Software Foundation، hbase.apache.org، 2014. [4] MongoDB, Inc.: «ميزة sharding الجديدة القائمة على hash في MongoDB 2.4»، blog.mongodb.org، 10 أبريل 2013. [5] Ikai Lan: «نصيحة حول App Engine Datastore: القيم المتزايدة رتيبًا سيئة»، ikaisays.com، 25 يناير 2011. [6] Martin Kleppmann: «hashCode في Java غير آمن للأنظمة الموزّعة»، martin.kleppmann.com، 18 يونيو 2012. [7] David Karger وEric Lehman وTom Leighton وآخرون: «Consistent hashing والأشجار العشوائية: بروتوكولات caching موزّعة لتخفيف نقاط السخونة على الويب»، في 29th Annual ACM Symposium on Theory of Computing (STOC)، الصفحات 654–663، 1997. doi:10.1145/258533.258660 [8] John Lamping وEric Veach: «خوارزمية consistent hashing سريعة ذات ذاكرة دنيا»، arxiv.org، يونيو 2014. [9] Eric Redmond: «كتاب صغير عن Riak»، الإصدار 1.4.0، Basho Technologies، سبتمبر 2013. [10] «دليل مسؤول Couchbase 2.5»، Couchbase, Inc.، 2014. [11] Avinash Lakshman وPrashant Malik: «Cassandra – نظام تخزين مُهيكل لا مركزي»، في 3rd ACM SIGOPS International Workshop on Large Scale Distributed Systems and Middleware (LADIS)، أكتوبر 2009. [12] Jonathan Ellis: «ورقة Facebook حول Cassandra، مشروحة ومقارنة بـ Apache Cassandra 2.0»، datastax.com، 12 سبتمبر 2013. [13] «مقدمة إلى لغة استعلام Cassandra»، DataStax, Inc.، 2014. [14] Samuel Axon: «3% من خوادم Twitter مخصّصة لـ Justin Bieber»، mashable.com، 7 سبتمبر 2010. [15] «توثيق Riak 1.4.8»، Basho Technologies, Inc.، 2014.

<!-- page 241 -->

[16] Richard Low: «النقطة المثلى لفهرسة Cassandra الثانوية»، wentnet.com، 21 أكتوبر 2013. [17] Zachary Tong: «تخصيص توجيه مستنداتك»، elasticsearch.org، 3 يونيو 2013. [18] «دليل Apache Solr المرجعي»، Apache Software Foundation، 2014. [19] Andrew Pavlo: «الأسئلة الشائعة عن H-Store»، hstore.cs.brown.edu، أكتوبر 2013. [20] «دليل مطوّري Amazon DynamoDB»، Amazon Web Services, Inc.، 2014. [21] Rusty Klophaus: «الفرق بين 2I وSearch»، رسالة بريد إلكتروني إلى قائمة بريد riak-users، lists.basho.com، 25 أكتوبر 2011. [22] Donald K. Burleson: «تقسيم الكائنات في Oracle»، dba-oracle.com، 8 نوفمبر 2000. [23] Eric Evans: «إعادة التفكير في الطوبولوجيا في Cassandra»، في ApacheCon Europe، نوفمبر 2012. [24] Rafał Kuć: «شرح reroute API»، elasticsearchserverbook.com، 30 سبتمبر 2013. [25] «توثيق Project Voldemort»، project-voldemort.com. [26] Enis Soztutar: «تقسيم مناطق Apache HBase ودمجها»، hortonworks.com، 1 فبراير 2013. [27] Brandon Williams: «العقد الافتراضية في Cassandra 1.2»، datastax.com، 4 ديسمبر 2012. [28] Richard Jones: «libketama: مكتبة consistent hashing لعملاء Memcached»، metabrew.com، 10 أبريل 2007. [29] Branimir Lambov: «خوارزمية تخصيص جديدة للـtokens في Cassandra 3.0»، datastax.com، 28 يناير 2016. [30] Jason Wilder: «اكتشاف الخدمات مفتوح المصدر»، jasonwilder.com، فبراير 2014. [31] Kishore Gopalakrishna وShi Lu وZhen Zhang وآخرون: «فكّ اشتباك إدارة العناقيد مع Helix»، في ACM Symposium on Cloud Computing (SoCC)، أكتوبر 2012. doi:10.1145/2391229.2391248 [32] «دليل Moxi 1.8»، Couchbase, Inc.، 2014. [33] Shivnath Babu وHerodotos Herodotou: «قواعد البيانات المتوازية على نطاق واسع وأنظمة MapReduce»، Foundations and Trends in Databases، المجلد 5، العدد 1، الصفحات 1–104، نوفمبر 2013. doi:10.1561/1900000036

<!-- page 242 -->

<table>
<tr><th>PHANTOMS</th><th>التنفيذ التسلسلي الفعلي •</th></tr>
<tr><td>Two-phase</td><td></td></tr>
<tr><td>locking</td><td></td></tr>
<tr><td></td><td></td></tr>
</table>

<table>
<tr><th>Serializable</th><th></th></tr>
<tr><td>No snapshot</td><td>Write Skew</td></tr>
<tr><td>isolation</td><td>.</td></tr>
<tr><td>ISOLATION</td><td></td></tr>
<tr><td></td><td></td></tr>
</table>

<table>
<tr><th></th><th>MVCC</th><th></th><th></th></tr>
<tr><td></td><td>7</td><td></td><td></td></tr>
<tr><td>•</td><td>No Read Skew</td><td>N</td><td>Lost Updates</td></tr>
<tr><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>Row-level</td><td></td><td></td></tr>
<tr><td></td><td>locking</td><td></td><td></td></tr>
<tr><td></td><td>No</td><td></td><td></td></tr>
<tr><td></td><td>Dirty</td><td></td><td></td></tr>
<tr><td></td><td>Reads</td><td></td><td></td></tr>
<tr><td>Dirty Reads</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td>-</td></tr>
<tr><td></td><td></td><td colspan="2">ذرّية متعدد الكائنات</td></tr>
<tr><td></td><td></td><td></td><td>- - …</td></tr>
<tr><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td>إلى</td></tr>
<tr><td></td><td></td><td></td><td>المعاملات الموزّعة</td></tr>
<tr><td></td><td></td><td></td><td>– (الفصل 9)</td></tr>
</table>

<!-- page 243 -->

## الفصل 7 Transactions

لقد ادّعى بعض المؤلفين أن two-phase commit العام مكلف أكثر من اللازم بحيث لا يمكن دعمه، بسبب مشكلات الأداء أو التوافر التي يجلبها. ونحن نعتقد أن من الأفضل أن يتعامل مبرمجو التطبيقات مع مشكلات الأداء الناتجة عن الإفراط في استخدام المعاملات مع ظهور الاختناقات، بدلًا من أن يتغنّوا دائمًا في كتابة الشيفرة نتيجةً لغياب المعاملات.

—James Corbett وآخرون، Spanner: Google’s Globally-Distributed Database (2012)

في الواقع القاسي لأنظمة البيانات، يمكن أن تسوء أشياء كثيرة:

• قد يفشل برنامج قاعدة البيانات أو عتادها في أي وقت (بما في ذلك في منتصف عملية كتابة).
• قد ينهار التطبيق في أي وقت (بما في ذلك في منتصف سلسلة من العمليات).
• يمكن أن تقطع انقطاعات الشبكة التطبيقَ فجأة عن قاعدة البيانات، أو تقطع عقدة قاعدة بيانات عن أخرى.
• قد يكتب عدة عملاء إلى قاعدة البيانات في الوقت نفسه، متجاوزين تغييرات بعضهم البعض.
• قد يقرأ عميل بيانات لا معنى لها لأنها لم تُحدَّث إلا جزئيًا.
• يمكن أن تسبّب حالات السباق (race conditions) بين العملاء أخطاءً مفاجئة.

لكي يكون موثوقًا، على النظام أن يتعامل مع هذه الأعطال ويضمن أنها لا تسبّب فشلًا كارثيًا للنظام كله. غير أن تنفيذ آليات تحمّل الأعطال (fault tolerance) عملٌ كبير. فهو يتطلب قدرًا كبيرًا من التفكير الدقيق في كل ما يمكن أن يسوء، وقدرًا كبيرًا من الاختبارات لضمان أن الحل يعمل فعلًا.

<!-- page 244 -->

لعقود من الزمن، كانت المعاملات (transactions) هي الآلية المفضّلة لتبسيط هذه المسائل. المعاملة طريقة لتجميع عدة عمليات قراءة وكتابة معًا في وحدة منطقية واحدة. ومن الناحية المفاهيمية، تُنفَّذ جميع عمليات القراءة والكتابة في المعاملة كعملية واحدة: إما أن تنجح المعاملة بالكامل (commit) أو أنها تفشل (abort، rollback). وإذا فشلت، فيستطيع التطبيق إعادة المحاولة بأمان. ومع المعاملات، تصبح معالجة الأخطاء أبسط بكثير للتطبيق، لأنه لا يحتاج إلى القلق بشأن الفشل الجزئي— أي الحالة التي تنجح فيها بعض العمليات وتفشل أخرى (لأي سبب كان).

إذا كنت قد أمضيت سنوات في العمل مع المعاملات، فقد تبدو بديهية، لكننا لا ينبغي أن نأخذها على محمل الجدل. المعاملات ليست قانونًا من قوانين الطبيعة؛ لقد أُنشئت لغرض معيّن، هو تبسيط نموذج البرمجة للتطبيقات التي تصل إلى قاعدة بيانات. وباستخدام المعاملات، يبقى التطبيق حرًا في تجاهل بعض سيناريوهات الخطأ المحتملة ومشاكل التزامن، لأن قاعدة البيانات تتولّى ذلك بدلًا منه (ونحن نسمّي هذه ضمانات السلامة).

ليست كل التطبيقات بحاجة إلى المعاملات، وأحيانًا تكون هناك فوائد لإضعال الضمانات المعاملية أو للتخلّي عنها تمامًا (على سبيل المثال، لتحقيق أداء أعلى أو توافر أعلى). ويمكن تحقيق بعض خصائص السلامة دون معاملات.

كيف تعرّف ما إذا كنت بحاجة إلى المعاملات؟ للإجابة عن هذا السؤال، نحتاج أولًا إلى أن نفهم بدقة ما هي ضمانات السلامة التي يمكن أن تقدّمها المعاملات، وما هي التكاليف المرتبطة بها. ورغم أن المعاملات تبدو بديهية للوهلة الأولى، فإن هناك في الواقع الكثير من التفاصيل الدقيقة المهمة التي تدخل في الحسبان.

