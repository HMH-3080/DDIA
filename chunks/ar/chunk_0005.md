معظم ما نتناوله في هذا الكتاب قيل من قبل بشكل أو بآخر—في عروض المؤتمرات، والأوراق البحثية، ومنشورات المدونات، والشيفرة، وأنظمة تتبّع الأخطاء، وقوائم البريد الإلكتروني، والموروثات الهندسية. يلخّص هذا الكتاب أهم الأفكار من مصادر مختلفة كثيرة، ويتضمّن في أنحاء النص إشارات إلى الأدبيات الأصلية. والمراجع في نهاية كل فصل مورد ممتاز إن أردت استكشاف مجال بعمق أكبر، ومعظمها متاح مجانًا على الإنترنت.

## O’Reilly Safari

Safari (المعروف سابقًا باسم Safari Books Online) هو منصة تدريب ومرجعية قائمة على الاشتراك، موجّهة للمؤسسات والحكومات والمعلمين والأفراد.

يحصل الأعضاء على الوصول إلى آلاف الكتب، ومقاطع التدريب، ومسارات التعلّم (Learning Paths)، والدروس التفاعلية، وقوائم التشغيل المنتقاة من أكثر من 250 ناشرًا، من بينهم O’Reilly Media وHarvard Business Review وPrentice Hall Professional وAddison-Wesley Professional وMicrosoft Press وSams وQue وPeachpit Press وAdobe وFocal Press وCisco Press وJohn Wiley & Sons وSyngress وMorgan Kaufmann وIBM Redbooks وPackt وAdobe Press وFT Press وApress وManning وNew Riders وMcGraw-Hill وJones & Bartlett وCourse Technology، وغيرها.

لمزيد من المعلومات، يرجى زيارة http://oreilly.com/safari.

<!-- page 20 -->

## كيف تتواصل معنا

يُرجى توجيه الملاحظات والأسئلة المتعلقة بهذا الكتاب إلى الناشر:

O’Reilly Media, Inc.

1005 Gravenstein Highway North Sebastopol, CA 95472 800-998-9938 (في الولايات المتحدة أو كندا) 707-829-0515 (دوليًا أو محليًا) 707-829-0104 (فاكس)

لدينا صفحة ويب لهذا الكتاب، نُدرج فيها الأخطاء الطباعية (errata) والأمثلة وأي معلومات إضافية. ويمكنك الوصول إلى هذه الصفحة على http://bit.ly/designing-data-intensive-apps.

للتعليق أو لطرح أسئلة تقنية حول هذا الكتاب، أرسل رسالة بريد إلكتروني إلى bookquestions@oreilly.com.

لمزيد من المعلومات عن كتبنا ودوراتنا ومؤتمراتنا وأخبارنا، راجع موقعنا الإلكتروني على http://www.oreilly.com.

ابحث عنا على Facebook: http://facebook.com/oreilly

تابعنا على Twitter: http://twitter.com/oreillymedia

شاهدنا على YouTube: http://www.youtube.com/oreillymedia

## شكر وتقدير

هذا الكتاب تجميعٌ ومنهَجةٌ لأعداد كبيرة من أفكار الآخرين ومعارفهم، يجمع بين خبرة البحث الأكاديمي والممارسة الصناعية. وفي عالم الحوسبة نميل إلى الانجذاب إلى الأشياء الجديدة اللامعة، لكنني أعتقد أن لدينا الكثير لتعلّمه من الأشياء التي أُنجزت من قبل. ويضم هذا الكتاب أكثر من 800 مرجع إلى مقالات، ومنشورات مدونات، ومحاضرات، وتوثيق، وغيرها، وكانت مصدر تعلّم لا يقدَّر ثمنه بالنسبة لي. وأنا ممتنّ جدًا لمؤلفي هذه المادة لمشاركتهم معرفتهم.

لقد تعلّمت الكثير أيضًا من المحادثات الشخصية، بفضل أعداد كبيرة من الأشخاص الذين استثمروا وقتهم في مناقشة الأفكار أو شرح الأمور لي بصبر. وبشكل خاص، أودّ أن أشكر Joe Adler وRoss Anderson وPeter Bailis وMárton Balassi وAlastair Beresford وMark Callaghan وMat Clayton وPatrick Collison وSean Cribbs وShirshanka Das وNiklas Ekström وStephan Ewen وAlan Fekete وGyula Fóra وCamille Fournier وAndres Freund وJohn Garbutt وSeth Gilbert وTom Haggett وPat Helland وJoe Hellerstein وJakob Homan وHeidi Howard وJohn Hugg وJulian Hyde وConrad Irwin وEvan Jones وFlavio Junqueira وJessica Kerr وKyle Kingsbury وJay Kreps وCarl Lerche وNicolas Liochon وSteve Loughran وLee Mallabone وNathan Marz وCaitie

<!-- page 21 -->

McCaffrey، Josie McLellan، Christopher Meiklejohn، Ian Meyers، Neha Narkhede، Neha Narula، Cathy O’Neil، Onora O’Neill، Ludovic Orban، Zoran Perkov، Julia Powles، Chris Riccomini، Henry Robinson، David Rosenthal، Jennifer Rullmann، Matthew Sackman، Martin Scholl، Amit Sela، Gwen Shapira، Greg Spurrier، Sam Stokes، Ben Stopford، Tom Stuart، Diana Vasile، Rahul Vohra، Pete Warden، وBrett Wooldridge.

