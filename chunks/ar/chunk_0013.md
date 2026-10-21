مدى سهولة تعديلك لنظام بيانات وتكييفه مع المتطلبات المتغيّرة يرتبط ارتباطًا وثيقًا ببساطته وبتجريداته (abstractions): فالأنظمة البسيطة سهلة الفهم عادةً أسهل في التعديل من الأنظمة المعقّدة. لكن بما أن هذه فكرة بالغة الأهمية، سنستخدم كلمة أخرى للإشارة إلى المرونة على مستوى نظام البيانات: قابلية التطور (evolvability) [34].

## ملخص

في هذا الفصل استكشفنا بعض الطرق الأساسية للتفكير في التطبيقات كثيفة البيانات (data-intensive). وهذه المبادئ ستوجّهنا في بقية الكتاب، حيث نغوص في تفاصيل تقنية عميقة.

لكي يكون تطبيق ما مفيدًا، عليه أن يستوفي متطلبات مختلفة. وهناك متطلبات وظيفية (functional requirements) (ما ينبغي أن يفعله، مثل السماح بتخزين البيانات واسترجاعها والبحث فيها ومعالجتها بطرق مختلفة)، وهناك بعض المتطلبات غير الوظيفية (nonfunctional requirements) (خصائص عامة مثل الأمان (security) والموثوقية (reliability) والامتثال (compliance) وقابلية التوسع (scalability) والتوافق (compatibility) وقابلية الصيانة (maintainability)). وفي هذا الفصل ناقشنا الموثوقية وقابلية التوسع وقابلية الصيانة بالتفصيل.

الموثوقية تعني جعل الأنظمة تعمل بشكل صحيح، حتى حين تحدث الأعطال (faults). ويمكن أن تكون الأعطال في الأجهزة (hardware) (عادةً عشوائية وغير مترابطة)، أو في البرمجيات (software) (حيث تكون الأخطاء البرمجية (bugs) عادةً منهجية وصعبة المعالجة)، أو في البشر (البشر لا محالة يصيبون أخطاء من حين لآخر). وتقنيات تحمّل الأعطال (fault tolerance) يمكنها إخفاء أنواع معينة من الأعطال عن المستخدم النهائي.

قابلية التوسع تعني وجود استراتيجيات للحفاظ على جودة الأداء (performance)، حتى عندما يزداد الحمل (load). ولمناقشة قابلية التوسع، نحتاج أولًا إلى طرائق لوصف الحمل والأداء بشكل كمّي. وقد ألقينا نظرة سريعة على الخطوط الزمنية الرئيسية (home timelines) لـTwitter مثالًا على وصف الحمل، وعلى الـpercentiles الخاصة بزمن الاستجابة (response time) كوسيلة لقياس الأداء.

<!-- page 45 -->

في نظام قابل للتوسع (scalable)، يمكنك إضافة قدرة معالجة (processing capacity) من أجل أن يبقى موثوقًا (reliable) تحت الحمل العالي.

قابلية الصيانة لها جوانب كثيرة، لكن جوهرها هو جعل الحياة أفضل لفرق الهندسة (engineering) والعمليات (operations) التي تحتاج إلى العمل مع النظام. ويمكن أن تساعد التجريدات (abstractions) الجيدة على تقليل التعقيد وجعل النظام أسهل في التعديل والتكييف من أجل حالات الاستخدام الجديدة. وتعني قابلية التشغيل (operability) الجيدة وجود رؤية جيدة لصحة النظام، ووجود طرق فعّالة لإدارته.

للأسف لا يوجد حل سهل لجعل التطبيقات موثوقة أو قابلة للتوسع أو قابلة للصيانة. لكن هناك أنماط وتقنيات معينة يظل ظهورها متكررًا في مختلف أنواع التطبيقات. وفي الفصول القليلة التالية سننظر في بعض الأمثلة على أنظمة البيانات، ونحلّل كيف تعمل في اتجاه تحقيق تلك الأهداف.

وفي وقت لاحق من الكتاب، في الجزء الثالث، سننظر في أنماط الأنظمة التي تتألف من عدة مكوّنات تعمل معًا، مثل النظام في الشكل 1-1.

