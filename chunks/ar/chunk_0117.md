[70] David Terei وAmit Levy: «Blade: جامع قمامة في مركز بيانات»، arXiv: 1504.02578، 13 أبريل 2015. [71] Martin Maas وTim Harris وKrste Asanović وJohn Kubiatowicz: «Trash Day: تنسيق جمع القمامة في الأنظمة الموزّعة»، في 15th USENIX Workshop on Hot Topics in Operating Systems (HotOS)، مايو 2015. [72] «Predictable Low Latency»، Cinnober Financial Technology AB، cinnober.com، 24 نوفمبر 2013. [73] Martin Fowler: «معمارية LMAX»، martinfowler.com، 12 يوليو 2011. [74] Flavio P. Junqueira وBenjamin Reed: ZooKeeper: تنسيق العمليات الموزّعة. O’Reilly Media، 2013. ISBN: 978-1-449-36130-3 [75] Enis Söztutar: «HBase وHDFS: فهم استخدام نظام الملفات في HBase»، في HBaseCon، يونيو 2013. [76] Caitie McCaffrey: «العملاء مُزعجون: أي كيف عطلت Halo 4 الخدمات عند الإطلاق وكيف صمدنا»، caitiem.com، 23 يونيو 2015. [77] Leslie Lamport وRobert Shostak وMarshall Pease: «مشكلة الجنرالات Byzantine»، ACM Transactions on Programming Languages and Systems (TOPLAS)، المجلد 4، العدد 3، الصفحات 382–401، يوليو 1982. doi:10.1145/357172.357176 [78] Jim N. Gray: «ملاحظات على أنظمة تشغيل قواعد البيانات»، في Operating Systems: An Advanced Course، Lecture Notes in Computer Science، المجلد 60، بتحرير R. Bayer،
R. M. Graham وG. Seegmüller، الصفحات 393–481، Springer-Verlag، 1978. ISBN: 978-3-540-08755-7 [79] Brian Palmer: «كم كانت معقّدة الإمبراطورية البيزنطية؟»، slate.com، 20 أكتوبر 2011. [80] Leslie Lamport: «كتاباتي»، research.microsoft.com، 16 ديسمبر 2014. يمكن العثور على هذه الصفحة بالبحث في الويب عن السلسلة المكوّنة من 23 حرفًا الناتجة عن إزالة الشرطات من السلسلة allla-mport-spubso-ntheweb. [81] John Rushby: «معماريات النواقل (bus) للأنظمة المدمجة الحرجة للسلامة»، في 1st International Workshop on Embedded Software (EMSOFT)، أكتوبر 2001. [82] Jake Edge: «ELC: دروس تعلّمها SpaceX»، lwn.net، 6 مارس 2013. [83] Andrew Miller وJoseph J. LaViola, Jr.: «consensus Byzantine مجهول من ألغاز متوسطة الصعوبة: نموذج لـ Bitcoin»، University of Central Florida، تقرير تقني CS-TR-14-01، أبريل 2014. [84] James Mickens: «أكثر اللحظات إيلامًا»، USENIX ;login: logout، مايو 2013. [85] Evan Gilman: «اكتشاف حزمة السموم في Apache ZooKeeper»، pagerd‐ uty.com، 7 مايو 2015.

<!-- page 340 -->

[86] Jonathan Stone وCraig Partridge: «عندما لا يتّفق CRC مع checksum الخاص بـ TCP»، في ACM Conference on Applications, Technologies, Architectures, and Protocols for Computer Communication (SIGCOMM)، أغسطس 2000. doi: 10.1145/347059.347561 [87] Evan Jones: «كيف يفشل checksum الخاص بـ TCP وchecksum الخاص بـ Ethernet معًا»، evanjones.ca، 5 أكتوبر 2015. [88] Cynthia Dwork وNancy Lynch وLarry Stockmeyer: «consensus في حضور التزامن الجزئي»، Journal of the ACM، المجلد 35، العدد 2، الصفحات 288–323، أبريل 1988. doi:10.1145/42282.42283 [89] Peter Bailis وAli Ghodsi: «الاتساق النهائي اليوم: القيود والتوسّعات وما وراءها»، ACM Queue، المجلد 11، العدد 3، الصفحات 55-63، مارس 2013. doi:10.1145/2460276.2462076 [90] Bowen Alpern وFred B. Schneider: «تعريف liveness»، Information Processing Letters، المجلد 21، العدد 4، الصفحات 181–185، أكتوبر 1985. doi: 10.1016/0020-0190(85)90056-0 [91] Flavio P. Junqueira: «يا صديقي، أين metadata؟»، fpj.me، 28 مايو 2015. [92] Scott Sanders: «تقرير حادثة 28 يناير»، github.com، 3 فبراير 2016. [93] Jay Kreps: «بعض الملاحظات حول Kafka وJepsen»، blog.empathybox.com، 25 سبتمبر 2013. [94] Thanh Do وMingzhe Hao وTanakorn Leesatapornwongsa وآخرون: «Limplock: فهم أثر Limpware على أنظمة السحابة ذات التوسّع الأفقي»، في 4th ACM Symposium on Cloud Computing (SoCC)، أكتوبر 2013. doi: 10.1145/2523616.2523627 [95] Frank McSherry وMichael Isard وDerek G. Murray: «القابلية للتوسّع! لكن بأي تكلفة؟»، في 15th USENIX Workshop on Hot Topics in Operating Systems (HotOS)، مايو 2015.

