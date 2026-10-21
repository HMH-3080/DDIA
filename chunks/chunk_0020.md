The SQL example doesn’t guarantee any particular ordering, and so it doesn’t mind if the order changes. But if the query is written as imperative code, the database can never be sure whether the code is relying on the ordering or not. The fact that SQL is more limited in functionality gives the database much more room for automatic opti‐ mizations.

Finally, declarative languages often lend themselves to parallel execution. Today, CPUs are getting faster by adding more cores, not by running at significantly higher clock speeds than before [31]. Imperative code is very hard to parallelize across mul‐ tiple cores and multiple machines, because it specifies instructions that must be per‐ formed in a particular order. Declarative languages have a better chance of getting faster in parallel execution because they specify only the pattern of the results, not the algorithm that is used to determine the results. The database is free to use a parallel implementation of the query language, if appropriate [32].

<!-- page 66 -->

## Declarative Queries on the Web

The advantages of declarative query languages are not limited to just databases. To illustrate the point, let’s compare declarative and imperative approaches in a com‐ pletely different environment: a web browser.

Say you have a website about animals in the ocean. The user is currently viewing the page on sharks, so you mark the navigation item “Sharks” as currently selected, like this:

<ul> <li class="selected"> <p>Sharks</p> <ul> <li>Great White Shark</li> <li>Tiger Shark</li> <li>Hammerhead Shark</li> </ul> </li> <li> <p>Whales</p> <ul> <li>Blue Whale</li> <li>Humpback Whale</li> <li>Fin Whale</li> </ul> </li> </ul>

The selected item is marked with the CSS class "selected".

<p>Sharks</p> is the title of the currently selected page.

Now say you want the title of the currently selected page to have a blue background, so that it is visually highlighted. This is easy, using CSS:

li.selected > p { background-color: blue; }

Here the CSS selector li.selected > p declares the pattern of elements to which we want to apply the blue style: namely, all <p> elements whose direct parent is an <li> element with a CSS class of selected. The element <p>Sharks</p> in the example matches this pattern, but <p>Whales</p> does not match because its <li> parent lacks class="selected".

<!-- page 67 -->

If you were using XSL instead of CSS, you could do something similar:

<xsl:template match="li[@class='selected']/p"> <fo:block background-color="blue"> <xsl:apply-templates/> </fo:block> </xsl:template>

Here, the XPath expression li[@class='selected']/p is equivalent to the CSS selec‐ tor li.selected > p in the previous example. What CSS and XSL have in common is that they are both declarative languages for specifying the styling of a document.

Imagine what life would be like if you had to use an imperative approach. In Java‐ Script, using the core Document Object Model (DOM) API, the result might look something like this:

var liElements = document.getElementsByTagName("li"); for (var i = 0; i < liElements.length; i++) { if (liElements[i].className === "selected") { var children = liElements[i].childNodes; for (var j = 0; j < children.length; j++) { var child = children[j]; if (child.nodeType === Node.ELEMENT_NODE && child.tagName === "P") { child.setAttribute("style", "background-color: blue"); } } } }

This JavaScript imperatively sets the element <p>Sharks</p> to have a blue back‐ ground, but the code is awful. Not only is it much longer and harder to understand than the CSS and XSL equivalents, but it also has some serious problems:

• If the selected class is removed (e.g., because the user clicks a different page), the blue color won’t be removed, even if the code is rerun—and so the item will remain highlighted until the entire page is reloaded. With CSS, the browser auto‐ matically detects when the li.selected > p rule no longer applies and removes the blue background as soon as the selected class is removed.
• If you want to take advantage of a new API, such as document.getElementsBy ClassName("selected") or even document.evaluate()—which may improve performance—you have to rewrite the code. On the other hand, browser vendors can improve the performance of CSS and XPath without breaking compatibility.

<!-- page 68 -->

vi. IMS and CODASYL both used imperative query APIs. Applications typically used COBOL code to iterate over records in the database, one record at a time [2, 16].

In a web browser, using declarative CSS styling is much better than manipulating styles imperatively in JavaScript. Similarly, in databases, declarative query languages like SQL turned out to be much better than imperative query APIs.vi

## MapReduce Querying

MapReduce is a programming model for processing large amounts of data in bulk across many machines, popularized by Google [33]. A limited form of MapReduce is supported by some NoSQL datastores, including MongoDB and CouchDB, as a mechanism for performing read-only queries across many documents.

MapReduce in general is described in more detail in Chapter 10. For now, we’ll just briefly discuss MongoDB’s use of the model.

MapReduce is neither a declarative query language nor a fully imperative query API, but somewhere in between: the logic of the query is expressed with snippets of code, which are called repeatedly by the processing framework. It is based on the map (also known as collect) and reduce (also known as fold or inject) functions that exist in many functional programming languages.

To give an example, imagine you are a marine biologist, and you add an observation record to your database every time you see animals in the ocean. Now you want to generate a report saying how many sharks you have sighted per month.

In PostgreSQL you might express that query like this:

SELECT date_trunc('month', observation_timestamp) AS observation_month, sum(num_animals) AS total_animals FROM observations WHERE family = 'Sharks' GROUP BY observation_month;

The date_trunc('month', timestamp) function determines the calendar month containing timestamp, and returns another timestamp representing the begin‐ ning of that month. In other words, it rounds a timestamp down to the nearest month.

This query first filters the observations to only show species in the Sharks family, then groups the observations by the calendar month in which they occurred, and finally adds up the number of animals seen in all observations in that month.

The same can be expressed with MongoDB’s MapReduce feature as follows:

<!-- page 69 -->

db.observations.mapReduce( function map() { var year = this.observationTimestamp.getFullYear(); var month = this.observationTimestamp.getMonth() + 1; emit(year + "-" + month, this.numAnimals); }, function reduce(key, values) { return Array.sum(values); }, { ); } query: { family: "Sharks" }, out: "monthlySharkReport"

