We talked about forward and backward compatibility, which are important for evolv‐ ability (making change easy by allowing you to upgrade different parts of your system independently, and not having to change everything at once). Compatibility is a rela‐ tionship between one process that encodes the data, and another process that decodes it.

<!-- page 151 -->

That’s a fairly abstract idea—there are many ways data can flow from one process to another. Who encodes the data, and who decodes it? In the rest of this chapter we will explore some of the most common ways how data flows between processes:

• Via databases (see “Dataflow Through Databases” on page 129)
• Via service calls (see “Dataflow Through Services: REST and RPC” on page 131)
• Via asynchronous message passing (see “Message-Passing Dataflow” on page 136)

## Dataflow Through Databases

In a database, the process that writes to the database encodes the data, and the pro‐ cess that reads from the database decodes it. There may just be a single process accessing the database, in which case the reader is simply a later version of the same process—in that case you can think of storing something in the database as sending a message to your future self.

Backward compatibility is clearly necessary here; otherwise your future self won’t be able to decode what you previously wrote.

In general, it’s common for several different processes to be accessing a database at the same time. Those processes might be several different applications or services, or they may simply be several instances of the same service (running in parallel for scal‐ ability or fault tolerance). Either way, in an environment where the application is changing, it is likely that some processes accessing the database will be running newer code and some will be running older code—for example because a new version is cur‐ rently being deployed in a rolling upgrade, so some instances have been updated while others haven’t yet.

This means that a value in the database may be written by a newer version of the code, and subsequently read by an older version of the code that is still running. Thus, forward compatibility is also often required for databases.

However, there is an additional snag. Say you add a field to a record schema, and the newer code writes a value for that new field to the database. Subsequently, an older version of the code (which doesn’t yet know about the new field) reads the record, updates it, and writes it back. In this situation, the desirable behavior is usually for the old code to keep the new field intact, even though it couldn’t be interpreted.

The encoding formats discussed previously support such preservation of unknown fields, but sometimes you need to take care at an application level, as illustrated in Figure 4-7. For example, if you decode a database value into model objects in the application, and later reencode those model objects, the unknown field might be lost in that translation process. Solving this is not a hard problem; you just need to be aware of it.

<!-- page 152 -->

<table>
<tr><th>public class Person {</th><th>Person person = db.read(…);</th></tr>
<tr><td>private String userName;</td><td>person.setFavoriteNumber(42);</td></tr>
<tr><td>Read and decode private Long favoriteNumber;</td><td>db.write(person.toJSON());</td></tr>
<tr><td>into model object</td><td></td></tr>
<tr><td>private List&lt;String&gt; interests;</td><td></td></tr>
<tr><td>// getters and setters…</td><td></td></tr>
<tr><td>}</td><td></td></tr>
<tr><td></td><td>Update, reencode</td></tr>
<tr><td>Old version of code (does not know</td><td>and write back</td></tr>
<tr><td>about photoURL field)</td><td></td></tr>
<tr><td>“userName”: “Martin”,</td><td>“userName”: “Martin”,</td></tr>
<tr><td>“favoriteNumber”: 1337, DB</td><td>“favoriteNumber”: 42</td></tr>
<tr><td>“interests”: [“hacking”],</td><td>“interests”: [“hacking”]</td></tr>
<tr><td>“photoURL”: “http://…”</td><td></td></tr>
<tr><td></td><td>Value of photoURL field is lost</td></tr>
<tr><td>Data written by new version of code</td><td></td></tr>
<tr><td>(including new photoURL field)</td><td></td></tr>
</table>

Figure 4-7. When an older version of the application updates data previously written by a newer version of the application, data may be lost if you’re not careful.

## Different values written at different times

A database generally allows any value to be updated at any time. This means that within a single database you may have some values that were written five milli‐ seconds ago, and some values that were written five years ago.

When you deploy a new version of your application (of a server-side application, at least), you may entirely replace the old version with the new version within a few minutes. The same is not true of database contents: the five-year-old data will still be there, in the original encoding, unless you have explicitly rewritten it since then. This observation is sometimes summed up as data outlives code.

Rewriting (migrating) data into a new schema is certainly possible, but it’s an expen‐ sive thing to do on a large dataset, so most databases avoid it if possible. Most rela‐ tional databases allow simple schema changes, such as adding a new column with a null default value, without rewriting existing data.v When an old row is read, the database fills in nulls for any columns that are missing from the encoded data on disk. LinkedIn’s document database Espresso uses Avro for storage, allowing it to use Avro’s schema evolution rules [23].

v. Except for MySQL, which often rewrites an entire table even though it is not strictly necessary, as men‐ tioned in “Schema flexibility in the document model” on page 39.

<!-- page 153 -->

Schema evolution thus allows the entire database to appear as if it was encoded with a single schema, even though the underlying storage may contain records encoded with various historical versions of the schema.

## Archival storage

Perhaps you take a snapshot of your database from time to time, say for backup pur‐ poses or for loading into a data warehouse (see “Data Warehousing” on page 91). In this case, the data dump will typically be encoded using the latest schema, even if the original encoding in the source database contained a mixture of schema versions from different eras. Since you’re copying the data anyway, you might as well encode the copy of the data consistently.

As the data dump is written in one go and is thereafter immutable, formats like Avro object container files are a good fit. This is also a good opportunity to encode the data in an analytics-friendly column-oriented format such as Parquet (see “Column Com‐ pression” on page 97).

In Chapter 10 we will talk more about using data in archival storage.

## Dataflow Through Services: REST and RPC

