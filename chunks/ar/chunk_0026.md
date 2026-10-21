1. قواعد بيانات المستندات تستهدف حالات الاستخدام التي تأتي فيها البيانات في مستندات مكتفية بذاتها، والعلاقات بين مستند وآخر نادرة.
2. قواعد بيانات الرسوم البيانية تسير في الاتجاه المعاكس، فهي تستهدف حالات الاستخدام التي قد يكون فيها كل شيء مرتبطًا بكل شيء.

تُستخدم النماذج الثلاثة (نموذج المستندات، والعلائقي، والرسوم البيانية) على نطاق واسع اليوم، وكل واحد منها جيد في مجاله. ويمكن محاكاة نموذج واحد في نموذج آخر—على سبيل المثال، يمكن تمثيل بيانات الرسوم البيانية في قاعدة بيانات علائقية—لكن النتيجة غالبًا ما تكون محرجة. ولهذا السبب لدينا أنظمة مختلفة لأغراض مختلفة، وليس حلًا واحدًا يناسب كل شيء.

أمرٌ واحد تشترك فيه قواعد بيانات المستندات وقواعد بيانات الرسوم البيانية هو أنها لا تفرض عادةً schema على البيانات التي تخزّنها، مما قد يجعل من الأسهل تكييف التطبيقات مع المتطلبات المتغيّرة. غير أن تطبيقك على الأرجح ما يزال يفترض أن البيانات لها بنية معيّنة؛ وإنما المسألة هي فقط ما إذا كان الـ schema صريحًا (مُفرضًا عند الكتابة) أم ضمنيًا (يُعالَج عند القراءة).

يأتي كل نموذج بيانات مع لغته الاستعلامية (query language) أو framework الخاص به، وقد ناقشنا عدة أمثلة: SQL، وMapReduce، وaggregation pipeline لـ MongoDB، وCypher، وSPARQL، وDatalog. كما لمّحنا إلى CSS وXSL/XPath، وهما ليسا لغتي استعلام لقواعد البيانات، لكنهما يتشاركان معهما في أوجه تشابه لافتة.

رغم أننا غطّينا جوانب كثيرة، فما زالت هناك نماذج بيانات كثيرة لم نُشر إليها. ولإعطاء أمثلة موجزة فحسب:

• الباحثون الذين يعملون مع بيانات الجينوم يحتاجون غالبًا إلى إجراء عمليات بحث عن تشابه السلاسل (sequence-similarity searches)، أي أخذ سلسلة طويلة جدًا (تمثّل جزيء

<!-- page 86 -->

DNA) ومطابقتها مع قاعدة بيانات ضخمة من السلاسل المتشابهة، لكن غير المتطابقة تمامًا. ولا يمكن لأي من قواعد البيانات الموصوفة هنا التعامل مع هذا النوع من الاستخدام، ولهذا كتب الباحثون برمجيات متخصصة لقواعد بيانات الجينوم مثل GenBank [48].

• وقد كان فيزياء الجسيمات يجرون تحليلات بيانات واسعة النطاق بأسلوب Big Data منذ عقود، ومشاريع مثل Large Hadron Collider (LHC) تعمل الآن مع مئات petabytes! وعلى هذا النطاق، يلزم وجود حلول مخصصة لمنع تكاليف الأجهزة من الانفلات خارج السيطرة [49].
• ويمكن القول إن البحث النصي الكامل (full-text search) هو نوع من نماذج البيانات الذي يُستخدم كثيرًا إلى جانب قواعد البيانات. أما استرجاع المعلومات (information retrieval) فهو موضوع متخصص كبير لن نتناوله بتفصيل كبير في هذا الكتاب، لكننا سنلمّح إلى فهارس البحث (search indexes) في الفصل 3 والجزء الثالث.

لابدّ أن نترك الأمر عند هذا الحد الآن. وفي الفصل التالي سنناقش بعض المفاضلات (trade-offs) التي تظهر عند تنفيذ نماذج البيانات الموصوفة في هذا الفصل.

## المراجع

[1] Edgar F. Codd: “A Relational Model of Data for Large Shared Data Banks,” Communications of the ACM، المجلد 13، العدد 6، الصفحات 377–387، يونيو 1970. doi: 10.1145/362384.362685 [2] Michael Stonebraker وJoseph M. Hellerstein: “What Goes Around Comes Around,” في Readings in Database Systems، الطبعة 4، MIT Press، الصفحات 2–41، 2005. ISBN: 978-0-262-69314-1 [3] Pramod J. Sadalage وMartin Fowler: NoSQL Distilled. Addison-Wesley، أغسطس 2012. ISBN: 978-0-321-82662-6 [4] Eric Evans: “NoSQL: What’s in a Name?,” blog.sym-link.com، 30 أكتوبر 2009. [5] James Phillips: “Surprises in Our NoSQL Adoption Survey,” blog.couchbase.com، 8 فبراير 2012. [6] Michael Wagner: SQL/XML:2006 – Evaluierung der Standardkonformität ausgewählter Datenbanksysteme. Diplomica Verlag، Hamburg، 2010. ISBN: 978-3-836-64609-3 [7] “XML Data in SQL Server,” توثيق SQL Server 2012، technet.microsoft.com، 2013. [8] “PostgreSQL 9.3.1 Documentation,” The PostgreSQL Global Development Group، 2013. [9] “The MongoDB 2.4 Manual,” MongoDB, Inc.، 2013.

<!-- page 87 -->

[10] “RethinkDB 1.11 Documentation,” rethinkdb.com، 2013. [11] “Apache CouchDB 1.6 Documentation,” docs.couchdb.org، 2014. [12] Lin Qiao وKapil Surlaker وShirshanka Das وآخرون: “On Brewing Fresh Espresso: LinkedIn’s Distributed Data Serving Platform,” في ACM International Conference on Management of Data (SIGMOD)، يونيو 2013. [13] Rick Long وMark Harrington وRobert Hain وGeoff Nicholls: IMS Primer. IBM Redbook SG24-5352-00، IBM International Technical Support Organization، يناير 2000. [14] Stephen D. Bartlett: “IBM’s IMS—Myths, Realities, and Opportunities,” The Clipper Group Navigator، TCG2013015LI، يوليو 2013. [15] Sarah Mei: “Why You Should Never Use MongoDB,” sarahmei.com، 11 نوفمبر 2013. [16] J. S. Knowles وD. M. R. Bell: “The CODASYL Model,” في Databases—Role and Structure: An Advanced Course، بتحرير P. M. Stocker وP. M. D. Gray وM. P. Atkinson، الصفحات 19–56، Cambridge University Press، 1984. ISBN: 978-0-521-25430-4 [17] Charles W. Bachman: “The Programmer as Navigator,” Communications of the ACM، المجلد 16، العدد 11، الصفحات 653–658، نوفمبر 1973. doi: 10.1145/355611.362534 [18] Joseph M. Hellerstein وMichael Stonebraker وJames Hamilton: “Architecture of a Database System,” Foundations and Trends in Databases، المجلد 1، العدد 2، الصفحات 141–259، نوفمبر 2007. doi:10.1561/1900000002 [19] Sandeep Parikh وKelly Stirman: “Schema Design for Time Series Data in MongoDB,” blog.mongodb.org، 30 أكتوبر 2013. [20] Martin Fowler: “Schemaless Data Structures,” martinfowler.com، 7 يناير 2013. [21] Amr Awadallah: “Schema-on-Read vs. Schema-on-Write,” في Berkeley EECS RAD Lab Retreat، Santa Cruz، CA، مايو 2009. [22] Martin Odersky: “The Trouble with Types,” في Strange Loop، سبتمبر 2013. [23] Conrad Irwin: “MongoDB—Confessions of a PostgreSQL Lover,” في HTML5DevConf، أكتوبر 2013. [24] “Percona Toolkit Documentation: pt-online-schema-change,” Percona Ireland Ltd.، 2013. [25] Rany Keddo وTobias Bielohlawek وTobias Schmidt: “Large Hadron Migrator,” SoundCloud، 2013.

<!-- page 88 -->

[26] Shlomi Noach: “gh-ost: GitHub’s Online Schema Migration Tool for MySQL,” githubengineering.com، 1 أغسطس 2016.

