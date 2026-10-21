كلما أصبحت الحواسيب أقوى بكثير وأكثر ترابطًا عبر الشبكات، بدأت تُستخدم لأغراض أكثر تنوّعًا على نحو متزايد. والأمر لافت أن قواعد البيانات العلائقية تبيّن أنها تتعمّم جيدًا إلى حدٍّ كبير، إلى ما يتجاوز نطاقها الأصلي في معالجة بيانات الأعمال، لتتوسّع لتشمل مجموعة واسعة من حالات الاستخدام. وما زال معظم ما تراه على الويب اليوم مدعومًا بقواعد البيانات العلائقية، سواء كان النشر عبر الإنترنت، أو النقاش، أو شبكات التواصل الاجتماعي، أو التجارة الإلكترونية، أو الألعاب، أو تطبيقات العمل الإنتاجية المقدَّمة كخدمة (software-as-a-service)، أو ما هو أبعد من ذلك بكثير.

## ولادة NoSQL

والآن، في عقد 2010s، تُمثّل NoSQL أحدث محاولة للإطاحة بهيمنة النموذج العلائقي. واسم «NoSQL» لسوء الحظ، لأنه لا يشير فعليًا إلى أي تقنية بعينها— فقد كان مقصودًا في الأصل مجرد وسم (hashtag) على Twitter جذّاب لقاءٍ (meetup) حول قواعد البيانات غير العلائقية الموزّعة مفتوحة المصدر في عام 2009 [3]. ومع ذلك، أصاب المصطلح وترًا حساسًا وسارع انتشاره عبر مجتمع الشركات الناشئة على الويب وخارجه. وأصبح عدد من أنظمة قواعد البيانات المثيرة مرتبطًا الآن بوسم #NoSQL، وقد أُعيد تفسيره بأثر رجعي على أنه «Not Only SQL» [4].

هناك عدة قوى دافعة تقف خلف تبنّي قواعد بيانات NoSQL، منها:

• الحاجة إلى قابلية توسّع أكبر مما تستطيع قواعد البيانات العلائقية تحقيقه بسهولة، بما في ذلك مجموعات بيانات ضخمة جدًا أو write throughput عالٍ جدًا
• تفضيل واسع النطاق للبرمجيات الحرة مفتوحة المصدر على منتجات قواعد البيانات التجارية
• عمليات استعلام متخصصة لا يدعمها النموذج العلائقي دعمًا جيدًا
• الإحباط من صرامة schemas العلائقية، والرغبة في نموذج بيانات أكثر ديناميكية وتعبيرية [5]

تختلف المتطلبات بين التطبيقات المختلفة، وقد يكون أفضل اختيار للتقنية في حالة استخدام ما مختلفًا تمامًا عن أفضل اختيار في حالة استخدام أخرى. ومن ثمّ يبدو مرجَّحًا أن قواعد البيانات العلائقية ستستمر، في المستقبل القريب المنظور، في الاستخدام إلى جانب مجموعة واسعة من مختلف datastores غير العلائقية— وهي فكرة تُسمّى أحيانًا polyglot persistence [3].

## عدم التطابق بين النموذج الكائني والنموذج العلائقي

معظم تطوير التطبيقات اليوم يتم في لغات البرمجة الموجّهة للكائنات (object-oriented)، وهذا يؤدي إلى انتقاد شائع لنموذج بيانات SQL: إذا كانت البيانات مخزَّنة في جداول علائقية، فإن هناك حاجة إلى طبقة ترجمة مُحرجة (awkward) بين الكائنات في

<!-- page 52 -->

i. مصطلح مستعار من الإلكترونيات. لكل دائرة كهربائية impedance معيّن (مقاومة للتيار المتردد) عند مدخلاتها ومخرجاتها. وعندما توصل مخرجات دائرة واحدة بمدخلات دائرة أخرى، فإن نقل القدرة عبر الوصلة يبلغ أقصى صوره إذا تطابق impedance المخرجات مع impedance المدخلات في الدائرتين. ويمكن أن يؤدي عدم تطابق impedance إلى انعكاسات في الإشارة ومشكلات أخرى.

