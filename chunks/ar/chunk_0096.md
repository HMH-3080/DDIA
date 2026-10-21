عندما يقوم التطبيق باستعلام (مثلًا: «كم عدد الأطباء الموجودين في المناوبة (on call) حاليًا؟»)، لا تعرف قاعدة البيانات كيف يستخدم منطق التطبيق نتيجة ذلك الاستعلام. ولأجل السلامة، تحتاج قاعدة البيانات إلى افتراض أن أي تغيير في نتيجة الاستعلام (الـ premise) يعني أن الكتابات في تلك الـ transaction قد تكون غير صالحة. وبعبارة أخرى، قد تكون هناك تبعية سببية بين الاستعلامات والكتابات في الـ transaction. ولتوفير عزل serializable، يجب على قاعدة البيانات أن تكشف الحالات التي

<!-- page 285 -->

فيها تكون فيها الـ transaction قد تصرّفت بناءً على premise قديمة، وتُلغى الـ transaction في تلك الحالة.

كيف تعرف قاعدة البيانات إن كانت نتيجة الاستعلام ربما تكون قد تغيّرت؟ هناك حالتان يجب مراعاتهما:

• الكشف عن قراءات إصدار كائن MVCC قديم (حدثت كتابة غير مُثبَتة قبل القراءة)
• الكشف عن الكتابات التي تؤثر في القراءات السابقة (تحدث الكتابة بعد القراءة)

## الكشف عن قراءات MVCC قديمة

تذكّر أن snapshot isolation تُنفَّذ عادةً بواسطة multi-version concurrency control (MVCC؛ انظر الشكل 7-10). عندما تقرأ الـ transaction من snapshot متسقة في قاعدة بيانات MVCC، فإنها تتجاهل الكتابات التي أجرتها أي معاملات أخرى لم تكن قد أثبتت (commit) بعد في الوقت الذي أُخذت فيه الـ snapshot. في الشكل 7-10، ترى الـ transaction 43 أن on_call لدى Alice يساوي true، لأن الـ transaction 42 (والتي عدّلت حالة on-call لدى Alice) لم تُثبَت بعد. لكن، عندما تريد الـ transaction 43 أن تُثبَت، تكون الـ transaction 42 قد أثبتت بالفعل. وهذا يعني أن الكتابة التي تم تجاهلها عند القراءة من الـ snapshot المتسقة قد أصبح مفعولها ساريًا الآن، وأن premise الـ transaction 43 لم تعد صحيحة.

<table>
<tr><th>select count(*)</th><th>update doctors</th><th></th></tr>
<tr><td>from doctors</td><td>set on_call = false</td><td></td></tr>
<tr><td>where on_call = true</td><td>where name = ‘Alice’</td><td></td></tr>
<tr><td>and shift_id = 1234 الـ transaction 42 ·</td><td>and shift_id = 1234</td><td>الزمن</td></tr>
</table>

## قاعدة البيانات

<table>
<tr><th>الـ transaction 43 -    -</th><th></th><th></th><th></th><th></th></tr>
<tr><td></td><td></td><td></td><td>select count(*)</td><td>update doctors commit retry…</td></tr>
<tr><td></td><td></td><td></td><td>from doctors</td><td>set on_call = false</td></tr>
<tr><td></td><td></td><td></td><td>where on_call = true</td><td>where name = ‘Bob’</td></tr>
<tr><td></td><td></td><td></td><td>and shift_id = 1234</td><td>and shift_id = 1234</td></tr>
<tr><td colspan="4">shift_id name on_call created_by deleted_by</td><td></td></tr>
<tr><td>1234</td><td>Alice</td><td>true</td><td>42</td><td>الـ transaction 42 لم تُثبَت بعد،</td></tr>
<tr><td>1234</td><td>Alice</td><td>false</td><td>42</td><td>لذلك ترى الـ transaction 43 أن Alice لا تزال</td></tr>
<tr><td></td><td></td><td></td><td></td><td>في المناوبة. لكن، الـ transaction</td></tr>
<tr><td>1234</td><td>Bob</td><td>true</td><td></td><td>manager يلاحظ أن هذه القيمة لم</td></tr>
<tr><td>1234</td><td>Carol</td><td>- false</td><td></td><td>تعد محدَّثة.</td></tr>
</table>

الشكل 7-10. الكشف عندما تقرأ الـ transaction قيمًا قديمة من snapshot في MVCC.

<!-- page 286 -->

لمنع هذا الشذوذ، تحتاج قاعدة البيانات إلى تتبّع اللحظات التي تتجاهل فيها الـ transaction كتابات معاملة أخرى بسبب قواعد الرؤية في MVCC. وعندما تريد الـ transaction أن تُثبَت، تتحقق قاعدة البيانات مما إذا كانت أي من الكتابات المُتجاهَلة قد أُثبِتت الآن. وإذا كان الأمر كذلك، فيجب إلغاء الـ transaction.

لماذا الانتظار حتى لحظة الإيثبات (commit)؟ ولماذا لا تُلغى الـ transaction 43 فورًا عند اكتشاف القراءة القديمة؟ حسنًا، إذا كانت الـ transaction 43 للقراءة فقط، فلن تحتاج إلى الإلغاء، لأنه لا يوجد خطر write skew. في الوقت الذي تُجري فيه الـ transaction 43 قراءتها، لا تعرف قاعدة البيانات بعدُ ما إذا كانت تلك الـ transaction ستجري كتابة لاحقًا. إضافةً إلى ذلك، قد تُلغى الـ transaction 42 أو قد تظل غير مُثبَتة في الوقت الذي تُثبَت فيه الـ transaction 43، لذا قد تبيّن في النهاية أن القراءة لم تكن قديمة أصلًا. وبتجنّب الإلغاءات غير الضرورية، تحافظ SSI على دعم snapshot isolation للقراءات طويلة المدى من snapshot متسقة.

## الكشف عن الكتابات التي تؤثر في القراءات السابقة

الحالة الثانية التي يجب مراعاتها هي عندما تُعدّل معاملة أخرى البيانات بعد أن تكون قد قُرئت. وتوضَّح هذه الحالة في الشكل 7-11.

<table>
<tr><th>select count(*)</th><th>update doctors</th><th></th><th></th><th></th><th></th></tr>
<tr><td>from doctors</td><td>set on</td><td>call = false</td><td></td><td></td><td></td></tr>
<tr><td></td><td>all = tru e</td><td></td><td></td><td></td><td></td></tr>
<tr><td>nd sh الـ transaction 42</td><td>234 d</td><td></td><td></td><td></td><td>m</td></tr>
<tr><td>قاعدة البيانات</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>ABORT</td></tr>
<tr><td>الـ transaction 43 · -</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>select count(*)</td><td></td><td colspan="2">update doctors</td><td></td><td>commit retry…</td></tr>
<tr><td>from doctors</td><td></td><td colspan="2">set on_call = false</td><td></td><td></td></tr>
<tr><td></td><td>where on_call = true</td><td colspan="2">where name = ‘Bob’</td><td></td><td></td></tr>
<tr><td></td><td>and shift_id = 1234</td><td colspan="2">and shift_id = 1234</td><td></td><td></td></tr>
<tr><td>نطاق المفتاح</td><td>معلومات</td><td></td><td colspan="3">shift_id name on_call</td></tr>
<tr><td>1234</td><td>قُرئت بواسطة الـ transaction 42</td><td>قديم</td><td>1234</td><td>Alice</td><td>true</td></tr>
<tr><td>1234</td><td>قُرئت بواسطة الـ transaction 43</td><td>جديد</td><td>1234</td><td>Alice</td><td>false</td></tr>
<tr><td colspan="2">أقفال نطاق الـ index على</td><td colspan="4">ملاحظة: التحديث الذي أجرته الـ transaction 42</td></tr>
<tr><td colspan="2">index على doctors.shift_id</td><td colspan="4">يؤثر في القراءة التي أجرتها الـ transaction 43</td></tr>
</table>

الشكل 7-11. في serializable snapshot isolation، الكشف عندما تعدّل معاملة واحدة قراءات معاملة أخرى.

في سياق two-phase locking ناقشنا أقفال نطاق الـ index (انظر «أقفال نطاق الـ index» في صفحة 260)، وهي تتيح لقاعدة البيانات قفل الوصول إلى جميع الصفوف المطابقة لاستعلام بحث ما، مثل WHERE shift_id = 1234. ويمكننا استخدام تقنية مشابهة هنا، إلا أن أقفال SSI لا تحجب المعاملات الأخرى.

<!-- page 287 -->

في الشكل 7-11، تبحث كلتا الـ transactionين 42 و43 عن الأطباء في المناوبة (on call) خلال المناوبة 1234. وإذا كان هناك index على shift_id، فيمكن لقاعدة البيانات أن تستخدم مُدخل الـ index 1234 لتسجيل أن الـ transactionين 42 و43 قد قرأتا هذه البيانات. (وإذا لم يكن هناك index، فيمكن تتبّع هذه المعلومات على مستوى الجدول.) ولا يلزم الاحتفاظ بهذه المعلومات إلا لفترة: بعد انتهاء الـ transaction (بإثباتها أو إلغائها)، وبعد انتهاء جميع المعاملات المتزامنة، يمكن لقاعدة البيانات أن تنسى ما الذي قرأته.

عندما تكتب الـ transaction إلى قاعدة البيانات، عليها أن تبحث في الـ indexes عن أي معاملات أخرى قرأت مؤخرًا البيانات المتأثرة. وهذه العملية مشابهة لاكتساب write lock على نطاق المفتاح المتأثر، لكن بدلًا من الحجب حتى تثبت القارئات، يعمل القفل كـ tripwire: فهو ببساطة يُشعر المعاملات بأن البيانات التي قرأتها ربما لم تعد محدَّثة.

في الشكل 7-11، تُشعر الـ transaction 43 الـ transaction 42 بأن قراءتها السابقة قديمة، والعكس صحيح. الـ transaction 42 هي أول من يُثبَت، ونجاحها: رغم أن كتابة الـ transaction 43 أثّرت في 42، فإن 43 لم تُثبَت بعد، لذا لم يكتب مفعول الكتابة بعد. لكن، عندما تريد الـ transaction 43 أن تُثبَت، تكون الكتابة المتعارضة من 42 قد أُثبِتت بالفعل، لذا يجب إلغاء 43.

## أداء serializable snapshot isolation

كالعادة، تؤثر تفاصيل هندسية كثيرة في مدى نجاح أي خوارزمية في الممارسة العملية. فمثلًا، أحد المفاضلات هو مستوى التفصيل (granularity) الذي تُتتبَّع عنده قراءات المعاملات وكتابتها. إذا احتفظت قاعدة البيانات بسجل تفصيلي لنشاط كل معاملة، فيمكنها أن تكون دقيقة بشأن المعاملات التي يلزم إلغاؤها، لكن عبء المحاسبة (bookkeeping) قد يصبح كبيرًا. التتبّع الأقل تفصيلًا أسرع، لكنه قد يؤدي إلى إلغاء عدد أكبر من المعاملات مما هو ضروري تمامًا.

في بعض الحالات، لا بأس أن تقرأ الـ transaction معلومات طُمست بمعاملة أخرى: فبحسب ما حدث فيما عداه، من الممكن أحيانًا إثبات أن نتيجة التنفيذ تبقى مع ذلك serializable. وتستخدم PostgreSQL هذه النظرية لتقليل عدد عمليات الإلغاء غير الضرورية [11, 41].

