[54] Sergey Melnik وAndrey Gubarev وJing Jing Long وآخرون: «Dremel: Interactive Analysis of Web-Scale Datasets»، في 36th International Conference on Very Large Data Bases (VLDB)، الصفحات 330–339، سبتمبر 2010. [55] Ralph Kimball وMargy Ross: The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling، الطبعة الثالثة. John Wiley & Sons، يوليو 2013. ISBN: 978-1-118-53080-1 [56] Derrick Harris: «Why Apple, eBay, and Walmart Have Some of the Biggest Data Warehouses You’ve Ever Seen»، gigaom.com، 27 مارس 2013. [57] Julien Le Dem: «Dremel Made Simple with Parquet»، blog.twitter.com، 11 سبتمبر 2013. [58] Daniel J. Abadi وPeter Boncz وStavros Harizopoulos وآخرون: «The Design and Implementation of Modern Column-Oriented Database Systems»، Foundations and Trends in Databases، المجلد 5، العدد 3، الصفحات 197–280، ديسمبر 2013. doi: 10.1561/1900000024 [59] Peter Boncz وMarcin Zukowski وNiels Nes: «MonetDB/X100: Hyper-Pipelining Query Execution»، في 2nd Biennial Conference on Innovative Data Systems Research (CIDR)، يناير 2005. [60] Jingren Zhou وKenneth A. Ross: «Implementing Database Operations Using SIMD Instructions»، في ACM International Conference on Management of Data (SIGMOD)، الصفحات 145–156، يونيو 2002. doi:10.1145/564691.564709 [61] Michael Stonebraker وDaniel J. Abadi وAdam Batkin وآخرون: «C-Store: A Column-Oriented DBMS»، في 31st International Conference on Very Large Data Bases (VLDB)، الصفحات 553–564، سبتمبر 2005. [62] Andrew Lamb وMatt Fuller وRamakrishna Varadarajan وآخرون: «The Vertica Analytic Database: C-Store 7 Years Later»، Proceedings of the VLDB Endowment، المجلد 5، العدد 12، الصفحات 1790–1801، أغسطس 2012. [63] Julien Le Dem وNong Li: «Efficient Data Storage for Analytics with Apache Parquet 2.0»، في Hadoop Summit، San Jose، يونيو 2014. [64] Jim Gray وSurajit Chaudhuri وAdam Bosworth وآخرون: «Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals»، Data Mining and Knowledge Discovery، المجلد 1، العدد 1، الصفحات 29–53، مارس 2007. doi:10.1023/A:1009726021843

<!-- page 131 -->

<!-- page 132 -->

<table>
<tr><th></th><th></th><th></th></tr>
<tr><td>৬</td><td>-</td><td></td></tr>
</table>

<table>
<tr><th></th><th></th></tr>
<tr><td>n</td><td>w</td></tr>
<tr><td></td><td>Z</td></tr>
<tr><td></td><td>Q</td></tr>
<tr><td></td><td>O</td></tr>
<tr><td></td><td>u</td></tr>
<tr><td></td><td>2</td></tr>
<tr><td></td><td></td></tr>
<tr><td>-</td><td>ব</td></tr>
<tr><td></td><td>2</td></tr>
<tr><td></td><td></td></tr>
<tr><td>u</td><td></td></tr>
<tr><td>৩</td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>o</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>o</td></tr>
<tr><td></td><td></td></tr>
</table>

<!-- page 133 -->

## الترميز والتطور

كل شيء يتغير ولا شيء يبقى ثابتًا.

—Heraclitus of Ephesus، كما نقله Plato في Cratylus (360 ق.م.)

تتغير التطبيقات حتمًا مع مرور الوقت. تُضاف الميزات أو تُعدَّل عند إطلاق منتجات جديدة، أو عندما تصبح متطلبات المستخدم مفهومة على نحو أفضل، أو عندما تتغير الظروف التجارية. وفي الفصل 1 قدّمنا فكرة قابلية التطور (evolvability): ينبغي أن نهدف إلى بناء أنظمة تجعل التكيّف مع التغيير سهلًا (انظر «قابلية التطور: جعل التغيير سهلًا» في صفحة 21).

في معظم الحالات، يتطلب تغيير ميزات التطبيق أيضًا تغييرًا في البيانات التي يخزّنها: ربما يلزم التقاط حقل جديد أو نوع سجل جديد، أو ربما يلزم عرض البيانات الموجودة بطريقة جديدة.

نماذج البيانات التي ناقشناها في الفصل 2 لها طرق مختلفة للتعامل مع هذا التغيير. تفترض قواعد البيانات العلائقية عمومًا أن جميع البيانات الموجودة في قاعدة البيانات تتوافق مع schema واحد: ومع أن هذا الـ schema يمكن تغييره (عبر migrations لـ schema؛ أي عبارات ALTER)، فإن هناك schema واحدًا ساري المفعول في أي لحظة زمنية واحدة. وبالمقابل، لا تفرض قواعد البيانات «schema-on-read» (أي «بلا schema») أي schema، لذا يمكن أن تحتوي قاعدة البيانات على مزيج من تنسيقات البيانات الأقدم والأحدث التي كُتبت في أوقات مختلفة (انظر «مرونة الـ schema في النموذج المستندي» في صفحة 39).

