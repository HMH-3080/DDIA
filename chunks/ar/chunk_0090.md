<table>
<tr><th>Alice:</th><th></th><th></th><th>Bob:</th></tr>
<tr><td>^ begin transaction</td><td></td><td></td><td>o begin transaction</td></tr>
<tr><td></td><td>name</td><td>on call</td><td></td></tr>
<tr><td>o currently_on_call = (</td><td>Alice</td><td>true</td><td>o currently_on_call = (</td></tr>
<tr><td>select count(*) from doctors</td><td>Bob</td><td>true</td><td>select count(*) from doctors</td></tr>
<tr><td>where on_call = true</td><td>Carol</td><td>false</td><td>where on_call = true</td></tr>
<tr><td>and shift_id = 1234</td><td></td><td></td><td>and shift_id = 1234</td></tr>
<tr><td>)</td><td></td><td></td><td>)</td></tr>
<tr><td>الآن currently_on_call = 2</td><td></td><td></td><td>الآن currently_on_call = 2</td></tr>
<tr><td>o if (currently_on_call &gt;= 2) {</td><td></td><td></td><td></td></tr>
<tr><td>update doctors</td><td></td><td></td><td></td></tr>
<tr><td>Alice set on_call = false</td><td>false</td><td></td><td></td></tr>
<tr><td>where name = ‘Alice’</td><td></td><td></td><td></td></tr>
<tr><td>and shift_id = 1234</td><td></td><td></td><td>o if (currently_on_call &gt;=2){</td></tr>
<tr><td>J</td><td></td><td></td><td>update doctors</td></tr>
<tr><td></td><td></td><td>false Bob</td><td>set on_call = false</td></tr>
<tr><td></td><td></td><td></td><td>where name = ‘Bob’</td></tr>
<tr><td>o commit transaction</td><td></td><td></td><td></td></tr>
<tr><td></td><td>name</td><td>on_call</td><td>and shift_id = 1234</td></tr>
<tr><td></td><td></td><td></td><td>J</td></tr>
<tr><td></td><td>Alice</td><td>false</td><td></td></tr>
<tr><td></td><td>Bob</td><td>false</td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td>o commit transaction</td></tr>
<tr><td></td><td>Carol</td><td>false</td><td></td><td></td></tr>
</table>

الشكل 7-8. مثال على write skew يسبب خللًا في التطبيق.

في كل transaction، يتحقق تطبيقك أولًا من وجود طبيبين أو أكثر في المناوبة (on call) حاليًا؛ وإذا كان الأمر كذلك، فإنه يفترض أن من الآمن أن ينزل أحد الأطباء من المناوبة. وبما أن قاعدة البيانات تستخدم snapshot isolation، فإن كلا الفحصين يُعيد 2، فتنتقل كلتا الـ transactions إلى المرحلة التالية. تُحدِّث Alice سجلها الخاص لتُخرج نفسها من المناوبة، ويحدّث Bob سجله الخاص على نحو مماثل. تُتعتمد (commit) كلتا الـ transactions، وأصبح الآن لا يوجد أي طبيب في المناوبة. وقد خُرق شرطك الخاص بوجود طبيب واحد على الأقل في المناوبة.

## توصيف write skew

هذه الشذوذ يُسمّى write skew [28]. وهو ليس dirty write ولا lost update، لأن الـ transactionين تُحدِّثان كائنين مختلفين (سجلَّي on_call الخاصَّين بـ Alice وBob على التوالي). ومن غير الواضح إلى هذا الحد أن تعارضًا قد وقع هنا، لكنه بالتأكيد race condition: فلو كانت الـ transactionان قد نُفِّذتا واحدة تلو الأخرى، لما مُنع الطبيب الثاني من النزول من المناوبة.

<!-- page 270 -->

لم يكن السلوك الشاذ ممكنًا إلا لأن الـ transactionين نُفِّذتا بالتزامن.

يمكنك أن تنظر إلى write skew على أنها تعميم لمشكلة lost update. ويمكن أن يحدث write skew إذا قرأت transactionان الكائنات نفسها، ثم حدّثتا بعضها من تلك الكائنات (قد تُحدِّث transactionان مختلفتان كائنات مختلفة). وفي الحالة الخاصة التي تُحدِّث فيها الـ transactionان مختلفتان الكائن نفسه، تحصل على شذوذ dirty write أو lost update (بناءً على التوقيت).

رأينا أن هناك طرقًا مختلفة لمنع lost update. ومع write skew، تكون خياراتنا أكثر تقييدًا:

• العمليات الذرّية على كائن واحد (atomic single-object operations) لا تساعد، لأن عدة كائنات مشمولة هنا.
• الكشف التلقائي عن lost update الذي تجده في بعض تطبيقات snapshot isolation لا يساعد أيضًا للأسف: write skew لا يُكتشف تلقائيًا في repeatable read الخاص بـ PostgreSQL، ولا في repeatable read الخاص بـ MySQL/InnoDB، ولا في serializable الخاص بـ Oracle، ولا في مستوى snapshot isolation الخاص بـ SQL Server [23]. ويمنع write skew تلقائيًا يتطلّب عزلة serializable حقيقية (true serializable isolation) (انظر «Serializability» في صفحة 251).
• تسمح بعض قواعد البيانات لك بتهيئة قيود (constraints)، التي يتم بعد ذلك فرضها بواسطة قاعدة البيانات (مثلًا قيود التفرّد (uniqueness)، أو قيود foreign key، أو قيود على قيمة بعينها). لكن، لكي تحدّد أن على الأقل طبيبًا واحدًا يجب أن يكون في المناوبة، ستحتاج إلى قيد يتضمّن عدة كائنات. معظم قواعد البيانات لا تملك دعمًا مدمجًا لمثل هذه القيود، لكن قد تتمكّن من تنفيذها باستخدام triggers أو materialized views، بحسب قاعدة البيانات [42].
• إذا كنت لا تستطيع استخدام مستوى عزل serializable، فإن الخيار الثاني الأفضل في هذه الحالة هو على الأرجح أن تقفل صراحةً الصفوف التي تعتمد عليها الـ transaction. وفي مثال doctors، يمكنك كتابة شيء مثل التالي:

BEGIN TRANSACTION;

SELECT * FROM doctors WHERE on_call = true AND shift_id = 1234 FOR UPDATE;

UPDATE doctors SET on_call = false WHERE name = 'Alice' AND shift_id = 1234;

COMMIT;

كما في السابق، يأمرك FOR UPDATE قاعدة البيانات بأن تقفل كل الصفوف التي يُعيدها هذا الاستعلام.

<!-- page 271 -->

ix. في PostgreSQL يمكنك فعل هذا الأمر بأناقة أكبر باستخدام range types، لكنها غير مدعومة على نطاق واسع في قواعد البيانات الأخرى.

## المزيد من الأمثلة على write skew

قد يبدو write skew وكأنه مسألة غامضة (esoteric) في البداية، لكن بمجرد أن تعرف عنها قد تلاحظ مزيدًا من المواقف التي يمكن أن يحدث فيها. وفيما يلي بعض الأمثلة الإضافية:

## نظام حجز قاعات الاجتماعات

لنفترض أنك تريد فرض أنه لا يمكن وجود حجزين لغرفة الاجتماعات نفسها في الوقت نفسه [43]. عندما يريد أحدهم إجراء حجز، تتحقق أولًا من وجود أي حجوزات متعارضة (أي حجوزات لنفس الغرفة بنطاق زمني متداخل)، وإذا لم يُعثر على أي منها، تُنشئ الاجتماع (انظر المثال 7-2).ix

مثال 7-2. نظام حجز قاعات الاجتماعات يحاول تجنب الحجز المزدوج (غير آمن تحت snapshot isolation)

BEGIN TRANSACTION;

-- Check for any existing bookings that overlap with the period of noon-1pm
SELECT COUNT(*) FROM bookings
  WHERE room_id = 123 AND
    end_time > '2015-01-01 12:00' AND start_time < '2015-01-01 13:00';



-- If the previous query returned zero:
INSERT INTO bookings
  (room_id, start_time, end_time, user_id)
  VALUES (123, '2015-01-01 12:00', '2015-01-01 13:00', 666);



COMMIT;

للأسف، لا يمنع snapshot isolation مستخدمًا آخر من إدراج اجتماع متعارض بالتزامن. ولكي تضمن عدم وقوع تعارضات في الجدولة، تحتاج مرة أخرى إلى عزلة serializable.

## لعبة متعددة اللاعبين

في المثال 7-1، استخدمنا قفلًا (lock) لمنع lost update (أي لضمان أن اللاعبين لا يستطيعان تحريك القطعة نفسها في الوقت نفسه). لكن القفل لا يمنع اللاعبين من تحريك قطعتين مختلفتين إلى الموضع نفسه على اللوح، أو من تنفيذ بعض التحركات الأخرى التي تخالف قواعد اللعبة. وبحسب نوع القاعدة التي تفرضها، قد تتمكّن من استخدام unique constraint، لكنك في غير ذلك عرضة لـ write skew.

<!-- page 272 -->

## حجز اسم المستخدم

في موقع ويب يكون لكل مستخدم فيه اسم مستخدم فريد، قد يحاول مستخدمان إنشاء حسابات بالاسم نفسه في الوقت نفسه. ويمكنك استخدام transaction للتحقق مما إذا كان الاسم محجوزًا، فإن لم يكن، تنشئ حسابًا بذلك الاسم. لكن، كما في الأمثلة السابقة، فإن ذلك غير آمن تحت snapshot isolation. ولحسن الحظ، فإن unique constraint يمثّل حلًا بسيطًا هنا (سيتم إيقاف الـ transaction الثانية التي تحاول تسجيل اسم المستخدم بسبب مخالفة القيد).

## منع الإنفاق المزدوج

تحتاج خدمة تسمح للمستخدمين بإنفاق المال أو النقاط إلى التحقق من أن المستخدم لا ينفق أكثر مما لديه. ويمكنك تنفيذ ذلك بإدراج بند إنفاق مؤقت (tentative spending item) في حساب المستخدم، مع عرض جميع بنود الحساب، والتحقق من أن المجموع موجب [44]. ومع write skew، يمكن أن يحدث أن تُدرَج بنود إنفاق اثنان بالتزامن فتسبّب معًا في أن يصبح الرصيد سالبًا، دون أن تنتبه أي من الـ transactionين إلى الأخرى.

## الأطياف (phantoms) التي تسبب write skew

تتبع جميع هذه الأمثلة نمطًا مشابهًا:

