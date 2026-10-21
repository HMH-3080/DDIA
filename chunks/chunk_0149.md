In many datasets it is common for one record to have an association with another record: a foreign key in a relational model, a document reference in a document model, or an edge in a graph model. A join is necessary whenever you have some code that needs to access records on both sides of that association (both the record that holds the reference and the record being referenced). As discussed in Chapter 2, denormalization can reduce the need for joins but generally not remove it entirely.v In a database, if you execute a query that involves only a small number of records, the database will typically use an index to quickly locate the records of interest (see Chap‐ ter 3). If the query involves joins, it may require multiple index lookups. However, MapReduce has no concept of indexes—at least not in the usual sense.

When a MapReduce job is given a set of files as input, it reads the entire content of all of those files; a database would call this operation a full table scan. If you only want to read a small number of records, a full table scan is outrageously expensive compared to an index lookup. However, in analytic queries (see “Transaction Processing or Analytics?” on page 90) it is common to want to calculate aggregates over a large number of records. In this case, scanning the entire input might be quite a reasonable thing to do, especially if you can parallelize the processing across multiple machines.

<!-- page 426 -->

When we talk about joins in the context of batch processing, we mean resolving all occurrences of some association within a dataset. For example, we assume that a job is processing the data for all users simultaneously, not merely looking up the data for one particular user (which would be done far more efficiently with an index).

## Example: analysis of user activity events

A typical example of a join in a batch job is illustrated in Figure 10-2. On the left is a log of events describing the things that logged-in users did on a website (known as activity events or clickstream data), and on the right is a database of users. You can think of this example as being part of a star schema (see “Stars and Snowflakes: Sche‐ mas for Analytics” on page 93): the log of events is the fact table, and the user data‐ base is one of the dimensions.

<table>
<tr><th>User activity events</th><th colspan="2">User database</th><th></th></tr>
<tr><td>user 105 clicked button .… to load URL .</td><td>user_id email</td><td></td><td>date_of_birth</td></tr>
<tr><td>user 296 viewed the profile of user 134</td><td>100</td><td>atilla@example.com</td><td>1991-02-15</td></tr>
<tr><td>user 251 logged out from browser session …</td><td>101</td><td>beth@foo.com</td><td>1952-06-29</td></tr>
<tr><td>user 184 loaded page with URL .</td><td>102</td><td>chunzhi@test.net</td><td>1967-09-08</td></tr>
<tr><td>user 101 posted a response to message ..</td><td>103</td><td>devaraj@example.net</td><td>1947-12-18</td></tr>
<tr><td>user 156 clicked the help button on page .…</td><td>104</td><td>evelyn@example.com</td><td>1989-01-30</td></tr>
<tr><td>user 301 clicked a link in email ..</td><td>05</td><td>flavio@foo.com</td><td>1971-05-05</td></tr>
<tr><td>user 123 searched for the keyword …</td><td></td><td></td><td></td></tr>
</table>

Figure 10-2. A join between a log of user activity events and a database of user profiles. An analytics task may need to correlate user activity with user profile information: for example, if the profile contains the user’s age or date of birth, the system could determine which pages are most popular with which age groups. However, the activ‐ ity events contain only the user ID, not the full user profile information. Embedding that profile information in every single activity event would most likely be too waste‐ ful. Therefore, the activity events need to be joined with the user profile database.

The simplest implementation of this join would go over the activity events one by one and query the user database (on a remote server) for every user ID it encounters. This is possible, but it would most likely suffer from very poor performance: the pro‐ cessing throughput would be limited by the round-trip time to the database server, the effectiveness of a local cache would depend very much on the distribution of data, and running a large number of queries in parallel could easily overwhelm the data‐ base [35].

<!-- page 427 -->

In order to achieve good throughput in a batch process, the computation must be (as much as possible) local to one machine. Making random-access requests over the network for every record you want to process is too slow. Moreover, querying a remote database would mean that the batch job becomes nondeterministic, because the data in the remote database might change.

Thus, a better approach would be to take a copy of the user database (for example, extracted from a database backup using an ETL process—see “Data Warehousing” on page 91) and to put it in the same distributed filesystem as the log of user activity events. You would then have the user database in one set of files in HDFS and the user activity records in another set of files, and could use MapReduce to bring together all of the relevant records in the same place and process them efficiently.

## Sort-merge joins

Recall that the purpose of the mapper is to extract a key and value from each input record. In the case of Figure 10-2, this key would be the user ID: one set of mappers would go over the activity events (extracting the user ID as the key and the activity event as the value), while another set of mappers would go over the user database (extracting the user ID as the key and the user’s date of birth as the value). This pro‐ cess is illustrated in Figure 10-3.

## User activity mapper

<table>
<tr><th>user 104 loaded URL /x</th></tr>
<tr><td>user 173 loaded URL /y</td></tr>
<tr><td>user 104 loaded URL /z</td></tr>
</table>

Reducer partition 1 d user IDs) dob

## User database mapper

<table>
<tr><th>{user_id: 103,</th><th></th></tr>
<tr><td>email: devaraj@example.net,</td><td></td></tr>
<tr><td>104 → dob: 1989 date_of_birth: 1947-12-18)</td><td>Reducer partition 2</td></tr>
<tr><td>{user_id: 104,</td><td>nbered u dd-nu</td></tr>
<tr><td>03  dob: 194</td><td></td></tr>
<tr><td>email: evelyn@example.com,</td><td></td></tr>
<tr><td>date_of_birth: 1989-01-30)</td><td></td></tr>
</table>

Figure 10-3. A reduce-side sort-merge join on user ID. If the input datasets are parti‐ tioned into multiple files, each could be processed with multiple mappers in parallel.

When the MapReduce framework partitions the mapper output by key and then sorts the key-value pairs, the effect is that all the activity events and the user record with the same user ID become adjacent to each other in the reducer input. The Map‐ Reduce job can even arrange the records to be sorted such that the reducer always

<!-- page 428 -->

sees the record from the user database first, followed by the activity events in time‐ stamp order—this technique is known as a secondary sort [26].