وقد كان هناك أشخاص عديدون آخرون لا يقدَّر ثمنهم في كتابة هذا الكتاب لمراجعتهم المسودات وتقديم الملاحظات. ولكل هذه المساهمات، أنا مدينٌ بامتنان خاص إلى Raul Agepati وTyler Akidau وMattias Andersson وSasha Baranov وVeena Basavaraj وDavid Beyer وJim Brikman وPaul Carey وRaul Castro Fernandez وJoseph Chow وDerek Elkins وSam Elliott وAlexander Gallego وMark Grover وStu Halloway وHeidi Howard وNicola Kleppmann وStefan Kruppa وBjorn Madsen وSander Mak وStefan Podkowinski وPhil Potter وHamid Ramazani وSam Stokes وBen Summers. وبالطبع فإنني أحمل كامل المسؤولية عن أي أخطاء متبقية أو آراء غير مقبولة في هذا الكتاب.

ولأن ساعدوني في جعل هذا الكتاب حقيقةً ملموسة، ولتحمّلهم صبري مع كتابتي البطيئة وطلباتي غير المعتادة، أنا ممتن لمحرري Marie Beaugureau وMike Loukides وAnn Spencer، وكل فريق O’Reilly. ولأن ساعدوني في إيجاد الكلمات المناسبة، أشكر Rachel Head. ولأن منحوني الوقت والحرية للكتابة رغم الالتزامات الأخرى بـ العمل، أشكر Alastair Beresford وSusan Goodhue وNeha Narkhede وKevin Scott.

تستحق Shabbir Diwan وEdie Freedman شكرًا خاصًا جدًا، فقد رَسَما بعناية بالغة الخرائط المرافقة للفصول. ومن الجميل أنهما تبنّيا الفكرة غير المعتادة الخاصة بإنشاء الخرائط، وجعلاها جميلة ومقنعة إلى هذا الحد.

وأخيرًا، يتحوّل حبي إلى عائلتي وأصدقائي، الذين ما كنت لأستطيع بدونهم أن أتجاوز هذه عملية الكتابة التي استغرقت قرابة أربع سنوات. أنتم الأفضل.

<!-- page 22 -->

<!-- page 23 -->

## أسس أنظمة البيانات

تتناول الفصول الأربعة الأولى الأفكار الجوهرية التي تنطبق على جميع أنظمة البيانات، سواء عملت على جهاز واحد أو وُزّعت على cluster من الأجهزة:

1. يقدّم الفصل 1 المصطلحات والمقاربة التي سنستخدمها في أنحاء هذا الكتاب. وهو يفحص ما نعنيه فعليًا بكلمات مثل الموثوقية (reliability)، وقابلية التوسّع (scalability)، وقابلية الصيانة (maintainability)، وكيف يمكننا السعي إلى تحقيق هذه الأهداف.
2. يقارن الفصل 2 عدة نماذج بيانات (data models) ولغات استعلام (query languages) مختلفة—وهي أكثر العوامل تمييزًا وضوحًا بين قواعد البيانات من وجهة نظر المطوّر. وسنرى كيف تكون النماذج المختلفة مناسبة لمواقف مختلفة.
3. يتناول الفصل 3 التفاصيل الداخلية لمحرّكات التخزين وينظر في كيفية ترتيب قواعد البيانات للبيانات على القرص. فمحرّكات التخزين المختلفة مُحسَّنة لأحمال عمل (workloads) مختلفة، واختيار المحرك المناسب قد يكون له تأثير هائل على الأداء.
4. يقارن الفصل 4 صيغًا مختلفة لترميز البيانات (data encoding/serialization)، ويفحص خصوصًا مدى نجاحها في بيئة تتغيّر فيها متطلبات التطبيق وتحتاج فيها المخططات (schemas) إلى التكيّف مع مرور الوقت.

وفي وقت لاحق، سيتناول الجزء الثاني (Part II) المسائل الخاصة بأنظمة البيانات الموزّعة.

<!-- page 24 -->

## ES I G N I NG تطبيقات كثيفة البيانات*

الأفكار الكبرى وراء أنظمة موثوقة وقابلة للتوسّع وقابلة للصيانة /

• 15

IAINTAINAB1

## ALABILIT

RelIAbilITý

SCAlaBilITy / قياس load | & performance .

<table>
<tr><th></th><th></th></tr>
<tr><td></td><td></td></tr>
</table>

<table>
<tr><th>تحمّل</th><th></th></tr>
<tr><td>الأجهزة &amp;</td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td>أعطال البرمجيات</td><td></td></tr>
<tr><td>الخطأ البشري</td><td>Latency</td></tr>
<tr><td></td><td>percentiles,</td></tr>
<tr><td></td><td>throughput</td></tr>
<tr><td></td><td>3</td></tr>
</table>

lAINTAINABILT1 قابلية التشغيل، والبساطة، وقابلية التطوّر

<!-- page 25 -->

الفصل 1

## تطبيقات موثوقة وقابلة للتوسّع وقابلة للصيانة
