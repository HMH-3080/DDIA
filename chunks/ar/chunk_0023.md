وكما هو معتاد في لغات الاستعلام التصريحية، فأنت لا تحتاج إلى تحديد تفاصيل التنفيذ هذه عند كتابة الاستعلام: فمُحسِّن الاستعلامات (query optimizer) يختار تلقائيًا الاستراتيجية التي يُتوقَّع أن تكون الأكثر كفاءة، لتتمكّن من متابعة كتابة بقية تطبيقك.

## استعلامات الرسوم البيانية في SQL

أشار المثال 2-2 إلى أن بيانات الرسوم البيانية يمكن تمثيلها في قاعدة بيانات علائقية. لكن إذا وضعنا بيانات الرسوم البيانية في بنية علائقية، فهل يمكننا أيضًا الاستعلام عنها باستخدام SQL؟

الجواب هو نعم، لكن مع بعض الصعوبة. في قاعدة البيانات العلائقية، عادةً ما تعرف مسبقًا الـjoins التي تحتاج إليها في استعلامك. أما في الاستعلام على رسم بياني، فقد تحتاج إلى

<!-- page 76 -->

أن تعبر عددًا متغيّرًا من الحواف (edges) قبل أن تجد الرأس (vertex) الذي تبحث عنه— أي أن عدد الـjoins غير محدَّد مسبقًا.

في مثالنا، يحدث ذلك في القاعدة () -[:WITHIN*0..]-> () في استعلام Cypher. قد يشير حاف LIVES_IN الخاص بشخص ما إلى أي نوع من المواقع: شارع، أو مدينة، أو حيّ، أو منطقة، أو ولاية، إلخ. فقد تكون المدينة WITHIN منطقة، والمنطقة WITHIN ولاية، والولاية WITHIN بلدًا، إلخ. وقد يشير حاف LIVES_IN مباشرةً إلى رأس الموقع الذي تبحث عنه، أو قد يفصله عنك عدة مستويات في التسلسل الهرمي للمواقع (location hierarchy).

في Cypher، تُعبِّر :WITHIN*0.. عن هذه الحقيقة بإيجاز شديد: فهي تعني «اتبع حاف WITHIN، صفرًا من المرات أو أكثر». وهي تشبه عامل * في تعبير نمطي (regular expression).

منذ SQL:1999، يمكن التعبير عن فكرة مسارات العبور متغيّرة الطول في الاستعلام باستخدام ما يُعرف بـrecursive common table expressions (صيغة WITH RECURSIVE). ويعرض المثال 2-5 الاستعلام نفسه— أي إيجاد أسماء الأشخاص الذين انتقلوا من الولايات المتحدة إلى أوروبا— معبَّرًا عنه في SQL باستخدام هذه التقنية (مدعومة في PostgreSQL وIBM DB2 وOracle وSQL Server). غير أن الصياغة مرهقة جدًّا بالمقارنة مع Cypher.

مثال 2-5. الاستعلام نفسه الموجود في المثال 2-4، معبَّرًا عنه في SQL باستخدام recursive common table expressions

WITH RECURSIVE
  -- in_usa is the set of vertex IDs of all locations within the United States
  in_usa(vertex_id) AS (
      SELECT vertex_id FROM vertices WHERE properties->>'name' = 'United States'
    UNION
      SELECT edges.tail_vertex FROM edges
        JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
        WHERE edges.label = 'within'
  ),
  -- in_europe is the set of vertex IDs of all locations within Europe
  in_europe(vertex_id) AS (
      SELECT vertex_id FROM vertices WHERE properties->>'name' = 'Europe'
    UNION
      SELECT edges.tail_vertex FROM edges
        JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
        WHERE edges.label = 'within'
  ),
  -- born_in_usa is the set of vertex IDs of all people born in the US
  born_in_usa(vertex_id) AS (
    SELECT edges.tail_vertex FROM edges
      JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
      WHERE edges.label = 'born_in'
  ),
  -- lives_in_europe is the set of vertex IDs of all people living in Europe
  lives_in_europe(vertex_id) AS (
    SELECT edges.tail_vertex FROM edges
      JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
      WHERE edges.label = 'lives_in'
  )
SELECT vertices.properties->>'name'
FROM vertices
-- join to find those people who were both born in the US *and* live in Europe
JOIN born_in_usa     ON vertices.vertex_id = born_in_usa.vertex_id
JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;

