إذا كان كل ما تحتاجه هو scale للتعامل مع حمل أعلى، فإن أبسط نهج هو شراء جهاز أكثر قوة (الذي يُسمّى أحيانًا vertical scaling أو scale up). ويمكن ضمّ عدة CPUs وعدة رقائق RAM وعدة أقراص (disks) معًا تحت نظام تشغيل واحد، ويتيح interconnect سريع لأي CPU الوصول إلى أي جزء من الذاكرة أو القرص. وفي هذا النوع من بنية الذاكرة المشتركة (shared-memory architecture)، يمكن التعامل مع جميع المكوّنات وكأنها جهاز واحد [1].i

المشكلة في نهج الذاكرة المشتركة (shared-memory) هي أن التكلفة تنمو أسرع من النمو الخطي: فالجهاز الذي يحتوي على ضعف عدد CPUs وضعف حجم RAM وضعف سعة القرص (disk) عن جهاز آخر، يكلّف عادةً أكثر بكثير من الضِعف. وبسبب وجود عنق الزجاجة (bottlenecks)، لا يمكن للجهاز ذو الحجم المضاعف أن يتعامل بالضرورة مع ضعف الحمل.

قد توفّر بنية الذاكرة المشتركة درجةً محدودة من fault tolerance (تحمّل الأخطاء)— فالأجهزة عالية النهاية تملك مكوّنات hot-swappable (قابلة للاستبدال أثناء التشغيل) (يمكنك استبدال الأقراص (disks) ووحدات الذاكرة وحتى المعالجات (CPUs) دون إيقاف تشغيل الأجهزة)— لكنها بالتأكيد محدودة إلى موقع جغرافي واحد.

نهج آخر هو بنية الـdisk المشتركة (shared-disk architecture)، التي تستخدم عدة أجهزة ذات معالجات (CPUs) وذاكرة RAM مستقلة، لكنها تخزّن البيانات على مصفوفة من الأقراص (disks) مشتركة بين الأجهزة، وهي الأجهزة المتصلة عبر شبكة سريعة.ii وتُستخدم هذه البنية لبعض أحمال العمل (workloads) الخاصة بـdata warehousing، لكن التنافس (contention) والعبء الزائد الذي يفرضه الـlocking يحدّان من قابلية توسّع نهج الـdisk المشتركة [2].

## بنى shared-nothing

وفي المقابل، فقد حققت بنى shared-nothing [3] (التي تُسمّى أحيانًا horizontal scaling أو scale out) الكثير من الشعبية. وفي هذا النهج، تُسمّى كل آلة أو آلة افتراضية (virtual machine) تشغّل برمجيات قاعدة البيانات عقدة (node). وتستخدم كل عقدة معالجاتها (CPUs) وذاكرة RAM وأقراصها (disks) بشكل مستقل. وأي تنسيق (coordination) بين العقد يجري على مستوى البرمجيات، باستخدام شبكة تقليدية.

ومع نشر الآلات الافتراضية (cloud deployments) في السحابة

<!-- page 169 -->

، لا تحتاج إلى العمل بمقياس (scale) Google: حتى الشركات الصغيرة صارت البنية الموزّعة متعددة المناطق (multi-region) ممكنة اليوم.

في هذا الجزء من الكتاب، نركّز على بنى shared-nothing— ليس لأنها بالضرورة أفضل خيار لكل حالة استخدام (use case)، بل لأنها تتطلب أكبر قدر من الحذر منك، أنت مطوّر التطبيق. فإذا كانت بياناتك موزّعة على عدة عقد، فيجب أن تكون على وعي بالقيود والمقايضات (trade-offs) التي تنشأ في مثل هذا النظام الموزّع— فقاعدة البيانات لا تستطيع أن تُخفيها عنك بشكل سحري.

ورغم أن البنية الموزّعة من نوع shared-nothing لها مزايا كثيرة، فإنها عادةً ما تُضيف أيضًا تعقيدًا إضافيًا للتطبيقات، وأحيانًا تحدّ من تعبيرية (expressiveness) نماذج البيانات التي يمكنك استخدامها. وفي بعض الحالات، يمكن لبرنامج بسيط أحادي الخيط (single-threaded) أن يؤدّي المهمة بفارق كبير مقارنةً بـcluster ذي أكثر من 100 نواة CPU [4]. ومن ناحية أخرى، يمكن لأنظمة shared-nothing أن تكون قوية جدًا. وتتعمّق الفصول القليلة التالية في التفاصيل حول المسائل التي تنشأ عندما تكون البيانات موزّعة.

## Replication مقابل Partitioning

هناك طريقتان شائعتان لتوزيع البيانات على عدة عقد:

## Replication

الاحتفاظ بنسخة من البيانات نفسها على عدة عقد مختلفة، ربما في مواقع مختلفة. يوفّر replication تكرارًا (redundancy): فإذا كانت بعض العقد غير متاحة، فلا يزال يمكن تقديم البيانات من العقد المتبقية. ويمكن لـreplication أيضًا أن يساعد في تحسين الأداء. ونناقش replication في الفصل 5.

## Partitioning

تقسيم قاعدة بيانات كبيرة إلى مجموعات فرعية أصغر تُسمّى partitions، بحيث يمكن إسناد الـpartitions المختلفة إلى عقد مختلفة (وهي أيضًا معروفة بـsharding). ونناقش partitioning في الفصل 6.

وهذه آليتان منفصلتان، لكنهما غالبًا ما يمشيان معًا، كما هو موضَّح في الشكل II-1.

<!-- page 170 -->

القسم 1، النسخة 1

<table>
<tr><th></th><th></th><th></th><th></th><th></th><th colspan="2">القسم 2، النسخة 1</th><th></th><th></th></tr>
<tr><td>136 →</td><td>211 →</td><td>S</td><td>377 →</td><td>N</td><td>629 →</td><td>696 →</td><td>N</td><td>858 →</td></tr>
<tr><td>Four score</td><td>Johannes</td><td></td><td>Whereas</td><td></td><td>Die Würde</td><td>Whereas</td><td></td><td>We hold</td></tr>
<tr><td>and seven</td><td>Dei gracia</td><td></td><td colspan="2">recognition</td><td>des Men-</td><td>the Lords</td><td></td><td>these truths</td></tr>
<tr><td>years ago</td><td>Rex Anglie,</td><td></td><td>of the</td><td></td><td>schen ist</td><td>Spiritual</td><td></td><td>to be self-</td></tr>
<tr><td>our fathers</td><td>Dominus</td><td></td><td>inherent</td><td></td><td>unantastbar</td><td colspan="2">and Tempo-</td><td>evident</td></tr>
<tr><td></td><td></td><td></td><td></td><td>¹ copy of</td><td></td><td></td><td></td><td>¹ copy of</td></tr>
<tr><td></td><td></td><td></td><td></td><td>◦ the same</td><td></td><td></td><td></td><td>◦ the same</td></tr>
<tr><td colspan="2">القسم 1، النسخة 2</td><td></td><td>v</td><td>. data</td><td colspan="2">القسم 2، النسخة 2</td><td></td><td>. data</td></tr>
<tr><td>X 136 →</td><td>211 →</td><td></td><td>377 →</td><td>S</td><td>629 →</td><td>696 →</td><td></td><td>858 →</td></tr>
<tr><td>Four score</td><td>Johannes</td><td></td><td>Whereas</td><td></td><td>Die Würde</td><td>Whereas</td><td></td><td>We hold</td></tr>
<tr><td>and seven</td><td>Dei gracia</td><td></td><td colspan="2">recognition</td><td>des Men-</td><td>the Lords</td><td></td><td>these truths</td></tr>
<tr><td>years ago</td><td>Rex Anglie,</td><td></td><td>of the</td><td></td><td>schen ist</td><td>Spiritual</td><td></td><td>to be self-</td></tr>
<tr><td>our fathers</td><td>Dominus</td><td></td><td>inherent</td><td></td><td>unantastbar</td><td colspan="2">and Tempo-</td><td>evident</td></tr>
</table>

الشكل II-1. قاعدة بيانات مقسّمة إلى قسمين (partitions)، مع نسختين (replicas) لكل قسم.

بعد فهم تلك المفاهيم، يمكننا مناقشة المقايضات (trade-offs) الصعبة التي عليك اتخاذها في نظام موزّع. وسنناقش الـtransactions في الفصل 7، لأن ذلك سيساعدك على فهم كل الأشياء الكثيرة التي يمكن أن تسوء في نظام بيانات، وما يمكنك فعله بشأنها. وسنختم هذا الجزء من الكتاب بمناقشة القيود الجوهرية للأنظمة الموزّعة في الفصلين 8 و9.

وفي وقت لاحق، في الجزء الثالث من هذا الكتاب، سنناقش كيف يمكنك أخذ عدة مخازن بيانات (datastores) (ربما موزّعة) ودمجها في نظام أكبر، بما يلبي احتياجات تطبيق معقّد. لكن لنبدأ أولًا بالحديث عن البيانات الموزّعة.

## المراجع

[1] Ulrich Drepper: «ما ينبغي أن يعرفه كل مبرمج عن الذاكرة»، akkadia.org، 21 نوفمبر 2007. [2] Ben Stopford: «Shared Nothing مقابل Shared Disk: نظرة مستقلة»، benstopford.com، 24 نوفمبر 2009. [3] Michael Stonebraker: «حجة Shared Nothing»، IEEE Database Engineering Bulletin، المجلد 9، العدد 1، الصفحات 4–9، مارس 1986. [4] Frank McSherry وMichael Isard وDerek G. Murray: «القابلية للتوسّع! لكن بأي تكلفة؟»، في 15th USENIX Workshop on Hot Topics in Operating Systems (HotOS)، مايو 2015.

<!-- page 171 -->

<!-- page 172 -->

<table>
<tr><th></th><th></th><th>إلى Consistency</th></tr>
<tr><td>• -</td><td></td><td>&amp; Consensus</td></tr>
<tr><td>RethinkDB</td><td>Mon</td><td>الفصل 9)</td></tr>
<tr><td>fy</td><td></td><td></td></tr>
<tr><td></td><td>NC</td><td></td></tr>
<tr><td>PostgreSQL</td><td></td><td></td></tr>
</table>

<table>
<tr><th></th><th>OR</th><th></th></tr>
<tr><td></td><td></td><td>CouchDB</td></tr>
<tr><td></td><td></td><td>alendar, sync</td></tr>
<tr><td></td><td></td><td>-</td></tr>
<tr><td></td><td></td><td></td></tr>
<tr><td></td><td>C A</td><td>10</td></tr>
<tr><td></td><td></td><td>Eassandra</td></tr>
</table>

إلى Log-structured Storage (الفصل 3)

<!-- page 173 -->

## Replication

الفرق الجوهري بين شيء قد يسوء وشيء لا يمكن أن يسوء إطلاقًا هو أن حين يسوء شيء لا يمكن أن يسوء إطلاقًا، فإن الأمر ينتهي عادةً إلى أنه يستحيل الوصول إليه أو إصلاحه.

—Douglas Adams, Mostly Harmless (1992)

يعني replication الاحتفاظ بنسخة من البيانات نفسها على عدة آلات متصلة عبر شبكة. وكما ناقشنا في مقدمة الجزء الثاني، هناك عدة أسباب قد ترغب في نسخ بياناتك:

• لإبقاء البيانات قريبة جغرافيًا من مستخدميك (وبالتالي تقليل latency)
• للسماح للنظام بالاستمرار في العمل حتى لو فشلت بعض أجزائه (وبالتالي زيادة availability)
• للتوسّع (scale out) في عدد الآلات التي يمكنها خدمة استعلامات القراءة (وبالتالي زيادة read throughput)