شيفرة التطبيق ونموذج قاعدة البيانات المكوَّن من الجداول والصفوف والأعمدة. ويُشار أحيانًا إلى الانفصال بين النموذجين بأنه impedance mismatch. i

أطر ORM (object-relational mapping) مثل ActiveRecord وHibernate تُقلّل حجم كود boilerplate المطلوب لطبقة الترجمة هذه، لكنها لا تستطيع أن تخفي بالكامل الاختلافات بين النموذجين.

على سبيل المثال، يوضّح الشكل 2-1 كيف يمكن التعبير عن سيرة ذاتية (résumé) (أي ملف تعريف على LinkedIn) في relational schema. ويمكن تعريف الملف الشخصي ككل بمعرّف فريد، user_id. وتظهر حقول مثل first_name وlast_name مرة واحدة بالضبط لكل مستخدم، لذا يمكن نمذجتها كأعمدة في جدول users. غير أن معظم الناس عملوا في أكثر من وظيفة واحدة طوال حياتهم المهنية (positions)، وقد يكون لدى الشخص عدد متفاوت من فترات التعليم وأي عدد من بيانات الاتصال. وهناك علاقة واحد-إلى-متعدد (one-to-many) من المستخدم إلى هذه العناصر، ويمكن تمثيلها بطرق متعددة:

• في نموذج SQL التقليدي (قبل SQL:1999)، التمثيل المُطبَّع (normalized) الأكثر شيوعًا هو وضع الوظائف (positions) والتعليم (education) ومعلومات الاتصال في جداول منفصلة، مع مرجع foreign key إلى جدول users، كما في الشكل 2-1.
• أضافت الإصدارات الأحدث من معيار SQL دعمًا لأنواع البيانات المهيكلة (structured) وبيانات XML؛ وقد سمح ذلك بتخزين البيانات متعددة القيم داخل صف واحد، مع دعم للاستعلام والفهرسة داخل تلك المستندات. وتدعم Oracle وIBM DB2 وMS SQL Server وPostgreSQL هذه الميزات بدرجات متفاوتة [6, 7]. كما تدعم عدةُ قواعد بيانات نوع بيانات JSON، ومنها IBM DB2 وMySQL وPostgreSQL [8].
• الخيار الثالث هو ترميز الوظائف والتعليم ومعلومات الاتصال في مستند JSON أو XML، وتخزينه في عمود نصي (text) في قاعدة البيانات، وترك التطبيق يفسّر بنيته ومحتواه. وفي هذا الإعداد، لا يمكنك عادةً استخدام قاعدة البيانات للاستعلام عن القيم داخل ذلك العمود المُرمَّز.

<!-- page 53 -->

