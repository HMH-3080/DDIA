Each input file is typically hundreds of megabytes in size. The MapReduce scheduler (not shown in the diagram) tries to run each mapper on one of the machines that stores a replica of the input file, provided that machine has enough spare RAM and CPU resources to run the map task [26]. This principle is known as putting the com‐ putation near the data [27]: it saves copying the input file over the network, reducing network load and increasing locality.

<!-- page 423 -->

<table>
<tr><th>Map task 1</th><th></th><th>Reduce task 1</th><th></th></tr>
<tr><td></td><td></td><td>(m 1,r1</td><td></td></tr>
<tr><td></td><td></td><td>m2,r1}</td><td>Reduce &gt;</td></tr>
<tr><td></td><td></td><td></td><td>o</td></tr>
<tr><td>o</td><td></td><td></td><td></td></tr>
<tr><td>v</td><td></td><td></td><td>-</td></tr>
<tr><td>Map task 2</td><td></td><td>Reduce task 2</td><td>o</td></tr>
<tr><td></td><td>n 2, r 1</td><td>(m 1,r2)</td><td></td></tr>
<tr><td>Mapper</td><td>n2, r 2</td><td>(m2.12</td><td>- Reducer o</td></tr>
<tr><td></td><td>2, r 3</td><td>m 3, r</td><td></td></tr>
<tr><td></td><td></td><td></td><td>o</td></tr>
<tr><td></td><td></td><td>Reduce task 3</td><td></td></tr>
</table>

Figure 10-1. A MapReduce job with three mappers and three reducers.

In most cases, the application code that should run in the map task is not yet present on the machine that is assigned the task of running it, so the MapReduce framework first copies the code (e.g., JAR files in the case of a Java program) to the appropriate machines. It then starts the map task and begins reading the input file, passing one record at a time to the mapper callback. The output of the mapper consists of keyvalue pairs.

The reduce side of the computation is also partitioned. While the number of map tasks is determined by the number of input file blocks, the number of reduce tasks is configured by the job author (it can be different from the number of map tasks). To ensure that all key-value pairs with the same key end up at the same reducer, the framework uses a hash of the key to determine which reduce task should receive a particular key-value pair (see “Partitioning by Hash of Key” on page 203).

The key-value pairs must be sorted, but the dataset is likely too large to be sorted with a conventional sorting algorithm on a single machine. Instead, the sorting is per‐ formed in stages. First, each map task partitions its output by reducer, based on the hash of the key. Each of these partitions is written to a sorted file on the mapper’s local disk, using a technique similar to what we discussed in “SSTables and LSM- Trees” on page 76.

<!-- page 424 -->

Whenever a mapper finishes reading its input file and writing its sorted output files, the MapReduce scheduler notifies the reducers that they can start fetching the output files from that mapper. The reducers connect to each of the mappers and download the files of sorted key-value pairs for their partition. The process of partitioning by reducer, sorting, and copying data partitions from mappers to reducers is known as the shuffle [26] (a confusing term—unlike shuffling a deck of cards, there is no ran‐ domness in MapReduce).

The reduce task takes the files from the mappers and merges them together, preserv‐ ing the sort order. Thus, if different mappers produced records with the same key, they will be adjacent in the merged reducer input.

The reducer is called with a key and an iterator that incrementally scans over all records with the same key (which may in some cases not all fit in memory). The reducer can use arbitrary logic to process these records, and can generate any number of output records. These output records are written to a file on the distributed filesys‐ tem (usually, one copy on the local disk of the machine running the reducer, with replicas on other machines).

## MapReduce workflows

The range of problems you can solve with a single MapReduce job is limited. Refer‐ ring back to the log analysis example, a single MapReduce job could determine the number of page views per URL, but not the most popular URLs, since that requires a second round of sorting.

Thus, it is very common for MapReduce jobs to be chained together into workflows, such that the output of one job becomes the input to the next job. The Hadoop Map‐ Reduce framework does not have any particular support for workflows, so this chain‐ ing is done implicitly by directory name: the first job must be configured to write its output to a designated directory in HDFS, and the second job must be configured to read that same directory name as its input. From the MapReduce framework’s point of view, they are two independent jobs.

Chained MapReduce jobs are therefore less like pipelines of Unix commands (which pass the output of one process as input to another process directly, using only a small in-memory buffer) and more like a sequence of commands where each command’s output is written to a temporary file, and the next command reads from the tempo‐ rary file. This design has advantages and disadvantages, which we will discuss in “Materialization of Intermediate State” on page 419.

A batch job’s output is only considered valid when the job has completed successfully (MapReduce discards the partial output of a failed job). Therefore, one job in a work‐ flow can only start when the prior jobs—that is, the jobs that produce its input direc‐ tories—have completed successfully. To handle these dependencies between job

<!-- page 425 -->

v. The joins we talk about in this book are generally equi-joins, the most common type of join, in which a record is associated with other records that have an identical value in a particular field (such as an ID). Some databases support more general types of joins, for example using a less-than operator instead of an equality operator, but we do not have space to cover them here.

executions, various workflow schedulers for Hadoop have been developed, including Oozie, Azkaban, Luigi, Airflow, and Pinball [28].

These schedulers also have management features that are useful when maintaining a large collection of batch jobs. Workflows consisting of 50 to 100 MapReduce jobs are common when building recommendation systems [29], and in a large organization, many different teams may be running different jobs that read each other’s output. Tool support is important for managing such complex dataflows.

Various higher-level tools for Hadoop, such as Pig [30], Hive [31], Cascading [32], Crunch [33], and FlumeJava [34], also set up workflows of multiple MapReduce stages that are automatically wired together appropriately.

## Reduce-Side Joins and Grouping

We discussed joins in Chapter 2 in the context of data models and query languages, but we have not delved into how joins are actually implemented. It is time that we pick up that thread again.

