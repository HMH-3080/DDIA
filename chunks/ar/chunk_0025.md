• في CODASYL، كانت لقاعدة البيانات schema تحدّد أي نوع سجل (record type) يمكن أن يتداخل داخل أي نوع سجل آخر. وفي قاعدة بيانات الرسوم البيانية (graph database)، لا يوجد مثل هذا التقييد: يمكن لأي vertex أن يكون له edge إلى أي vertex آخر. وهذا يمنح التطبيقات مرونة أكبر بكثير للتكيّف مع المتطلبات المتغيّرة.
• في CODASYL، لم تكن هناك سوى طريقة واحدة للوصول إلى سجل بعينه، وهي المرور عبر أحد access paths المؤدية إليه. وفي قاعدة بيانات الرسوم البيانية، يمكنك الإشارة مباشرةً إلى أي vertex بمعرّفه الفريد (unique ID)، أو يمكنك استخدام index للعثور على الـvertices التي تحمل قيمة بعينها.
• في CODASYL، كانت أبناء السجل مجموعةً مرتَّبة، لذا كان على قاعدة البيانات أن تحافظ على ذلك الترتيب (ولكان له عواقب على تخطيط التخزين (storage layout))، وكان على التطبيقات التي تُدرج سجلات جديدة في قاعدة البيانات أن تشغل نفسها بمواضع السجلات الجديدة في هذه المجموعات. وفي قاعدة بيانات الرسوم البيانية، ليست الـvertices والـedges مرتَّبة (لا يمكنك فرز النتائج إلا عند إجراء استعلام).
• في CODASYL، كانت جميع الاستعلامات أمرّية (imperative)، صعبة الكتابة ومنكوسة بسهولة بفعل التغييرات في الـschema. وفي قاعدة بيانات الرسوم البيانية، يمكنك كتابة الـtraversal في كود أمرّي إن أردت، لكن معظم قواعد بيانات الرسوم البيانية تدعم أيضًا لغات استعلام تصريحية (declarative) عالية المستوى مثل Cypher أو SPARQL.

## الأساس: Datalog

Datalog لغة أقدم بكثير من SPARQL أو Cypher، فقد دُرست على نطاق واسع من قبل الباحثين الأكاديميين في الثمانينيات [44, 45, 46]. وهي أقلّ شهرة بين مهندسي البرمجيات، لكنها مع ذلك مهمة، لأنها توفّر الأساس الذي بُنيت عليه لغات الاستعلام اللاحقة.

في الواقع، تُستخدم Datalog في بضعة أنظمة بيانات: على سبيل المثال، هي لغة الاستعلام في Datomic [40]، وCascalog [47] هي تنفيذ لـDatalog للاستعلام عن مجموعات بيانات كبيرة في Hadoop.viii

<!-- page 83 -->

نموذج بيانات Datalog مشابه لنموذج الـtriple-store، مع تعميم طفيف. وبدلًا من كتابة الـtriple بالشكل (subject, predicate, object)، نكتبها بالشكل predicate(subject, object). ويوضح المثال 2-10 كيف نكتب بيانات مثالنا في Datalog.

المثال 2-10. مجموعة جزئية من بيانات الشكل 2-5، معبَّرة كوقائع Datalog

name(namerica, 'North America'). type(namerica, continent). name(usa, 'United States'). type(usa, country). within(usa, namerica). name(idaho, 'Idaho'). type(idaho, state). within(idaho, usa). name(lucy, 'Lucy'). born_in(lucy, idaho).

والآن بعد أن عرّفنا البيانات، يمكننا كتابة الاستعلام نفسه كما سبق، كما هو موضَّح في المثال 2-11. يبدو مختلفًا قليلًا عن نظيره في Cypher أو SPARQL، لكن لا تدع ذلك يُثبطك. Datalog مجموعة جزئية من Prolog، وقد تكون صادفتها من قبل إن كنت قد درست علوم الحاسوب.

المثال 2-11. الاستعلام نفسه الموجود في المثال 2-4، معبَّرًا عنه في Datalog

within_recursive(Location, Name) :- name(Location, Name). /* Rule 1 */ within_recursive(Location, Name) :- within(Location, Via), /* Rule 2 */ within_recursive(Via, Name). migrated(Name, BornIn, LivingIn) :- name(Person, Name), /* Rule 3 */ born_in(Person, BornLoc), within_recursive(BornLoc, BornIn), lives_in(Person, LivingLoc), within_recursive(LivingLoc, LivingIn).

?- migrated(Who, 'United States', 'Europe'). /* Who = 'Lucy'. */

تبدأ Cypher وSPARQL مباشرةً بـSELECT، أما Datalog فتاخذ خطوةً صغيرة في كل مرة. نعرّف قواعد تخبر قاعدة البيانات بpredicates جديدة: هنا نعرّف predicate جديدين، هما within_recursive وmigrated. وهذه الـpredicates ليست triples مخزَّنة في قاعدة البيانات، بل هي مشتقّة من البيانات أو من قواعد أخرى. ويمكن للقواعد أن تشير إلى قواعد أخرى، تمامًا كما يمكن للدوال أن تستدعي دوال أخرى أو أن تستدعي نفسها بشكل متكرر (recursively). وهكذا يمكن بناء الاستعلامات المعقّدة قطعةً صغيرة تلو الأخرى.