<table>
<tr><th></th><th></th><th></th><th></th><th></th><th>جدول users</th></tr>
<tr><td>http://www.linkedin.com/in/williamhgates</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>user_id</td><td>first_name</td><td>last_name</td><td></td><td>summary</td></tr>
<tr><td>Bill Gates</td><td>251</td><td>Bill</td><td>Gates</td><td></td><td>شريك رئيسي لـ… مدوّن.</td></tr>
<tr><td>منطقة Seattle الكبرى | العمل الخيري</td><td></td><td>region_id</td><td>industry_id</td><td></td><td>photo_id</td></tr>
<tr><td></td><td></td><td>• us:91</td><td>131 \phi</td><td></td><td>57817532</td></tr>
<tr><td>الملخّص</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>شريك رئيسي في مؤسسة Bill &amp; Melinda Gates Foundation.</td><td></td><td></td><td>جدول regions</td><td></td><td>جدول industries</td></tr>
<tr><td>رئيس، Microsoft Corporation. قارئ نهم. مسافر متلهف. مدوّن نشط.</td><td>id</td><td colspan="2">/ region_name</td><td>id</td><td>industry_name</td></tr>
<tr><td></td><td>us:7</td><td colspan="2">منطقة Boston الكبرى</td><td>43</td><td>الخدمات المالية</td></tr>
<tr><td>الخبرة</td><td>us:91</td><td colspan="2">منطقة Seattle الكبرى</td><td>48</td><td>البناء</td></tr>
<tr><td>شريك رئيسي • مؤسسة Bill &amp; Melinda Gates Foundation</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>2000 – الحاضر</td><td></td><td></td><td></td><td>131</td><td>العمل الخيري</td></tr>
<tr><td>مؤسس مشارك، رئيس • Microsoft</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>1975 – الحاضر</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>جدول positions</td></tr>
<tr><td>التعليم</td><td>id</td><td>user_id</td><td>job_title</td><td></td><td>organization</td></tr>
<tr><td>Harvard University</td><td>458</td><td>• 251</td><td>شريك رئيسي</td><td colspan="2">Bill &amp; Melinda Gates F..</td></tr>
<tr><td>1973 – 1975</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Lakeside School, Seattle</td><td>457</td><td>• 251</td><td>مؤسس مشارك، رئيس</td><td></td><td>Microsoft</td></tr>
<tr><td>معلومات الاتصال</td><td></td><td></td><td></td><td></td><td>جدول education</td></tr>
<tr><td>المدونة: thegatesnotes.com Twitter: @BillGates</td><td>id</td><td>user_id</td><td>school_name</td><td></td><td>end start</td></tr>
<tr><td></td><td>807</td><td>• 251</td><td colspan="2">Harvard University</td><td>1975 1973</td></tr>
<tr><td></td><td>806</td><td>• 251</td><td></td><td>Lakeside School,</td><td>NULL NULL</td></tr>
<tr><td></td><td></td><td></td><td>Seattle</td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>جدول contact_info</td></tr>
<tr><td></td><td>id</td><td>user_id</td><td>type</td><td></td><td>url</td></tr>
<tr><td></td><td>155</td><td>• 251</td><td>blog</td><td colspan="2">http://thegatesnotes.com</td></tr>
<tr><td></td><td>156</td><td>• 251</td><td>twitter</td><td colspan="2">http://twitter.com/BillGates</td></tr>
</table>

الشكل 2-1. تمثيل ملف تعريف على LinkedIn باستخدام relational schema. صورة Bill Gates من طريق Wikimedia Commons، Ricardo Stuckert، Agência Brasil.

بالنسبة إلى بنية بيانات مثل سيرة ذاتية (résumé)، وهي في معظمها مستند مكتتفٍ بذاته، قد يكون تمثيل JSON مناسبًا إلى حدٍّ كبير: انظر المثال 2-1. وتتمتع JSON بجاذبية كونها أبسط بكثير من XML. وتدعم قواعد البيانات الموجّهة للمستندات (document-oriented) مثل MongoDB [9] وRethinkDB [10] وCouchDB [11] وEspresso [12] نموذج البيانات هذا.

مثال 2-1. تمثيل ملف تعريف على LinkedIn في صورة مستند JSON

{ "user_id": 251, "first_name": "Bill" "last_name": "Gates", "summary": "Co-chair of the Bill & Melinda Gates... Active blogger.", "region_id": "us:91", "industry_id": 131, "photo_url": "/p/7/000/253/05b/308dd6e.jpg",

<!-- page 54 -->

} "positions": [ {"job_title": "Co-chair", "organization": "Bill & Melinda Gates Foundation"}, {"job_title": "Co-founder, Chairman", "organization": "Microsoft"} ], "education": [ {"school_name": "Harvard University", "start": 1973, "end": 1975}, {"school_name": "Lakeside School, Seattle", "start": null, "end": null} ], "contact_info": { "blog": "http://thegatesnotes.com", "twitter": "http://twitter.com/BillGates" }

يرى بعض المطورين أن نموذج JSON يقلّل من عدم التطابق في impedance (impedance mismatch) بين شيفرة التطبيق وطبقة التخزين. غير أنه، كما سنرى في الفصل 4، هناك مشكلات أيضًا مع JSON كتنسيق ترميز للبيانات. وغالبًا ما يُستشهد غياب schema كميزة؛ وسنناقش هذا في «Schema flexibility in the document model» في صفحة 39.

