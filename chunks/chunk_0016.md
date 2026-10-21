The JSON representation has better locality than the multi-table schema in Figure 2-1. If you want to fetch a profile in the relational example, you need to either perform multiple queries (query each table by user_id) or perform a messy multiway join between the users table and its subordinate tables. In the JSON representa‐ tion, all the relevant information is in one place, and one query is sufficient.

The one-to-many relationships from the user profile to the user’s positions, educa‐ tional history, and contact information imply a tree structure in the data, and the JSON representation makes this tree structure explicit (see Figure 2-2).

ositio

b

Figure 2-2. One-to-many relationships forming a tree structure.

<!-- page 55 -->

ii. Literature on the relational model distinguishes several different normal forms, but the distinctions are of little practical interest. As a rule of thumb, if you’re duplicating values that could be stored in just one place, the schema is not normalized.

## Many-to-One and Many-to-Many Relationships

In Example 2-1 in the preceding section, region_id and industry_id are given as IDs, not as plain-text strings "Greater Seattle Area" and "Philanthropy". Why?

If the user interface has free-text fields for entering the region and the industry, it makes sense to store them as plain-text strings. But there are advantages to having standardized lists of geographic regions and industries, and letting users choose from a drop-down list or autocompleter:

• Consistent style and spelling across profiles
• Avoiding ambiguity (e.g., if there are several cities with the same name)
• Ease of updating—the name is stored in only one place, so it is easy to update across the board if it ever needs to be changed (e.g., change of a city name due to political events)
• Localization support—when the site is translated into other languages, the stand‐ ardized lists can be localized, so the region and industry can be displayed in the viewer’s language
• Better search—e.g., a search for philanthropists in the state of Washington can match this profile, because the list of regions can encode the fact that Seattle is in Washington (which is not apparent from the string "Greater Seattle Area")

Whether you store an ID or a text string is a question of duplication. When you use an ID, the information that is meaningful to humans (such as the word Philanthropy) is stored in only one place, and everything that refers to it uses an ID (which only has meaning within the database). When you store the text directly, you are duplicating the human-meaningful information in every record that uses it.

The advantage of using an ID is that because it has no meaning to humans, it never needs to change: the ID can remain the same, even if the information it identifies changes. Anything that is meaningful to humans may need to change sometime in the future—and if that information is duplicated, all the redundant copies need to be updated. That incurs write overheads, and risks inconsistencies (where some copies of the information are updated but others aren’t). Removing such duplication is the key idea behind normalization in databases.ii

<!-- page 56 -->

iii. At the time of writing, joins are supported in RethinkDB, not supported in MongoDB, and only sup‐ ported in predeclared views in CouchDB.

Database administrators and developers love to argue about nor‐ malization and denormalization, but we will suspend judgment for now. In Part III of this book we will return to this topic and explore systematic ways of dealing with caching, denormalization, and derived data.

Unfortunately, normalizing this data requires many-to-one relationships (many peo‐ ple live in one particular region, many people work in one particular industry), which don’t fit nicely into the document model. In relational databases, it’s normal to refer to rows in other tables by ID, because joins are easy. In document databases, joins are not needed for one-to-many tree structures, and support for joins is often weak.iii

If the database itself does not support joins, you have to emulate a join in application code by making multiple queries to the database. (In this case, the lists of regions and industries are probably small and slow-changing enough that the application can simply keep them in memory. But nevertheless, the work of making the join is shifted from the database to the application code.)

Moreover, even if the initial version of an application fits well in a join-free docu‐ ment model, data has a tendency of becoming more interconnected as features are added to applications. For example, consider some changes we could make to the résumé example:

## Organizations and schools as entities

In the previous description, organization (the company where the user worked) and school_name (where they studied) are just strings. Perhaps they should be references to entities instead? Then each organization, school, or university could have its own web page (with logo, news feed, etc.); each résumé could link to the organizations and schools that it mentions, and include their logos and other information (see Figure 2-3 for an example from LinkedIn).

## Recommendations

Say you want to add a new feature: one user can write a recommendation for another user. The recommendation is shown on the résumé of the user who was recommended, together with the name and photo of the user making the recom‐ mendation. If the recommender updates their photo, any recommendations they have written need to reflect the new photo. Therefore, the recommendation should have a reference to the author’s profile.

<!-- page 57 -->

xperience Co-chair Bill & Melinda Gates Foundation 2000 – Present (13 years) Co-founder.Chairman crosoft licroso help their full ery day

Figure 2-3. The company name is not just a string, but a link to a company entity. Screenshot of linkedin.com.

Figure 2-4 illustrates how these new features require many-to-many relationships. The data within each dotted rectangle can be grouped into one document, but the references to organizations, schools, and other users need to be represented as refer‐ ences, and require joins when queried.

## org 1

g

<table>
<tr><th>org 3</th><th>ositio</th></tr>
<tr><td>ob 2</td><td>job 2</td></tr>
<tr><td>job_title</td><td>job title w</td></tr>
<tr><td>rt</td><td></td></tr>
<tr><td></td><td>end 4</td></tr>
<tr><td>chool 1</td><td></td></tr>
<tr><td></td><td>educat</td></tr>
<tr><td></td><td>end</td></tr>
<tr><td></td><td>edu 2</td></tr>
</table>

hool 3

Figure 2-4. Extending résumés with many-to-many relationships.

<!-- page 58 -->

## Are Document Databases Repeating History?

While many-to-many relationships and joins are routinely used in relational data‐ bases, document databases and NoSQL reopened the debate on how best to represent such relationships in a database. This debate is much older than NoSQL—in fact, it goes back to the very earliest computerized database systems.