<!-- page 84 -->

في القواعد، الكلمات التي تبدأ بحرف لاتيني كبير هي متغيّرات (variables)، وتُطابَق الـpredicates كما في Cypher وSPARQL. على سبيل المثال، name(Location, Name) يطابق الـtriple name(namerica, 'North America') مع ربط المتغيّرات Location = namerica وName = 'North America'.

تُطبَّق القاعدة إذا استطاع النظام أن يجد مطابقة لكل الـpredicates الموجودة في الجانب الأيمن من المعامل :-. وحين تُطبَّق القاعدة، فكأن الجانب الأيسر من :- قد أُضيف إلى قاعدة البيانات (مع استبدال المتغيّرات بالقيم التي طابقتها).

إحدى الطرق الممكنة لتطبيق القواعد هي:

1. name(namerica, 'North America') موجود في قاعدة البيانات، لذا تنطبق القاعدة 1. وهي تولّد within_recursive(namerica, 'North America').
2. within(usa, namerica) موجود في قاعدة البيانات، وولّدت الخطوة السابقة within_recursive(namerica, 'North America')، لذا تنطبق القاعدة 2. وهي تولّد within_recursive(usa, 'North America').
3. within(idaho, usa) موجود في قاعدة البيانات، وولّدت الخطوة السابقة within_recursive(usa, 'North America')، لذا تنطبق القاعدة 2. وهي تولّد within_recursive(idaho, 'North America').

بتطبيق القاعدتين 1 و2 تكرارًا، يمكن للـpredicate within_recursive أن يخبرنا بكل المواقع الموجودة في أمريكا الشمالية (أو بأي اسم موقع آخر) الموجودة في قاعدة بياناتنا. وهذا الإجراء موضَّح في الشكل 2-6.

<table>
<tr><th>بعد</th><th>تطبيق القاعدة 1:</th><th colspan="2">بعد تطبيق القاعدة 2 مرة</th><th colspan="2">بعد تطبيق القاعدة 2 مرتين:</th></tr>
<tr><td>within</td><td></td><td>within_recursiv</td><td></td><td>within_recursive</td><td></td></tr>
<tr><td></td><td></td><td>ocation</td><td>Na</td><td>Location</td><td>Name</td></tr>
<tr><td>namer</td><td>orth</td><td>america</td><td>North A</td><td>namerica</td><td>North America</td></tr>
<tr><td></td><td>nited States</td><td></td><td>North A</td><td>isa</td><td>North America</td></tr>
<tr><td></td><td>ho</td><td>sa</td><td>nited</td><td>daho</td><td>North America</td></tr>
<tr><td></td><td></td><td>dah</td><td></td><td></td><td>United States</td></tr>
<tr><td></td><td></td><td>daho</td><td>d</td><td>laho</td><td>United States</td></tr>
<tr><td></td><td></td><td></td><td></td><td>daho</td><td>Idaho</td></tr>
<tr><td></td><td></td><td></td><td>within(idaho, usa)</td><td></td><td></td></tr>
</table>

الشكل 2-6. تحديد أن Idaho تقع في أمريكا الشمالية، باستخدام قواعد Datalog من المثال 2-11.

والآن تستطيع القاعدة 3 أن تجد أشخاصًا وُلدوا في موقع ما BornIn ويعيشون في موقع ما LivingIn. وبالاستعلام بـBornIn = 'United States' وLivingIn = 'Europe'، وترك الشخص كمتغيّر Who، نطلب من نظام Datalog أن يعرف ما هي القيم التي يمكن أن تظهر للمتغيّر Who. فنحصل في النهاية على الإجابة نفسها كما في استعلامات Cypher وSPARQL السابقة.

<!-- page 85 -->

يتطلب نهج Datalog نوعًا مختلفًا من التفكير عن لغات الاستعلام الأخرى التي ناقشناها في هذا الفصل، لكنه نهج قوي جدًا، إذ يمكن دمج القواعد وإعادة استخدامها في استعلامات مختلفة. وهو أقلّ ملاءمة للاستعلامات البسيطة التي تُكتب مرة واحدة، لكنه يتعامل بشكل أفضل إذا كانت بياناتك معقّدة.

## ملخّص

نماذج البيانات موضوع ضخم، وفي هذا الفصل أخذنا لمحة سريعة على تشكيلة واسعة من النماذج المختلفة. لم يتّسع لنا المجال للدخول في كل تفاصيل كل نموذج، لكننا نأمل أن يكون هذا العرض كافيًا لإثارة شهيتك لمعرفة المزيد عن النموذج الذي يناسب متطلبات تطبيقك أكثر من غيره.

تاريخيًا، بدأت البيانات تُمثَّل على هيئة شجرة واحدة كبيرة (النموذج الهرمي)، لكن ذلك لم يكن جيدًا لتمثيل العلاقات many-to-many، لذا اخترع النموذج العلائقي لحل تلك المشكلة. وفي الآونة الأخيرة، اكتشف المطورون أن بعض التطبيقات لا تناسبها النموذج العلائقي أيضًا. وقد تشعّبت مخازن البيانات غير العلائقية “NoSQL” الجديدة في اتجاهين رئيسيين:

