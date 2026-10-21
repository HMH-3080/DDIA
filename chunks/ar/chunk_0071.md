رغم أن الهدف بسيط—الاحتفاظ بنسخة من البيانات نفسها على عدة أجهزة— فإن الـreplication يتبيّن أنه مسألة معقّدة بشكل لافت. فهو يتطلّب التفكير بعناية في التزامن (concurrency) وفي كل الأشياء التي يمكن أن تسوء، وفي التعامل مع نتائج تلك الأعطال. وفي أقل تقدير، نحتاج إلى التعامل مع العقد غير المتاحة وانقطاعات الشبكة (ولا نحسب هنا حتى أنواع الأعطال الأكثر خفية، مثل تلف البيانات الصامت بسبب أخطاء برمجية).

ناقشنا ثلاث طرق رئيسية للـreplication:

## single-leader replication

يرسل العملاء جميع الكتابات إلى عقدة واحدة (الـleader)، وهي ترسل بدورها تدفّقًا من أحداث تغيير البيانات إلى الـreplicas الأخرى (الـfollowers). ويمكن إجراء القراءات على أي replica، لكن القراءات من الـfollowers قد تكون قديمة.

## multi-leader replication

يرسل العملاء كل كتابة إلى إحدى عدة عقد leaders، أيّ منها يمكنه قبول الكتابات. ويرسل الـleaders تدفّقات من أحداث تغيير البيانات إلى بعضها وإلى أي عقد followers.

## leaderless replication

يرسل العملاء كل كتابة إلى عدة عقد، ويقرأون من عدة عقد على التوازي، من أجل كشف العقد التي تحمل بيانات قديمة وتصحيحها.

لكل طريقة مزايا وعيوب. وsingle-leader replication شائع لأنه سهل الفهم نسبيًا ولا داعي للقلق بشأن حل التعارضات. أما multi-leader replication وleaderless replication فيمكن أن يكونا أكثر متانة عند وجود

<!-- page 215 -->

عقد معطوبة، وانقطاعات في الشبكة، وقفزات في latency— على حساب أن يصعب استنتاج سلوكهما وأنهما لا يوفّران سوى ضمانات consistency ضعيفة جدًا.

قد يكون الـreplication متزامنًا أو غير متزامن، وهذا له تأثير عميق في سلوك النظام عند وقوع عطل. ورغم أن الـreplication غير المتزامن قد يكون سريعًا حين يعمل النظام بسلاسة، من المهم أن نعرف ما يحدث حين يزداد تأخّر replication وتتعطّل الخوادم. فإذا تعطّل leader وعيّنت follower حُدِّث بشكل غير متزامن ليصبح leader الجديد، فقد تضيع بيانات committed (مُودَعة) مؤخرًا.

لقد نظرنا في بعض الآثار الغريبة التي قد يسبّبها تأخّر replication، وناقشنا بضعة نماذج consistency مفيدة لتحديد كيف ينبغي للتطبيق أن يتصرّف في حالة تأخّر replication:

## read-after-write consistency

ينبغي أن يرى المستخدمون دائمًا البيانات التي أدخلوها بأنفسهم.

## قراءات رتيبة

بعد أن يكون المستخدمون قد رأوا البيانات عند نقطة زمنية ما، لا ينبغي أن يروا لاحقًا بيانات من نقطة زمنية أسبق.

## القراءات ذات البادئة المتّسقة

ينبغي أن يرى المستخدمون البيانات في حالة تتّسق مع السببية (causality): على سبيل المثال، رؤية سؤال وردّه بالترتيب الصحيح.

أخيرًا، ناقشنا مشكلات التزامن (concurrency) التي تنشأ بطبيعتها في مقاربتَي multi-leader replication وleaderless replication: لأنهما تسمحان بحدوث عدة كتابات في وقت واحد (concurrently)، فقد تنشأ تعارضات. وقد فحصنا خوارزمية قد تستخدمها قاعدة البيانات لتحديد ما إذا كانت عملية قد سبقت عملية أخرى، أو ما إذا كانتا قد حدثتا في آن واحد. ولمّحنا أيضًا إلى أساليب لحل التعارضات عبر دمج التحديثات المتزامنة معًا.

