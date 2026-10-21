إن تكرار الموضوع نفسه مرارًا وتكرارًا أمر مُملّ إلى حدٍّ كبير، لكن لحسن الحظ يمكنك استخدام الفواصل المنقوطة (semicolons) لقول أشياء متعددة عن الموضوع نفسه. وهذا يجعل صيغة Turtle جميلة وسهلة القراءة إلى حدٍّ كبير: انظر المثال 2-7.

<!-- page 79 -->

vii. من الناحية التقنية، تستخدم Datomic 5-tuples بدلًا من triples؛ والحقلان الإضافيان هما metadata لتتبّع الإصدارات (versioning).

## المثال 2-7. طريقة أكثر إيجازًا لكتابة بيانات المثال 2-6

@prefix : <urn:example:>. _:lucy a :Person; :name "Lucy"; :bornIn _:idaho. _:idaho a :Location; :name "Idaho"; :type "state"; :within _:usa. _:usa a :Location; :name "United States"; :type "country"; :within _:namerica. _:namerica a :Location; :name "North America"; :type "continent".

## الويب الدلالي (semantic web)

إذا قرأت المزيد عن triple-stores، فقد تنجذب إلى دوّامة من المقالات المكتوبة عن الويب الدلالي (semantic web). ونموذج بيانات الـtriple-store مستقل تمامًا عن الويب الدلالي—فمثلًا، Datomic [40] هي triple-store لا تدّعي أن لها أي صلة به.vii لكن بما أن الاثنين مرتبطان على نحو وثيق في أذهان كثيرين، فينبغي لنا مناقشتهما بإيجاز.

الويب الدلالي (semantic web) هو في الأساس فكرة بسيطة ومعقولة: فمواقع الويب تنشر بالفعل معلومات في صورة نصوص وصور ليقرأها البشر، فلماذا لا تنشر أيضًا معلومات في صورة بيانات قابلة للقراءة آليًا (machine-readable data) لتقرأها الحواسيب؟ وكان المقصود من Resource Description Framework (RDF) [41] أن يكون آلية تتيح لمواقع ويب مختلفة نشر البيانات بصيغة متسقة، بحيث يمكن دمج بيانات مواقع الويب المختلفة تلقائيًا في شبكة من البيانات—أي نوعًا من «قاعدة بيانات لكل شيء» على نطاق الإنترنت.

للأسف، سُوِّق للويب الدلالي (semantic web) بشكل مبالغ فيه في مطلع عام 2000، لكنه لم يُظهر حتى الآن أي علامة على أن يتحقّق في الواقع العملي، وهو ما جعل كثيرين متشائمين منه. كما أنه عانى من وابل مُذهل من الاختصارات، ومن مقترحات معايير مفرطة في التعقيد، ومن التكبّر (hubris).

لكن إذا تجاوزت تلك المثالب، فهناك أيضًا الكثير من العمل الجيد الذي أنتجه مشروع الويب الدلالي (semantic web). ويمكن أن تكون الـtriples نموذج بيانات داخليًا جيدًا للتطبيقات، حتى لو لم يكن لديك أي اهتمام بنشر بيانات RDF على الويب الدلالي.

## نموذج بيانات RDF

لغة Turtle التي استخدمناها في المثال 2-7 هي صيغة قابلة للقراءة من قِبل البشر لبيانات RDF. وأحيانًا تُكتب RDF أيضًا بصيغة XML، وهو ما يؤدي الغرض نفسه بأسلوب أطول بكثير—انظر المثال 2-8. وTurtle/N3 هي الأفضل لأنها أسهل بكثير على العين، وأدوات مثل Apache Jena [42] تستطيع التحويل تلقائيًا بين صيغ RDF المختلفة عند الحاجة.

<!-- page 80 -->

## المثال 2-8. بيانات المثال 2-7، معبَّرة باستخدام صياغة RDF/XML

<rdf:RDF xmlns="urn:example:" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <Location rdf:nodeID="idaho"> <name>Idaho</name> <type>state</type> <within> <Location rdf:nodeID="usa"> <name>United States</name> <type>country</type> <within> <Location rdf:nodeID="namerica"> <name>North America</name> <type>continent</type> </Location> </within> </Location> </within> </Location> <Person rdf:nodeID="lucy"> <name>Lucy</name> <bornIn rdf:nodeID="idaho"/> </Person> </rdf:RDF>

