As a result, graph algorithms often have a lot of cross-machine communication over‐ head, and the intermediate state (messages sent between nodes) is often bigger than the original graph. The overhead of sending messages over the network can signifi‐ cantly slow down distributed graph algorithms.

For this reason, if your graph can fit in memory on a single computer, it’s quite likely that a single-machine (maybe even single-threaded) algorithm will outperform a dis‐ tributed batch process [73, 74]. Even if the graph is bigger than memory, it can fit on the disks of a single computer, single-machine processing using a framework such as GraphChi is a viable option [75]. If the graph is too big to fit on a single machine, a distributed approach such as Pregel is unavoidable; efficiently parallelizing graph algorithms is an area of ongoing research [76].

## High-Level APIs and Languages

Over the years since MapReduce first became popular, the execution engines for dis‐ tributed batch processing have matured. By now, the infrastructure has become robust enough to store and process many petabytes of data on clusters of over 10,000 machines. As the problem of physically operating batch processes at such scale has been considered more or less solved, attention has turned to other areas: improving the programming model, improving the efficiency of processing, and broadening the set of problems that these technologies can solve.

<!-- page 449 -->

As discussed previously, higher-level languages and APIs such as Hive, Pig, Cascad‐ ing, and Crunch became popular because programming MapReduce jobs by hand is quite laborious. As Tez emerged, these high-level languages had the additional bene‐ fit of being able to move to the new dataflow execution engine without the need to rewrite job code. Spark and Flink also include their own high-level dataflow APIs, often taking inspiration from FlumeJava [34].

These dataflow APIs generally use relational-style building blocks to express a com‐ putation: joining datasets on the value of some field; grouping tuples by key; filtering by some condition; and aggregating tuples by counting, summing, or other functions. Internally, these operations are implemented using the various join and grouping algorithms that we discussed earlier in this chapter.

Besides the obvious advantage of requiring less code, these high-level interfaces also allow interactive use, in which you write analysis code incrementally in a shell and run it frequently to observe what it is doing. This style of development is very helpful when exploring a dataset and experimenting with approaches for processing it. It is also reminiscent of the Unix philosophy, which we discussed in “The Unix Philoso‐ phy” on page 394.

Moreover, these high-level interfaces not only make the humans using the system more productive, but they also improve the job execution efficiency at a machine level.

## The move toward declarative query languages

An advantage of specifying joins as relational operators, compared to spelling out the code that performs the join, is that the framework can analyze the properties of the join inputs and automatically decide which of the aforementioned join algorithms would be most suitable for the task at hand. Hive, Spark, and Flink have cost-based query optimizers that can do this, and even change the order of joins so that the amount of intermediate state is minimized [66, 77, 78, 79].

The choice of join algorithm can make a big difference to the performance of a batch job, and it is nice not to have to understand and remember all the various join algo‐ rithms we discussed in this chapter. This is possible if joins are specified in a declara‐ tive way: the application simply states which joins are required, and the query optimizer decides how they can best be executed. We previously came across this idea in “Query Languages for Data” on page 42.

However, in other ways, MapReduce and its dataflow successors are very different from the fully declarative query model of SQL. MapReduce was built around the idea of function callbacks: for each record or group of records, a user-defined function (the mapper or reducer) is called, and that function is free to call arbitrary code in order to decide what to output. This approach has the advantage that you can draw

<!-- page 450 -->

upon a large ecosystem of existing libraries to do things like parsing, natural language analysis, image analysis, and running numerical or statistical algorithms.

The freedom to easily run arbitrary code is what has long distinguished batch pro‐ cessing systems of MapReduce heritage from MPP databases (see “Comparing Hadoop to Distributed Databases” on page 414); although databases have facilities for writing user-defined functions, they are often cumbersome to use and not well integrated with the package managers and dependency management systems that are widely used in most programming languages (such as Maven for Java, npm for Java‐ Script, and Rubygems for Ruby).

However, dataflow engines have found that there are also advantages to incorporat‐ ing more declarative features in areas besides joins. For example, if a callback func‐ tion contains only a simple filtering condition, or it just selects some fields from a record, then there is significant CPU overhead in calling the function on every record. If such simple filtering and mapping operations are expressed in a declarative way, the query optimizer can take advantage of column-oriented storage layouts (see “Column-Oriented Storage” on page 95) and read only the required columns from disk. Hive, Spark DataFrames, and Impala also use vectorized execution (see “Mem‐ ory bandwidth and vectorized processing” on page 99): iterating over data in a tight inner loop that is friendly to CPU caches, and avoiding function calls. Spark gener‐ ates JVM bytecode [79] and Impala uses LLVM to generate native code for these inner loops [41].

By incorporating declarative aspects in their high-level APIs, and having query opti‐ mizers that can take advantage of them during execution, batch processing frame‐ works begin to look more like MPP databases (and can achieve comparable performance). At the same time, by having the extensibility of being able to run arbi‐ trary code and read data in arbitrary formats, they retain their flexibility advantage.

## Specialization for different domains

While the extensibility of being able to run arbitrary code is useful, there are also many common cases where standard processing patterns keep reoccurring, and so it is worth having reusable implementations of the common building blocks. Tradition‐ ally, MPP databases have served the needs of business intelligence analysts and busi‐ ness reporting, but that is just one among many domains in which batch processing is used.