<!-- page 341 -->

<!-- page 342 -->

<!-- page 343 -->

## الاتساق و consensus

أفضل أن تكون حيًّا وخطأً أم صحيحًا وميتًا؟

—Jay Kreps, A Few Notes on Kafka and Jepsen (2013)

الكثير من الأمور يمكن أن تسوء في الأنظمة الموزّعة، كما ناقشنا في الفصل 8. وأبسط طريقة للتعامل مع هذه الأعطال هي ببساطة أن نترك الخدمة كاملةً تتعطّل، ونعرض للمستخدم رسالة خطأ. وإذا كان هذا الحل غير مقبول، فنحن بحاجة إلى إيجاد طرق للتسامح مع الأعطال—أي لإبقاء الخدمة تعمل بشكل صحيح، حتى لو كان أحد مكوّناتها الداخلية معطوبًا.

في هذا الفصل، سنتحدث عن بعض أمثلة الخوارزميات والبروتوكولات لبناء أنظمة موزّعة متسامحة مع الأعطال. وسنفترض أن جميع مشكلات الفصل 8 يمكن أن تحدث: يمكن أن تُفقد الحزم في الشبكة، أو تُعاد ترتيبها، أو تُكرَّر، أو تتأخر تأخيرًا غير محدود؛ والساعات تقريبية في أحسن الأحوال؛ كما يمكن للعُقد أن تتوقّف مؤقتًا (مثلًا بسبب جمع القمامة) أو تنهار في أي وقت.

أفضل طريقة لبناء أنظمة متسامحة مع الأعطال هي إيجاد بعض التجريدات العامة (general-purpose) ذات ضمانات مفيدة، وتنفيذها مرة واحدة، ثم ترك التطبيقات تعتمد على تلك الضمانات. وهذا هو الأسلوب نفسه الذي استخدمناه مع المعاملات (transactions) في الفصل 7: فباستخدام transaction، يستطيع التطبيق أن يتظاهر بأنه لا توجد انهيارات (atomicity)، ولا أحد آخر يصل إلى قاعدة البيانات في الوقت نفسه (isolation)، وأجهزة التخزين موثوقة تمامًا (durability). ورغم أن الانهيارات وحالات السباق (race conditions) وأعطال الأقراص تحدث فعلًا، فإن تجريد transaction يخفي تلك المشكلات بحيث لا يحتاج التطبيق إلى القلق بشأنها.

وسنكمل الآن على المنوال نفسه، ونبحث عن تجريدات تسمح لتطبيق بأن يتجاهل بعض مشكلات الأنظمة الموزّعة. فمثلًا، من أهم التجريدات في الأنظمة الموزّعة هي consensus: أي جعل جميع العُقد تتفق على شيء ما. وكما سنرى في هذا الفصل، فإن بلوغ consensus

<!-- page 344 -->

بموثوقية رغم أعطال الشبكة وفشل العمليات مسألة تش.chromium بصعوبة مفاجئة.

بمجرد أن تتوفّر لديك تنفيذية (implementation) لـ consensus، تستطيع التطبيقات استخدامه لأغراض شتّى. فمثلًا، لنفترض أن لديك قاعدة بيانات ذات replication بـleader واحد (single-leader). إذا مات leader واحتجت إلى الانتقال (fail over) إلى عقدة أخرى، فيمكن لعُقد قاعدة البيانات المتبقية أن تستخدم consensus لانتخاب leader جديد. وكما ناقشنا في «معالجة أعطال العُقد» في الصفحة 156، من المهم ألّا يوجد سوى leader واحد، وأن تتّفق جميع العُقد على من هو leader. فإذا اعتقدت عقدتان معًا أنهما leader، تُسمّى هذه الحالة split brain، وهي غالبًا ما تؤدّي إلى فقدان بيانات. والتنفيذيات الصحيحة لـ consensus تساعد على تفادي هذه المشكلات.

وفي وقت لاحق من هذا الفصل، في «المعاملات الموزّعة وconsensus» في الصفحة 352، سنبحث في الخوارزميات لحل consensus والمشكلات المرتبطة به. لكن علينا أولًا أن نستكشف نطاق الضمانات والتجريدات التي يمكن توفيرها في نظام موزّع.

نحتاج إلى فهم نطاق ما يمكن وما لا يمكن فعله: في بعض المواقف، من الممكن أن يتسامح النظام مع الأعطال ويواصل العمل؛ وفي مواقف أخرى، ذلك غير ممكن. وقد استُكشفت حدود ما هو ممكن وغير ممكن بعمق، سواء في البراهين النظرية أو في التطبيقات العملية. وسنحصل في هذا الفصل على لمحة عامة عن تلك الحدود الأساسية.

