[27] James C. Corbett وJeffrey Dean وMichael Epstein وآخرون: “Spanner: Google’s Globally-Distributed Database”، في مؤتمر 10th USENIX Symposium on Operating System Design and Implementation (OSDI)، أكتوبر 2012. [28] Donald K. Burleson: “Reduce I/O with Oracle Cluster Tables”، dba-oracle.com. [29] Fay Chang وJeffrey Dean وSanjay Ghemawat وآخرون: “Bigtable: A Distributed Storage System for Structured Data”، في مؤتمر 7th USENIX Symposium on Operating System Design and Implementation (OSDI)، نوفمبر 2006. [30] Bobbie J. Cochrane وKathy A. McKnight: “DB2 JSON Capabilities, Part 1: Introduction to DB2 JSON”، IBM developerWorks، 20 يونيو 2013. [31] Herb Sutter: “The Free Lunch Is Over: A Fundamental Turn Toward Concurrency in Software”، Dr. Dobb’s Journal، المجلد 30، العدد 3، الصفحات 202-210، مارس 2005. [32] Joseph M. Hellerstein: “The Declarative Imperative: Experiences and Conjectures in Distributed Logic”، Electrical Engineering and Computer Sciences، University of California at Berkeley، تقرير تقني UCB/EECS-2010-90، يونيو 2010. [33] Jeffrey Dean وSanjay Ghemawat: “MapReduce: Simplified Data Processing on Large Clusters”، في مؤتمر 6th USENIX Symposium on Operating System Design and Implementation (OSDI)، ديسمبر 2004. [34] Craig Kerstiens: “JavaScript in Your Postgres”، blog.heroku.com، 5 يونيو 2013. [35] Nathan Bronson وZach Amsden وGeorge Cabrera وآخرون: “TAO: Facebook’s Distributed Data Store for the Social Graph”، في مؤتمر USENIX Annual Technical Conference (USENIX ATC)، يونيو 2013. [36] “Apache TinkerPop3.2.3 Documentation”، tinkerpop.apache.org، أكتوبر 2016. [37] “The Neo4j Manual v2.0.0”، Neo Technology، 2013. [38] Emil Eifrem: مراسلات عبر Twitter، 3 يناير 2014. [39] David Beckett وTim Berners-Lee: “Turtle – Terse RDF Triple Language”، W3C Team Submission، 28 مارس 2011. [40] “Datomic Development Resources”، Metadata Partners, LLC، 2013. [41] W3C RDF Working Group: “Resource Description Framework (RDF)”، w3.org، 10 فبراير 2004.

[42] “Apache Jena”، Apache Software Foundation.

<!-- page 89 -->

[43] Steve Harris وAndy Seaborne وEric Prud’hommeaux: “SPARQL 1.1 Query Language”، W3C Recommendation، مارس 2013.

[44] Todd J. Green وShan Shan Huang وBoon Thau Loo وWenchao Zhou: “Datalog and Recursive Query Processing”، Foundations and Trends in Databases، المجلد 5، العدد 2، الصفحات 105–195، نوفمبر 2013. doi:10.1561/1900000017

[45] Stefano Ceri وGeorg Gottlob وLetizia Tanca: “What You Always Wanted to Know About Datalog (And Never Dared to Ask)”، IEEE Transactions on Knowledge and Data Engineering، المجلد 1، العدد 1، الصفحات 146–166، مارس 1989. doi: 10.1109/69.43410 [46] Serge Abiteboul وRichard Hull وVictor Vianu: Foundations of Databases. Addison-Wesley، 1995. ISBN: 978-0-201-53771-0، متاح على الإنترنت على web‐dam.inria.fr/Alice [47] Nathan Marz: “Cascalog”، cascalog.org.

[48] Dennis A. Benson وIlene Karsch-Mizrachi وDavid J. Lipman وآخرون: “GenBank”، Nucleic Acids Research، المجلد 36، عدد قاعدة البيانات (Database issue)، الصفحات D25–D30، ديسمبر 2007. doi:10.1093/nar/gkm929 [49] Fons Rademakers: “ROOT for Big Data Analysis”، في ورشة العمل Workshop on the Future of Big Data Management، لندن، المملكة المتحدة، يونيو 2013.

<!-- page 90 -->

Q Q AQ V Q o Z <

<table>
<tr><th></th><th></th></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>c</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>O</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>=</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>2)</td></tr>
<tr><td></td><td>u</td></tr>
<tr><td></td><td>&lt;</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>O</td></tr>
<tr><td>৩</td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>V</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>o</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>7</td></tr>
<tr><td></td><td></td></tr>
<tr><td>4</td><td></td></tr>
<tr><td></td><td>V</td></tr>
<tr><td></td><td></td></tr>
</table>

=

<!-- page 91 -->

## التخزين والاسترجاع

من يحافظ على الترتيب ليس إلا كسولًا عن البحث.

(إذا أبقيت الأشياء مرتّبة بأناقة، فأنت كسول فحسب عن البحث.) —مثلّ ألماني

على المستوى الأكثر أساسًا، تحتاج قاعدة البيانات إلى أن تفعل أمرين: حين تعطيها بعض البيانات، ينبغي أن تخزّن البيانات، وحين تطلبها منها لاحقًا، ينبغي أن تُعيد إليك البيانات.

في الفصل 2 ناقشنا نماذج البيانات ولغات الاستعلام (query languages)—أي الصيغة التي تعطي بها أنت (مطوّر التطبيق) بياناتك إلى قاعدة البيانات، والآلية التي يمكنك بواسطتها أن تطلبها مرة أخرى لاحقًا. وفي هذا الفصل نناقش الأمر نفسه من وجهة نظر قاعدة البيانات: كيف يمكننا تخزين البيانات التي تُعطى إلينا، وكيف يمكننا العثور عليها مرة أخرى حين يُطلب ذلك منا.

لماذا ينبغي لك، وأنت مطوّر تطبيقات، أن يهمّ بكيفية تعامل قاعدة البيانات مع التخزين والاسترجاع من الداخل؟ من المرجّح أنك لن تُنفّذ محرك تخزين خاصًا بك من الصفر، لكن عليك أن تختار محرك تخزين مناسبًا لتطبيقك من بين المحركات العديدة المتاحة. ومن أجل ضبط (tune) محرك تخزين ليتحقق أداءً جيدًا على نوع أحمال العمل (workload) لديك، تحتاج إلى فكرة تقريبية عمّا يفعله محرك التخزين تحت الغطاء (under the hood).

على وجه الخصوص، هناك فرق كبير بين محركات التخزين المُحسَّنة لأحمال العمل المعاملاتية (transactional workloads) وتلك المُحسَّنة للتحليلات (analytics). وسنستكشف هذا التمييز لاحقًا في «معالجة المعاملات أم التحليلات؟» في صفحة 90، وفي «التخزين العمودي (Column-Oriented Storage)» في صفحة 95 سنناقش عائلة من محركات التخزين المُحسَّنة للتحليلات.

غير أن الفصل يبدأ أولًا بالتحدّث عن محركات التخزين المستخدَمة في أنواع قواعد البيانات التي من المرجّح أن تكون على معرفة بها: قواعد البيانات العلائقية التقليدية، وكذلك معظم قواعد بيانات NoSQL المعروفة بهذا الاسم. وسندرس عائلتين من

<!-- page 92 -->

محركات التخزين: محركات تخزين ذات البنية السجلية (log-structured storage engines)، ومحركات تخزين موجّهة نحو الصفحات (page-oriented storage engines) مثل B-trees.

## بنيات البيانات التي تُشغّل قاعدة بياناتك

تخيَّل أبسط قاعدة بيانات في العالم، والمُنفَّذة في صورة دالتين من Bash:

#!/bin/bash db_set () { echo "$1,$2" >> database } db_get () { grep "^$1," database | sed -e "s/^$1,//" | tail -n 1 }

تنفّذ هاتان الدالتان مخزن مفتاح-قيمة (key-value store). يمكنك استدعاء db_set key value،uhan سيخزّن المفتاح والقيمة في قاعدة البيانات. ويمكن أن يكون المفتاح والقيمة أي شيء (تقريبًا) تريده—على سبيل المثال، يمكن أن تكون القيمة مستند JSON. وعندئذٍ يمكنك استدعاء db_get key، التي تبحث عن أحدث قيمة مرتبطة بذلك المفتاح تحديدًا وتُعيدها.

وهو يعمل:

$ db_set 123456 '{"name":"London","attractions":["Big Ben","London Eye"]}' $ db_set 42 '{"name":"San Francisco","attractions":["Golden Gate Bridge"]}' $ db_get 42 {"name":"San Francisco","attractions":["Golden Gate Bridge"]}

صيغة التخزين الأساسية بسيطة جدًا: ملف نصي يحتوي كل سطر فيه على زوج مفتاح-قيمة، مفصول بفاصلة (تقريبًا مثل ملف CSV، مع تجاهل مسائل تهريب المحارف). وكل استدعاء لـ db_set يُلحق بالبيانات في نهاية الملف، لذا إن حدّدت قيمة مفتاح عدّة مرّات، فإن الإصدارات القديمة من القيمة لا تُستبدَل—بل عليك النظر في آخر ورود للمفتاح في الملف للعثور على أحدث قيمة (ولهذا السبب tail -n 1 في db_get):

$ db_set 42 '{"name":"San Francisco","attractions":["Exploratorium"]}' $ db_get 42 {"name":"San Francisco","attractions":["Exploratorium"]} $ cat database 123456,{"name":"London","attractions":["Big Ben","London Eye"]} 42,{"name":"San Francisco","attractions":["Golden Gate Bridge"]} 42,{"name":"San Francisco","attractions":["Exploratorium"]}

<!-- page 93 -->