## المراجع

[1] Michael Stonebraker وUğur Çetintemel: «'One Size Fits All': An Idea Whose Time Has Come and Gone»، في 21st International Conference on Data Engineering (ICDE)، أبريل 2005.

[2] Walter L. Heimerdinger وCharles B. Weinstock: «A Conceptual Framework for System Fault Tolerance»، Technical Report CMU/SEI-92-TR-033، Software Engineering Institute، Carnegie Mellon University، أكتوبر 1992. [3] Ding Yuan وYu Luo وXin Zhuang وآخرون: «Simple Testing Can Prevent Most Critical Failures: An Analysis of Production Failures in Distributed Data-Intensive Systems»، في 11th USENIX Symposium on Operating Systems Design and Implementation (OSDI)، أكتوبر 2014. [4] Yury Izrailevsky وAriel Tseitlin: «The Netflix Simian Army»، techblog.netflix.com، 19 يوليو 2011. [5] Daniel Ford وFrançois Labelle وFlorentina I. Popovici وآخرون: «Availability in Globally Distributed Storage Systems»، في 9th USENIX Symposium on Operating Systems Design and Implementation (OSDI)، أكتوبر 2010. [6] Brian Beach: «Hard Drive Reliability Update – Sep 2014»، backblaze.com، 23 سبتمبر 2014. [7] Laurie Voss: «AWS: The Good, the Bad and the Ugly»، blog.awe.sm، 18 ديسمبر 2012.

<!-- page 46 -->

[8] Haryadi S. Gunawi وMingzhe Hao وTanakorn Leesatapornwongsa وآخرون: «What Bugs Live in the Cloud?»، في 5th ACM Symposium on Cloud Computing (SoCC)، نوفمبر 2014. doi:10.1145/2670979.2670986

[9] Nelson Minar: «Leap Second Crashes Half the Internet»، somebits.com، 3 يوليو 2012. [10] Amazon Web Services: «Summary of the Amazon EC2 and Amazon RDS Service Disruption in the US East Region»، aws.amazon.com، 29 أبريل 2011. [11] Richard I. Cook: «How Complex Systems Fail»، Cognitive Technologies Laboratory، أبريل 2000. [12] Jay Kreps: «Getting Real About Distributed System Reliability»، blog.empathybox.com، 19 مارس 2012. [13] David Oppenheimer وArchana Ganapathi وDavid A. Patterson: «Why Do Internet Services Fail, and What Can Be Done About It?»، في 4th USENIX Symposium on Internet Technologies and Systems (USITS)، مارس 2003. [14] Nathan Marz: «Principles of Software Engineering, Part 1»، nathanmarz.com، 2 أبريل 2013. [15] Michael Jurewitz: «The Human Impact of Bugs»، jury.me، 15 مارس 2013. [16] Raffi Krikorian: «Timelines at Scale»، في QCon San Francisco، نوفمبر 2012. [17] Martin Fowler: Patterns of Enterprise Application Architecture. Addison Wesley، 2002. ISBN: 978-0-321-12742-6 [18] Kelly Sommers: «After all that run around, what caused 500ms disk latency even when we replaced physical server?»، twitter.com، 13 نوفمبر 2014. [19] Giuseppe DeCandida وDeniz Hastorun وMadan Jampani وآخرون: «Dynamo: Amazon's Highly Available Key-Value Store»، في 21st ACM Symposium on Operating Systems Principles (SOSP)، أكتوبر 2007. [20] Greg Linden: «Make Data Useful»، شرائح من عرض تقديمي في مادة Data Mining لجامعة Stanford University (CS345)، ديسمبر 2006. [21] Tammy Everts: «The Real Cost of Slow Time vs Downtime»، webperformancetoday.com، 12 نوفمبر 2014. [22] Jake Brutlag: «Speed Matters for Google Web Search»، googleresearch.blogspot.co.uk، 22 يونيو 2009. [23] Tyler Treat: «Everything You Know About Latency Is Wrong»، bravenewgeek.com، 12 ديسمبر 2015.

<!-- page 47 -->
