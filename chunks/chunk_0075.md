However, having split the writes across different keys, any reads now have to do addi‐ tional work, as they have to read the data from all 100 keys and combine it. This tech‐ nique also requires additional bookkeeping: it only makes sense to append the random number for the small number of hot keys; for the vast majority of keys with low write throughput this would be unnecessary overhead. Thus, you also need some way of keeping track of which keys are being split.

Perhaps in the future, data systems will be able to automatically detect and compen‐ sate for skewed workloads; but for now, you need to think through the trade-offs for your own application.

<!-- page 228 -->

ii. If your database only supports a key-value model, you might be tempted to implement a secondary index yourself by creating a mapping from values to document IDs in application code. If you go down this route, you need to take great care to ensure your indexes remain consistent with the underlying data. Race condi‐ tions and intermittent write failures (where some changes were saved but others weren’t) can very easily cause the data to go out of sync—see “The need for multi-object transactions” on page 231.

## Partitioning and Secondary Indexes

The partitioning schemes we have discussed so far rely on a key-value data model. If records are only ever accessed via their primary key, we can determine the partition from that key and use it to route read and write requests to the partition responsible for that key.

The situation becomes more complicated if secondary indexes are involved (see also “Other Indexing Structures” on page 85). A secondary index usually doesn’t identify a record uniquely but rather is a way of searching for occurrences of a particular value: find all actions by user 123, find all articles containing the word hogwash, find all cars whose color is red, and so on.

Secondary indexes are the bread and butter of relational databases, and they are com‐ mon in document databases too. Many key-value stores (such as HBase and Volde‐ mort) have avoided secondary indexes because of their added implementation complexity, but some (such as Riak) have started adding them because they are so useful for data modeling. And finally, secondary indexes are the raison d’être of search servers such as Solr and Elasticsearch.

The problem with secondary indexes is that they don’t map neatly to partitions. There are two main approaches to partitioning a database with secondary indexes: document-based partitioning and term-based partitioning.

## Partitioning Secondary Indexes by Document

For example, imagine you are operating a website for selling used cars (illustrated in Figure 6-4). Each listing has a unique ID—call it the document ID—and you partition the database by the document ID (for example, IDs 0 to 499 in partition 0, IDs 500 to 999 in partition 1, etc.).

You want to let users search for cars, allowing them to filter by color and by make, so you need a secondary index on color and make (in a document database these would be fields; in a relational database they would be columns). If you have declared the index, the database can perform the indexing automatically.ii For example, whenever a red car is added to the database, the database partition automatically adds it to the list of document IDs for the index entry color:red.

<!-- page 229 -->

Partition 0

## Partition 1

<table>
<tr><th colspan="2">PRIMARY KEY INDEX</th><th colspan="2">PRIMARY KEY INDEX</th></tr>
<tr><td colspan="2">191 → (color:“red”,</td><td colspan="2">515 → {color:”silver”, make:“Ford”, location:”Milpitas”)</td></tr>
<tr><td colspan="2">214 → {color:“black”, make:“Dodge”, location:“San Jose”}</td><td colspan="2">768 → (color:“red”,</td></tr>
<tr><td colspan="2">306 → (color: “red”,</td><td colspan="2">893 → {color:“silver”, make:“Audi”, location:“Santa Clara”}</td></tr>
<tr><td colspan="2">SECONDARY INDEXES (Partitioned by document)</td><td colspan="2">SECONDARY INDEXES (Partitioned by document)</td></tr>
<tr><td>color:black</td><td>→ [214]</td><td>color:black</td><td>→ 0</td></tr>
<tr><td>color:red</td><td>→ [191, 306] &lt;{</td><td>- color:red</td><td>→ [768]</td></tr>
<tr><td>color:yellow</td><td>→ []</td><td>color:silver</td><td>→ [515, 893]</td></tr>
<tr><td colspan="2">make:Dodge → [214]</td><td>make:Audi</td><td>→ [893]</td></tr>
<tr><td>make:Ford</td><td>→ [306]</td><td>make:Ford</td><td>→ [515]</td></tr>
<tr><td>make:Honda</td><td>→ [191]</td><td>make:Volvo</td><td>→ [768]</td></tr>
<tr><td></td><td></td><td colspan="2">scatter/gather read from all partitions</td></tr>
<tr><td></td><td></td><td colspan="2">“I am looking for a red car”</td></tr>
</table>

Figure 6-4. Partitioning secondary indexes by document.

In this indexing approach, each partition is completely separate: each partition main‐ tains its own secondary indexes, covering only the documents in that partition. It doesn’t care what data is stored in other partitions. Whenever you need to write to the database—to add, remove, or update a document—you only need to deal with the partition that contains the document ID that you are writing. For that reason, a document-partitioned index is also known as a local index (as opposed to a global index, described in the next section).

However, reading from a document-partitioned index requires care: unless you have done something special with the document IDs, there is no reason why all the cars with a particular color or a particular make would be in the same partition. In Figure 6-4, red cars appear in both partition 0 and partition 1. Thus, if you want to search for red cars, you need to send the query to all partitions, and combine all the results you get back.

This approach to querying a partitioned database is sometimes known as scatter/ gather, and it can make read queries on secondary indexes quite expensive. Even if you query the partitions in parallel, scatter/gather is prone to tail latency amplifica‐ tion (see “Percentiles in Practice” on page 16). Nevertheless, it is widely used: Mon‐ goDB, Riak [15], Cassandra [16], Elasticsearch [17], SolrCloud [18], and VoltDB [19] all use document-partitioned secondary indexes. Most database vendors recommend that you structure your partitioning scheme so that secondary index queries can be served from a single partition, but that is not always possible, especially when you’re using multiple secondary indexes in a single query (such as filtering cars by color and by make at the same time).

<!-- page 230 -->

## Partition 0

## Partition 1

<table>
<tr><th colspan="2">PRIMARY KEY INDEX</th><th></th><th colspan="2">PRIMARY KEY INDEX</th></tr>
<tr><td>191 → (color:“red”,</td><td></td><td>make:“Honda”, location:“Palo Alto”}</td><td colspan="2">515 → {color:”silver”, make:“Ford”, location:“Milpitas”)</td></tr>
<tr><td colspan="3">214 → {color:"black”, make:“Dodge”, location:“San Jose”}</td><td colspan="2">768 → (color:”red”,</td></tr>
<tr><td colspan="2">306 → (color: “red”,</td><td>location:“Sunnyvale”} make:“Ford”,</td><td colspan="2">893 → (color:“silver”, make:“Audi”, location:“Santa Clara”) •</td></tr>
<tr><td></td><td></td><td></td><td></td><td>-</td></tr>
<tr><td colspan="3">SECONDARY INDEXES (Partitioned by term)</td><td colspan="2">\¿SECONDARY INDEXES (Partitioned by term)</td></tr>
<tr><td>color:black</td><td>→ [214]</td><td></td><td>color:silver</td><td>→ [515, 893]</td></tr>
<tr><td>color:red</td><td colspan="2">→ [191, 306, 768] «</td><td>color.yellow</td><td>→ []</td></tr>
<tr><td>make:Audi</td><td>→ [893] (</td><td>----</td><td>make:Honda</td><td>→ [191]</td></tr>
<tr><td>make:Do</td><td>→ [214]</td><td></td><td>make:Volvo</td><td>→ [768]</td></tr>
<tr><td>make:Ford</td><td>[306, 515]</td><td></td><td></td><td></td></tr>
</table>

“I am looking for a red car”

Figure 6-5. Partitioning secondary indexes by term.

## Partitioning Secondary Indexes by Term