تتمتع RDF ببعض السمات غير المعتادة، بسبب أنها مصمَّمة لتبادل البيانات على نطاق الإنترنت. فـsubject (الفاعل) وpredicate (المسند) وobject (المفعول) للـtriple تكون غالبًا URIs. فمثلًا قد يكون المسند URI مثل <http://my-company.com/namespace#within> أو <http://my-company.com/namespace#lives_in>، بدلًا من مجرد WITHIN أو LIVES_IN. والمنطق وراء هذا التصميم هو أنه ينبغي أن تستطيع أن تجمع بياناتك مع بيانات شخص آخر، وإذا حمل هو معنًى مختلفًا للكلمة within أو lives_in، فلن ينشأ تعارض لأن مسنداته في الواقع هي <http://other.org/foo#within> و<http://other.org/foo#lives_in>.

لا يحتاج URL <http://my-company.com/namespace> بالضرورة إلى أن يشير إلى أي شيء—فمن منظور RDF، هو ببساطة namespace. ولتجنّب الالتباس المحتمل مع URLs من نوع http://، تستخدم الأمثلة في هذا القسم URIs غير قابلة للحل مثل urn:example:within. ولحسن الحظ، يمكنك ببساطة أن تحدّد هذه البادئة (prefix) مرة واحدة في أعلى الملف ثم تنساه.

<!-- page 81 -->

## لغة الاستعلام SPARQL

SPARQL هي لغة استعلام لـtriple-stores تستخدم نموذج بيانات RDF [43]. (وهي اختصار لعبارة SPARQL Protocol and RDF Query Language، وتُنطق «sparkle».) وهي أقدم من Cypher، ولأن مطابقة الأنماط (pattern matching) في Cypher مستعارة من SPARQL، فإنهما يبدو متشابهين إلى حدٍّ كبير [37].

الاستعلام نفسه كما سبق—البحث عن أشخاص انتقلوا من الولايات المتحدة إلى أوروبا— هو أكثر إيجازًا في SPARQL حتى منه في Cypher (انظر المثال 2-9).

## المثال 2-9. الاستعلام نفسه الموجود في المثال 2-4، معبَّرًا عنه في SPARQL

PREFIX : <urn:example:>

SELECT ?personName WHERE { ?person :name ?personName. ?person :bornIn / :within* / :name "United States". ?person :livesIn / :within* / :name "Europe". }

البنية متشابهة جدًا. التعبيران التاليان متكافئان (تبدأ المتغيرات بعلامة الاستفهام في SPARQL):

(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location) # Cypher ?person :bornIn / :within* ?location. # SPARQL

لأن RDF لا تميّز بين properties وedges، وإنما تستخدم المسندات (predicates) لكليهما، يمكنك استخدام الصياغة نفسها في مطابقة properties. وفي التعبير التالي، يكون المتغير usa مرتبطًا بأي vertex لديه name property قيمتها هي السلسلة "United States":

(usa {name:'United States'}) # Cypher ?usa :name "United States". # SPARQL

SPARQL هي لغة استعلام جيدة—فحتى لو لم يتحقّق الويب الدلالي (semantic web) أبدًا، يمكن أن تكون أداة قوية تستخدمها التطبيقات داخليًا.

<!-- page 82 -->

viii. تستخدم Datomic وCascalog صياغة S-expression في Clojure لـDatalog. وفي الأمثلة التالية نستخدم صياغة Prolog، وهي أسهل قليلًا في القراءة، لكن هذا لا يُحدث أي فرق وظيفي.

## مقارنة قواعد بيانات الرسوم البيانية (graph databases) بالنموذج الشبكي

في «هل تُعيد قواعد بيانات المستندات تكرار التاريخ؟» في الصفحة 36، ناقشنا كيف تنافس CODASYL والنموذج العلائقي لحل مشكلة العلاقات many-to-many في IMS. وللوهلة الأولى يبدو النموذج الشبكي لـCODASYL مشابهًا للنموذج البياني (graph model). فهل قواعد بيانات الرسوم البيانية هي عودة CODASYL مرة أخرى في صورة مموّهة؟

لا. فهما يختلفان في عدة جوانب مهمة:

