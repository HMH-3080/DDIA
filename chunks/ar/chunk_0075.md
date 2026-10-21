غير أن، بعد تقسيم الكتابات على مفاتيح مختلفة، تتعيّن الآن على أي قراءة أن تقوم بعمل إضافي، إذ عليها أن تقرأ البيانات من المفاتيح الـ100 كلها وتدمجها. وتتطلّب هذه التقنية أيضًا أعمال محاسبة إضافية: فلا معنى لإلحاق الرقم العشوائي إلا مع العدد الصغير من المفاتيح الساخنة (hot keys)؛ أما الغالبية العظمى من المفاتيح ذات write throughput المنخفض فسيكون ذلك عبئًا غير ضروري. وعليه، تحتاج أيضًا إلى بعض وسيلة لمتابعة المفاتيح التي يجري تقسيمها.

ربما في المستقبل، ستتمكّن أنظمة البيانات من اكتشاف أحمال العمل المُحدَّبة (skewed workloads) وتعويضها تلقائيًا؛ لكن في الوقت الحالي، عليك أن تفكّر في المفاضلات (trade-offs) الخاصة بتطبيقك.

<!-- page 228 -->

ii. إذا كانت قاعدة بياناتك لا تدعم سوى نموذج key-value، فقد يغريك أن تُنفّذ بنفسك secondary index من خلال إنشاء خريطة (mapping) من القيم إلى document IDs في كود التطبيق. وإن سلكت هذا الطريق، فعليك أن تتّخذ عناية بالغة لضمان بقاء فهارسك متّسقة مع البيانات الأساسية. ويمكن لـrace conditions ولأخطاء الكتابة المتقطّعة (intermittent write failures) (حيث حُفظت بعض التغييرات ولم تُحفظ أخرى) أن تسبّب بسهولة شديدة خروج البيانات عن التزامن— انظر «الحاجة إلى transactions متعددة الكائنات» في صفحة 231.

## Partitioning والفهارس الثانوية

تعتمد مخططات الـpartitioning التي ناقشناها حتى الآن على نموذج بيانات key-value. وإذا لم يُطالَب بالسجلات (records) إلا عبر مفتاحها الأساسي، فيمكننا تحديد الـpartition من ذلك المفتاح واستخدامه لتوجيه طلبات القراءة والكتابة إلى الـpartition المسؤولة عن ذلك المفتاح.

يصبح الموقف أكثر تعقيدًا إذا تطرّرت secondary indexes في الأمر (وانظر أيضًا «هياكل الفهرسة الأخرى» في صفحة 85). فـsecondary index لا يحدّد سجلًا (record) بصورة فريدة عادةً، بل هو وسيلة للبحث عن مواضع قيمة معيّنة: اعثر على كل الإجراءات التي قام بها المستخدم 123، وعلى كل المقالات التي تحتوي الكلمة hogwash، وعلى كل السيارات التي لونها أحمر، وهكذا.

تُعدّ secondary indexes من خبز وزبد قواعد البيانات العلائقية، وهي شائعة أيضًا في قواعد بيانات المستندات (document databases). وقد تجنّبت كثير من مخازن key-value (مثل HBase وVoldemort) الفهارس الثانوية بسبب التعقيد الإضافي الذي يُضيفه تنفيذها، لكن بعضها (مثل Riak) بدأ بإضافتها لأنها مفيدة جدًا لنمذجة البيانات (data modeling). وأخيرًا، فإن secondary indexes هي raison d'être لخوادم البحث مثل Solr وElasticsearch.

المشكلة في secondary indexes أنها لا تنطبق بانتظام على الـpartitions. وهناك منهجان رئيسيان لتقسيم قاعدة بيانات ذات secondary indexes: التقسيم بحسب المستند (document-based partitioning) والتقسيم بحسب الـterm (term-based partitioning).

## Partitioning الفهارس الثانوية حسب المستند

على سبيل المثال، تخيّل أنك تُدير موقعًا لبيع السيارات المستعملة (كما هو موضّح في الشكل 6-4). ولكل إعلان معروض ID فريد— لنسمّه document ID— وتُقسِّم قاعدة البيانات بحسب document ID (مثلًا، IDs من 0 إلى 499 في الـpartition 0، ومن 500 إلى 999 في الـpartition 1، إلخ).

تريد أن تسمح للمستخدمين بالبحث عن السيارات، مع تمكينهم من التصفية حسب اللون (color) وحسب الصنع (make)، لذا تحتاج إلى secondary index على color وعلى make (في قاعدة بيانات المستندات تكون هذه حقولًا (fields)، وفي قاعدة البيانات العلائقية تكون أعمدة (columns)). وإذا كنت قد عرّفت الفهرس، فيمكن لقاعدة البيانات أن تنفّذ الفهرسة تلقائيًا.ii وعلى سبيل المثال، كلما أُضيفت سيارة حمراء إلى قاعدة البيانات، أضافها الـpartition تلقائيًا إلى قائمة document IDs الخاصة بمدخل الفهرس color:red.

<!-- page 229 -->

Partition 0

## Partition 1

<table>
<tr><th colspan="2">فهرس المفتاح الأساسي</th><th colspan="2">فهرس المفتاح الأساسي</th></tr>
<tr><td colspan="2">191 → (color:“red”,</td><td colspan="2">515 → {color:”silver”, make:“Ford”, location:”Milpitas”)</td></tr>
<tr><td colspan="2">214 → {color:“black”, make:“Dodge”, location:“San Jose”}</td><td colspan="2">768 → (color:“red”,</td></tr>
<tr><td colspan="2">306 → (color: “red”,</td><td colspan="2">893 → {color:“silver”, make:“Audi”, location:“Santa Clara”)</td></tr>
<tr><td colspan="2">secondary indexes (مقسّمة بحسب المستند)</td><td colspan="2">secondary indexes (مقسّمة بحسب المستند)</td></tr>
<tr><td>color:black</td><td>→ [214]</td><td>color:black</td><td>→ 0</td></tr>
<tr><td>color:red</td><td>→ [191, 306] &lt;{</td><td>- color:red</td><td>→ [768]</td></tr>
<tr><td>color:yellow</td><td>→ []</td><td>color:silver</td><td>→ [515, 893]</td></tr>
<tr><td colspan="2">make:Dodge → [214]</td><td>make:Audi</td><td>→ [893]</td></tr>
<tr><td>make:Ford</td><td>→ [306]</td><td>make:Ford</td><td>→ [515]</td></tr>
<tr><td>make:Honda</td><td>→ [191]</td><td>make:Volvo</td><td>→ [768]</td></tr>
<tr><td></td><td></td><td colspan="2">قراءة scatter/gather من جميع الـpartitions</td></tr>
<tr><td></td><td></td><td colspan="2">«أبحث عن سيارة حمراء»</td></tr>
</table>

الشكل 6-4. Partitioning الفهارس الثانوية حسب المستند.

في منهج الفهرسة هذا، كل partition منفصلة تمامًا: فكل partition تحتفظ بفهارسها الثانوية الخاصة، التي تغطّي المستندات الموجودة في تلك الـpartition وحدها. ولا تعبأ بما هو مخزَّن في الـpartitions الأخرى. وكلما احتجت الكتابة في قاعدة البيانات— لإضافة مستند أو إزالته أو تحديثه— فإنك لا تحتاج إلا إلى التعامل مع الـpartition التي تحوي document ID الذي تكتب إليه. ولهذا السبب يُعرف الفهرس المُقسَّم بحسب المستند أيضًا بـlocal index (على النقيض من global index، الموصوف في القسم التالي).

غير أن القراءة من فهرس مُقسَّم بحسب المستند تتطلّب حذرًا: فإذ لم تفعل شيئًا خاصًا بمعرّفات المستندات (document IDs)، فلا سبب لأن تكون كل السيارات ذات اللون المعيّن أو الصنع المعيّن في الـpartition نفسها. وفي الشكل 6-4، تظهر السيارات الحمراء في كلٍّ من الـpartition 0 والـpartition 1. وعليه، إن أردت البحث عن السيارات الحمراء، عليك إرسال الاستعلام إلى جميع الـpartitions، ودمج كل النتائج التي تعود إليك.

تُعرف هذه الطريقة في الاستعلام عن قاعدة بيانات مُقسَّمة أحيانًا بـscatter/gather، وقد تجعل استعلامات القراءة على secondary indexes مكلفةً إلى حدٍّ كبير. وحتى لو أُرسلت الاستعلامات إلى الـpartitions على التوازي، فإن scatter/gather عرضة لتضخيم tail latency (انظر «الـpercentiles في الممارسة العملية» في صفحة 16). ومع ذلك، فهي مستخدَمة على نطاق واسع: فMongoDB وRiak [15] وCassandra [16] وElasticsearch [17] وSolrCloud [18] وVoltDB [19] تستخدم جميعها فهارس ثانوية مُقسَّمة بحسب المستند. ويوصي معظم بائعي قواعد البيانات بأن تصمّم مخطط الـpartitioning بحيث يمكن تقديم استعلامات secondary index من partition واحدة، لكن ذلك ليس ممكنًا دائمًا، ولا سيما حين تستخدم عدة secondary indexes في استعلام واحد (مثل تصفية السيارات حسب اللون وحسب الصنع في الوقت نفسه).

<!-- page 230 -->

## Partition 0

## Partition 1

<table>
<tr><th colspan="2">فهرس المفتاح الأساسي</th><th></th><th colspan="2">فهرس المفتاح الأساسي</th></tr>
<tr><td>191 → (color:“red”,</td><td></td><td>make:“Honda”, location:“Palo Alto”}</td><td colspan="2">515 → {color:”silver”, make:“Ford”, location:”Milpitas”)</td></tr>
<tr><td colspan="3">214 → {color:"black”, make:“Dodge”, location:“San Jose”}</td><td colspan="2">768 → (color:”red”,</td></tr>
<tr><td colspan="2">306 → (color: “red”,</td><td>location:“Sunnyvale”} make:“Ford”,</td><td colspan="2">893 → (color:”silver”, make:“Audi”, location:”Santa Clara”) •</td></tr>
<tr><td></td><td></td><td></td><td></td><td>-</td></tr>
<tr><td colspan="3">secondary indexes (مقسّمة بحسب الـterm)</td><td colspan="2">\¿secondary indexes (مقسّمة بحسب الـterm)</td></tr>
<tr><td>color:black</td><td>→ [214]</td><td></td><td>color:silver</td><td>→ [515, 893]</td></tr>
<tr><td>color:red</td><td colspan="2">→ [191, 306, 768] «</td><td>color.yellow</td><td>→ []</td></tr>
<tr><td>make:Audi</td><td>→ [893] (</td><td>----</td><td>make:Honda</td><td>→ [191]</td></tr>
<tr><td>make:Do</td><td>→ [214]</td><td></td><td>make:Volvo</td><td>→ [768]</td></tr>
<tr><td>make:Ford</td><td>[306, 515]</td><td></td><td></td><td></td></tr>
</table>

«أبحث عن سيارة حمراء»

الشكل 6-5. Partitioning الفهارس الثانوية حسب المصطلح.

## Partitioning الفهارس الثانوية حسب المصطلح