أولًا ابحث عن الرأس الذي قيمة خاصية name فيه هي "United States"، واجعله العنصر الأول في مجموعة الرؤوس in_usa. اتبع جميع حواف within الداخلة من الرؤوس الموجودة في المجموعة in_usa، وأضفها إلى المجموعة نفسها، حتى تُزار جميع حواف within الداخلة. افعل الشيء نفسه بدءًا من الرأس الذي قيمة خاصية name فيه هي "Europe"، وابنِ مجموعة الرؤوس in_europe. لكل رأس من الرؤوس في المجموعة in_usa، اتبع حواف born_in الداخلة للعثور على أشخاص وُلدوا في بعض المكان داخل الولايات المتحدة. وعلى نحو مماثل، لكل رأس من الرؤوس في المجموعة in_europe، اتبع حواف lives_in الداخلة للعثور على أشخاص يعيشون في أوروبا. وأخيرًا، قاطع مجموعة الأشخاص المولودين في الولايات المتحدة مع مجموعة الأشخاص الذين يعيشون في أوروبا، عبر الـjoin بينهما.

إذا كان الاستعلام نفسه يمكن كتابته في 4 أسطر في لغة استعلام واحدة، لكنه يتطلب 29 سطرًا في لغة أخرى، فإن هذا لا يثبت سوى أن نماذج البيانات المختلفة مصمَّمة لتلبية حالات الاستخدام المختلفة. ومن المهم أن تختار نموذج بيانات مناسبًا لتطبيقك.

## Triple-Stores وSPARQL

نموذج الـtriple-store مكافئ في الغالب لنموذج الـproperty graph، مع استخدام كلمات مختلفة لوصف الأفكار نفسها. ومع ذلك فإن مناقشته تستحق العناء، إذ توجد أدوات ولغات مختلفة للـtriple-stores يمكن أن تكون إضافات مفيدة إلى صندوق أدواتك لبناء التطبيقات.

في الـtriple-store، تُخزَّن كل المعلومات في صورة عبارات ثلاثية الأجزاء بسيطة جدًا: (subject, predicate, object). فمثلًا، في الـtriple (Jim, likes, bananas)، يكون Jim هو الفاعل (subject)، وlikes هو المسند (predicate) (الفعل)، وbananas هو المفعول (object).

<!-- page 78 -->

فاعل الـtriple يكافئ رأسًا (vertex) في رسم بياني. أما المفعول (object) فأحد أمرين:

1. قيمة في نوع بيانات أولي (primitive datatype)، مثل سلسلة نصية أو رقم. في هذه الحالة، يكافئ مسند الـtriple ومفعوله مفتاح الخاصية (property) وقيمتها على رأس الفاعل. فمثلًا، (lucy, age, 33) تشبه رأسًا lucy له properties من الشكل {"age":33}.
2. رأس آخر في الرسم البياني. في هذه الحالة، يكون المسند حافًّا في الرسم البياني، ويكون الفاعل هو الرأس الخلفي (tail vertex)، ويكون المفعول هو الرأس الأمامي (head vertex). فمثلًا، في (lucy, marriedTo, alain) يكون الفاعل والمفعول، lucy وalain، رأسين، ويكون المسند marriedTo هو تسمية (label) الحاف الذي يصل بينهما.

يعرض المثال 2-6 البيانات نفسها الواردة في المثال 2-3، مكتوبة في صورة triples بصيغة تُدعى Turtle، وهي مجموعة جزئية من Notation3 (N3) [39].

مثال 2-6. مجموعة جزئية من بيانات الشكل 2-5، معبَّرة في صورة triples بصيغة Turtle

@prefix : <urn:example:>. _:lucy _:lucy _:lucy a :Person. :name "Lucy". :bornIn _:idaho. _:idaho _:idaho _:idaho a :name :type :Location. "Idaho". "state". _:idaho :within _:usa. _:usa _:usa _:usa _:usa a :name :Location. "United States". :type "country". :within _:namerica. _:namerica a :Location. _:namerica :name _:namerica :type "North America". "continent".

في هذا المثال، تُكتب رؤوس الرسم البياني في صورة _:someName. وهذا الاسم لا يعني شيئًا خارج هذا الملف؛ فهو موجود فقط لأننا لولا ذلك لما عرفنا أي الـtriples تشير إلى الرأس نفسه. وحين يمثّل المسند حافًّا، يكون المفعول رأسًا، كما في _:idaho :within _:usa. وحين يكون المسند خاصية (property)، يكون المفعول قيمة نصية (string literal)، كما في _:usa :name "United States".

