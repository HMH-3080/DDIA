JSON أقل إسهابًا من XML، لكن كليهما لا يزالان يستهلكان مساحة كبيرة مقارنةً بالصيغ الثنائية (binary formats). وقد أدت هذه الملاحظة إلى ظهور كمٍّ كبير من الترميزات الثنائية (binary encodings) الخاصة بـJSON (MessagePack، BSON، BJSON، UBJSON، BISON، وSmile، على سبيل ذكر بعض الأسماء) والخاصة بـXML (مثل WBXML وFast Infoset). وقد تبنّت هذه الصيغ في مجالات مختلفة، لكن أيًّا منها لم يحظِ بالانتشار الواسع الذي حظيت به الصيغ النصية لـJSON وXML.

توسّع بعض هذه الصيغ مجموعة أنواع البيانات (datatypes) (مثل التمييز بين الأعداد الصحيحة (integers) والأعداد العشرية العائمة (floating-point numbers)، أو إضافة دعم للنصوص الثنائية (binary strings))، لكنها تحافظ فيما عدا ذلك على نموذج بيانات JSON/XML دون تغيير. وبشكل خاص، بما أنها لا تفرض أي schema، فإنها تحتاج إلى تضمين جميع أسماء حقول الـobject ضمن البيانات المرمَّزة. أي أنها في الترميز الثنائي لمستند JSON الوارد في المثال 4-1 ستحتاج إلى تضمين النصوص userName وfavoriteNumber وinterests في مكان ما.

<!-- page 138 -->

المثال 4-1. سجل مثال سنرمّزه في عدة صيغ ثنائية في هذا الفصل

{ "userName": "Martin", "favoriteNumber": 1337, "interests": ["daydreaming", "hacking"] }

لننظر إلى مثال على MessagePack، وهو ترميز ثنائي لـJSON. ويوضح الشكل 4-1 تسلسل البايتات الذي تحصل عليه إذا رمّزت مستند JSON في المثال 4-1 باستخدام MessagePack [14]. أول بضعة بايتات هي كما يلي:

1. البايت الأول، 0x83، يدل على أن ما يلي هو object (أربع بتات عليا = 0x80) ذو ثلاثة حقول (أربع بتات سفلية = 0x03). (في حال كنت تتساءل عمّا يحدث إذا كان لـobject أكثر من 15 حقلًا، بحيث لا يتسع عدد الحقول في أربع بتات، فإنه حينها يحصل على مؤشر نوع مختلف، ويُرمَّز عدد الحقول في بايتين أو أربعة بايتات.)
2. البايت الثاني، 0xa8، يدل على أن ما يلي هو string (أربع بتات عليا = 0xa0) طوله ثمانية بايتات (أربع بتات سفلية = 0x08).
3. البايتات الثمانية التالية هي اسم الحقل userName بترميز ASCII. وبما أن الطول قد أُشير إليه سابقًا، فلا حاجة إلى أي marker يخبرنا بمكان انتهاء النص (ولا إلى أي escaping).
4. البايتات السبعة التالية ترمّز قيمة النص Martin المكوّنة من ستة أحرف مع بادئة 0xa6، وهكذا.

الترميز الثنائي يبلغ طوله 66 بايت، وهو أقل قليلًا فقط من الـ81 بايت التي يستهلكها الترميز النصي لـJSON (بعد إزالة المسافات البيضاء). وجميع الترميزات الثنائية لـJSON متشابهة في هذا الصدد. ومن غير الواضح ما إذا كان هذا الانخفاض الصغير في المساحة (وربما تسريع في parsing) يستحق فقدان سهولة القراءة من قِبل البشر.

في الأقسام التالية سنرى كيف يمكننا أن نُحسِّن الأمر كثيرًا، وأن نرمّز السجل نفسه في 32 بايت فقط.

<!-- page 139 -->

## MessagePack

تسلسل البايتات (66 بايت):

83 a8 75 73 65 72 4e 61 6d 65 a6 4d 61 72 74 69 6e ae 66 61 76 6£ 72 69 74 65 4e 75 6d 62 65 72 cd 05 39 a9 69 6e 74 65 72 65 73 74 73 92 ab 64 61 79 64 72 65 61 6d 69 6e 67 a7 68

61 63 6b 69 6e 67

التفصيل:

<table>
<tr><th>object</th><th>string</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th>string</th><th></th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td>(3 مدخلات)</td><td>◦ (الطول 8)</td><td>u</td><td>s</td><td>e</td><td>N</td><td>a</td><td>m</td><td>e</td><td>(الطول 6)</td><td>M</td><td>a</td><td>x</td><td>七</td><td>-i</td><td>n</td></tr>
<tr><td>83</td><td>a8</td><td colspan="5">75 73 65 72 4e 61</td><td colspan="2">6d 65</td><td>a6</td><td colspan="6">4d 61 72 74 69 6e</td></tr>
<tr><td></td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>(الطول 14)</td><td>f</td><td>a</td><td>v o</td><td></td><td></td><td>t</td><td>e</td><td>N m u</td><td>b</td><td>e</td><td>x</td><td></td><td></td><td></td></tr>
<tr><td></td><td>ae</td><td colspan="11">66 61 76 6f 72 69 74 65 4e 75 6d 62 65 72</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>uint16</td><td colspan="2">1337</td><td>(الطول 9)</td><td></td><td>i</td><td>n</td><td>t</td><td>e x e</td><td>s</td><td>t</td><td>s</td><td></td><td></td><td></td></tr>
<tr><td></td><td>cd</td><td colspan="2">05 39</td><td>a9</td><td></td><td colspan="7">69 66 74 65 72 65 73 74 73</td><td></td><td></td></tr>
<tr><td>array</td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td colspan="2">(2 مدخلات) (الطول 11)</td><td>d</td><td>a</td><td>d y</td><td>x</td><td>e</td><td>a</td><td>m</td><td>n</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>92.</td><td>ab</td><td colspan="8">64 61 79 64 72 65 61 6d 69 6e 67</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>(الطول 7)</td><td>h</td><td>a</td><td>c k</td><td>1</td><td>n</td><td>g</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>a7</td><td colspan="6">68 61 63 6b 69 6e 67</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
</table>

الشكل 4-1. سجل المثال (المثال 4-1) مرمَّزًا باستخدام MessagePack.

## Thrift وProtocol Buffers

Apache Thrift [15] وProtocol Buffers (protobuf) [16] هما مكتبتا ترميز ثنائي مبنيتان على المبدأ نفسه. فقد طُوِّر Protocol Buffers في الأصل في Google، وطُوِّر Thrift في الأصل في Facebook، وأصبح كلاهما مفتوح المصدر في 2007–08 [17].

يتطلب كل من Thrift وProtocol Buffers وجود schema لأي بيانات يتم ترميزها. ولترميز بيانات المثال 4-1 في Thrift، تصف الـschema بلغة تعريف واجهات Thrift (Thrift interface definition language, IDL) على النحو التالي:

struct Person { 1: required string 2: optional i64 userName, favoriteNumber, 3: optional list<string> interests }

<!-- page 140 -->

تعريف الـschema المكافئ لـProtocol Buffers يبدو مشابهًا جدًا:

message Person { required string user_name = 1; optional int64 favorite_number = 2; } repeated string interests = 3;

يأتي كل من Thrift وProtocol Buffers مع أداة توليد شيفرة (code generation tool) تأخذ تعريف schema مثل المعروض هنا، وتُنتج أصنافًا (classes) تُنفّذ الـschema بلغات برمجة مختلفة [18]. ويمكن لشيفرة تطبيقك أن تستدعي هذه الشيفرة المولَّدة لترميز سجلات الـschema أو فكّ ترميزها.

كيف تبدو البيانات المرمَّزة بهذا الـschema؟ وإرباكًا، فإن Thrift له صيغتا ترميز ثنائي مختلفتان،iii تُسمَّيان على التوالي BinaryProtocol وCompactProtocol. لننظر أولًا إلى BinaryProtocol. يستغرق ترميز المثال 4-1 في تلك الصيغة 59 بايت، كما هو موضح في الشكل 4-2 [19].

Thrift BinaryProtocol

تسلسل البايتات (59 بايت):

0b 00 01 00 00 00 06 4d 61 72 74 69 6e 0a 00 02 00 00 00 00 00 00 05 39 0 00 03 0b 00 00 00 02 00 00 00 0b 64 61 79 64 72 65 61 6d 69 6e 67 00 00 00 07 68 61 63 6b 69 6e 67 00

التفصيل:

<table>
<tr><th>وسم الحقل = 1 النوع 11 (string)  f الطول 6</th><th>M.</th><th>a</th><th></th><th>t</th><th>i</th><th>n</th><th></th><th></th><th></th></tr>
<tr><td>00 01 00 00 00 06 0b</td><td colspan="6">4d 61 72 74 69 6e</td><td></td><td></td><td></td></tr>
<tr><td>1337 وسم الحقل = 2 النوع 10 (i64)</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td colspan="4">00 02 00 00 00 00 00 00 05 39 Oa</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>وسم الحقل = 3 نوع العنصر 11 (string) النوع 15 (list)</td><td></td><td colspan="2">2 عنصرًا في list</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>00 03 0f 0b</td><td colspan="4">00 00 00 02</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>الطول 11</td><td>d.</td><td>a</td><td>y</td><td>d</td><td>x</td><td>e</td><td>a</td><td>n</td><td>g</td></tr>
<tr><td>00 00 00 0&gt;</td><td colspan="9">64 61 79 64 72 65 61 6d 69 6e 67</td></tr>
<tr><td>الطول 7</td><td>h</td><td>a</td><td>c</td><td>k</td><td>1.</td><td>n</td><td>g</td><td colspan="2">نهاية struct</td></tr>
<tr><td>00 00 00 07</td><td colspan="7">68 61 63 6b 69 6e 67</td><td>00</td><td></td></tr>
</table>

الشكل 4-2. سجل المثال مرمَّزًا باستخدام BinaryProtocol الخاص بـThrift.

iii. في الواقع، له ثلاث صيغ—BinaryProtocol وCompactProtocol وDenseProtocol—غير أن DenseProtocol مدعوم فقط في تنفيذ C++، لذا لا يُحتسب ضمن الصيغ متعددة اللغات [18]. وإلى جانب هذه الصيغ، لديه أيضًا صيغتا ترميز مختلفتان قائمتان على JSON [19]. يا لها من متعة!

<!-- page 141 -->