وعندما يتغير تنسيق البيانات أو الـ schema، فإن غالبًا ما يلزم إجراء تغيير مقابل في كود التطبيق (على سبيل المثال، تضيف حقلًا جديدًا إلى سجل، فيبدأ كود التطبيق بقراءة ذلك الحقل وكتابته). لكن في تطبيق كبير، لا يمكن أن تحدث تغييرات الكود فورًا:

<!-- page 134 -->

• في التطبيقات من جهة الخادم (server-side)، قد ترغب في تنفيذ rolling upgrade (ترقية متدرجة، تُعرف أيضًا بـ staged rollout أو طرح متدرّج)، من خلال نشر الإصدار الجديد على بضعة عقد في كل مرة، والتحقق مما إذا كان الإصدار الجديد يعمل بسلاسة، ثم التقدم تدريجيًا عبر جميع العقد. ويتيح هذا نشر الإصدارات الجديدة دون توقف في الخدمة، ومن ثم يشجّع على إصدارات أكثر تكرارًا وقابلية تطور أفضل.
• في التطبيقات من جهة العميل (client-side)، أنت رهين إرادة المستخدم، الذي قد لا يثبّت التحديث إلا بعد مرور بعض الوقت.

وهذا يعني أن الإصدارات القديمة والجديدة من الكود، وتنسيقات البيانات القديمة والجديدة، قد تتعايش كلها في النظام في الوقت نفسه. ولكي يواصل النظام العمل بسلاسة، نحتاج إلى الحفاظ على التوافق في الاتجاهين:

## التوافق العكسي

يمكن للكود الأحدث قراءة البيانات التي كتبها الكود الأقدم.

## التوافق الأمامي

يمكن للكود الأقدم قراءة البيانات التي كتبها الكود الأحدث.

التوافق العكسي ليس صعبًا في العادة من الصالح: فأنت بصفتك مؤلف الكود الأحدث، تعرف تنسيق البيانات التي كتبها الكود الأقدم، ومن ثم يمكنك معالجتها صراحةً (أو، إذا لزم الأمر، بالاحتفاظ بالكود القديم ببساطة لقراءة البيانات القديمة). أما التوافق الأمامي فقد يكون أعقد، لأنه يتطلب من الكود الأقدم تجاهُل الإضافات التي أجراها إصدار أحدث من الكود.

في هذا الفصل سننظر في عدة تنسيقات لترميز البيانات، منها JSON وXML وProtocol Buffers وThrift وAvro. وعلى وجه الخصوص، سننظر في كيفية تعاملها مع تغييرات الـ schema، وكيف تدعم الأنظمة التي تحتاج فيها البيانات والكود القديم والجديد إلى التعايش. ثم سنناقش كيف تُستخدم هذه التنسيقات لتخزين البيانات وللاتصال: في خدمات الويب، Representational State Transfer (REST)، واستدعاءات الإجراءات عن بُعد (RPC)، وكذلك أنظمة تمرير الرسائل مثل actors وقوائم الرسائل.

## تنسيقات ترميز البيانات

تعمل البرامج عادةً مع البيانات في تمثيلين مختلفين على الأقل:

1. في الذاكرة، تُحفظ البيانات في كائنات (objects) وبنى (structs) وقوائم ومصفوفات وجداول تجزئة (hash tables) وأشجار، وما إلى ذلك. وقد خُصّصت هياكل البيانات هذه من أجل الوصول إليها والتعامل معها بكفاءة بواسطة المعالج (CPU) (عادةً باستخدام المؤشرات).
2. وعندما تريد كتابة البيانات إلى ملف أو إرسالها عبر الشبكة، عليك ترميزها في صورة نوع ما من تسلسل بايتات مكتنف بذاته (self-contained) (على سبيل المثال، مستند JSON). وبما أن المؤشر لا معنى له لأي عملية أخرى، فإن

<!-- page 135 -->

i. باستثناء بعض الحالات الخاصة، مثل بعض ملفات الذاكرة المُخطَّطة (memory-mapped files)، أو عند العمل مباشرة على البيانات المضغوطة (كما هو موضح في «ضغط الأعمدة» في صفحة 97).

ii. لاحظ أن الترميز (encoding) لا علاقة له بالتشفير (encryption). نحن لا نتناول التشفير في هذا الكتاب.

تمثيل تسلسل البايتات يبدو مختلفًا تمامًا عن هياكل البيانات التي تُستخدم عادةً في الذاكرة.i