في الفصل القادم سنواصل النظر في البيانات الموزّعة على عدة أجهزة، من خلال نظير الـreplication: تقسيم مجموعة بيانات كبيرة إلى partitions.

## المراجع

[1] Bruce G. Lindsay وPatricia Griffiths Selinger وC. Galtieri وآخرون: «ملاحظات على قواعد البيانات الموزّعة»، IBM Research، تقرير بحثي RJ2571(33471)، يوليو 1979.

[2] «Oracle Active Data Guard: حماية البيانات في الوقت الحقيقي وتوافرها»، ورقة بيضاء من Oracle، يونيو 2013.

[3] «مجموعات AlwaysOn Available»، في SQL Server Books Online، Microsoft، 2012.

<!-- page 216 -->

[4] Lin Qiao وKapil Surlaker وShirshanka Das وآخرون: «عن تحضير Espresso الطازج: منصّة LinkedIn لخدمة البيانات الموزّعة»، في ACM International Conference on Management of Data (SIGMOD)، يونيو 2013. [5] Jun Rao: «Intra-Cluster replication لـ Apache Kafka»، في ApacheCon North America، فبراير 2013. [6] «طوابير عالية التوافر»، في توثيق RabbitMQ Server، Pivotal Software, Inc.، 2014. [7] Yoshinori Matsunobu: «Semi-Synchronous replication في Facebook»، yoshinori-matsunobu.blogspot.co.uk، 1 أبريل 2014. [8] Robbert van Renesse وFred B. Schneider: «Chain replication لدعم throughput عالية وavailability»، في 6th USENIX Symposium on Operating System Design and Implementation (OSDI)، ديسمبر 2004. [9] Jeff Terrace وMichael J. Freedman: «تخزين الكائنات على CRAQ: Chain replication عالية الـthroughput لأحمال العمل read-mostly»، في USENIX Annual Technical Conference (ATC)، يونيو 2009. [10] Brad Calder وJu Wang وAaron Ogus وآخرون: «Windows Azure Storage: خدمة تخزين سحابية عالية availability مع consistency قوية»، في 23rd ACM Symposium on Operating Systems Principles (SOSP)، أكتوبر 2011. [11] Andrew Wang: «Windows Azure Storage»، umbrant.com، 4 فبراير 2016. [12] «Percona Xtrabackup - التوثيق»، Percona LLC، 2014. [13] «توافر GitHub هذا الأسبوع»، github.com، 14 سبتمبر 2012. [14] «التوقّف عن العمل السبت الماضي»، github.com، 26 ديسمبر 2012. [15] John Hugg: «'All in' مع الحتمية (determinism) من أجل الأداء والاختبار في الأنظمة الموزّعة»، في Strange Loop، سبتمبر 2015. [16] Amit Kapila: «داخليات WAL في PostgreSQL»، في PostgreSQL Conference (PGCon)، مايو 2012. [17] دليل MySQL Internals. Oracle، 2014. [18] Yogeshwer Sharma وPhilippe Ajoux وPetchean Ang وآخرون: «Wormhole: Pub-Sub موثوق لدعم خدمات الإنترنت المُكرَّرة جغرافيًا»، في 12th USENIX Symposium on Networked Systems Design and Implementation (NSDI)، مايو 2015. [19] «Oracle GoldenGate 12c: وصول في الوقت الحقيقي إلى المعلومات في الوقت الحقيقي»، ورقة بيضاء من Oracle، أكتوبر 2013. [20] Shirshanka Das وChavdar Botev وKapil Surlaker وآخرون: «كل شيء على متن Databus!»، في ACM Symposium on Cloud Computing (SoCC)، أكتوبر 2012.

<!-- page 217 -->

