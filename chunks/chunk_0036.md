<table>
<tr><th>Property</th><th>Transaction processing systems (OLTP)</th><th>Analytic systems (OLAP)</th></tr>
<tr><td>Main read pattern</td><td>Small number of records per query, fetched by key</td><td>Aggregate over large number of records</td></tr>
<tr><td>Main write pattern</td><td>Random-access, low-latency writes from user input</td><td>Bulk import (ETL) or event stream</td></tr>
<tr><td>Primarily used by</td><td>End user/customer, via web application</td><td>Internal analyst, for decision support</td></tr>
<tr><td>What data represents</td><td>Latest state of data (current point in time)</td><td>History of events that happened over time</td></tr>
<tr><td>Dataset size</td><td>Gigabytes to terabytes</td><td>Terabytes to petabytes</td></tr>
</table>

At first, the same databases were used for both transaction processing and analytic queries. SQL turned out to be quite flexible in this regard: it works well for OLTPtype queries as well as OLAP-type queries. Nevertheless, in the late 1980s and early 1990s, there was a trend for companies to stop using their OLTP systems for analytics purposes, and to run the analytics on a separate database instead. This separate data‐ base was called a data warehouse.

## Data Warehousing

An enterprise may have dozens of different transaction processing systems: systems powering the customer-facing website, controlling point of sale (checkout) systems in physical stores, tracking inventory in warehouses, planning routes for vehicles, man‐ aging suppliers, administering employees, etc. Each of these systems is complex and needs a team of people to maintain it, so the systems end up operating mostly auton‐ omously from each other.

These OLTP systems are usually expected to be highly available and to process trans‐ actions with low latency, since they are often critical to the operation of the business. Database administrators therefore closely guard their OLTP databases. They are usu‐ ally reluctant to let business analysts run ad hoc analytic queries on an OLTP data‐ base, since those queries are often expensive, scanning large parts of the dataset, which can harm the performance of concurrently executing transactions.

<!-- page 114 -->

A data warehouse, by contrast, is a separate database that analysts can query to their hearts’ content, without affecting OLTP operations [48]. The data warehouse con‐ tains a read-only copy of the data in all the various OLTP systems in the company. Data is extracted from OLTP databases (using either a periodic data dump or a con‐ tinuous stream of updates), transformed into an analysis-friendly schema, cleaned up, and then loaded into the data warehouse. This process of getting data into the warehouse is known as Extract–Transform–Load (ETL) and is illustrated in Figure 3-8.

<table>
<tr><th></th><th></th><th>Warehouse</th><th>Truck</th></tr>
<tr><td></td><td></td><td>er k</td><td>driver</td></tr>
<tr><td>omme</td><td>er</td><td>Stock-keeping app</td><td>lanner</td></tr>
<tr><td>Sales</td><td></td><td>Inventory</td><td>Geo</td></tr>
<tr><td>DB</td><td></td><td>DB</td><td>DB</td></tr>
<tr><td>extrac</td><td></td><td>ract</td><td>extract</td></tr>
<tr><td></td><td></td><td>transform transform rm</td><td></td></tr>
<tr><td></td><td></td><td>ad oa</td><td></td></tr>
<tr><td></td><td></td><td>eh war ata v</td><td></td></tr>
</table>

Figure 3-8. Simplified outline of ETL into a data warehouse.

Data warehouses now exist in almost all large enterprises, but in small companies they are almost unheard of. This is probably because most small companies don’t have so many different OLTP systems, and most small companies have a small amount of data—small enough that it can be queried in a conventional SQL database, or even analyzed in a spreadsheet. In a large company, a lot of heavy lifting is required to do something that is simple in a small company.

A big advantage of using a separate data warehouse, rather than querying OLTP sys‐ tems directly for analytics, is that the data warehouse can be optimized for analytic access patterns. It turns out that the indexing algorithms discussed in the first half of this chapter work well for OLTP, but are not very good at answering analytic queries.

<!-- page 115 -->

In the rest of this chapter we will look at storage engines that are optimized for ana‐ lytics instead.

## The divergence between OLTP databases and data warehouses

The data model of a data warehouse is most commonly relational, because SQL is generally a good fit for analytic queries. There are many graphical data analysis tools that generate SQL queries, visualize the results, and allow analysts to explore the data (through operations such as drill-down and slicing and dicing).

On the surface, a data warehouse and a relational OLTP database look similar, because they both have a SQL query interface. However, the internals of the systems can look quite different, because they are optimized for very different query patterns. Many database vendors now focus on supporting either transaction processing or analytics workloads, but not both.

Some databases, such as Microsoft SQL Server and SAP HANA, have support for transaction processing and data warehousing in the same product. However, they are increasingly becoming two separate storage and query engines, which happen to be accessible through a common SQL interface [49, 50, 51].

Data warehouse vendors such as Teradata, Vertica, SAP HANA, and ParAccel typi‐ cally sell their systems under expensive commercial licenses. Amazon RedShift is a hosted version of ParAccel. More recently, a plethora of open source SQL-on- Hadoop projects have emerged; they are young but aiming to compete with commer‐ cial data warehouse systems. These include Apache Hive, Spark SQL, Cloudera Impala, Facebook Presto, Apache Tajo, and Apache Drill [52, 53]. Some of them are based on ideas from Google’s Dremel [54].

## Stars and Snowflakes: Schemas for Analytics

As explored in Chapter 2, a wide range of different data models are used in the realm of transaction processing, depending on the needs of the application. On the other hand, in analytics, there is much less diversity of data models. Many data warehouses are used in a fairly formulaic style, known as a star schema (also known as dimen‐ sional modeling [55]).

The example schema in Figure 3-9 shows a data warehouse that might be found at a grocery retailer. At the center of the schema is a so-called fact table (in this example, it is called fact_sales). Each row of the fact table represents an event that occurred at a particular time (here, each row represents a customer’s purchase of a product). If we were analyzing website traffic rather than retail sales, each row might represent a page view or a click by a user.

<!-- page 116 -->

<table>
<tr><th colspan="2">dim_product table</th><th></th><th></th><th></th><th colspan="2">dim_store table</th><th></th></tr>
<tr><td>product_sk</td><td>sku</td><td>description</td><td>brand</td><td>category</td><td>store_sk</td><td>state</td><td>city</td></tr>
<tr><td>30</td><td>ОK4012</td><td>Bananas</td><td>Freshmax</td><td>Fresh fruit</td><td>1</td><td>WA</td><td>Seattle</td></tr>
<tr><td>31</td><td>KA9511</td><td>Fish food</td><td>Aquatech</td><td>Pet supplies</td><td>2</td><td>CA</td><td>San Francisco</td></tr>
<tr><td>32</td><td>AB1234</td><td>Croissant</td><td>Dealicious</td><td>Bakery</td><td>3</td><td>CA</td><td>Palo Alto</td></tr>
</table>

## fact_sales table

<table>
<tr><th>date_key</th><th>product_sk</th><th colspan="2">store_sk / promotion_sk</th><th>customer_sk _</th><th>quantity</th><th>net_price</th><th>discount_price</th></tr>
<tr><td>140102</td><td>31</td><td>3d</td><td>NULL</td><td>NULL</td><td>1</td><td>2.49</td><td>2.49</td></tr>
<tr><td>140102</td><td>69</td><td>5</td><td>19 •.</td><td>NULL</td><td>3</td><td>14.99</td><td>9.99</td></tr>
<tr><td>140102</td><td>74</td><td>3</td><td>23</td><td>191 •.</td><td>1</td><td>4.49</td><td>3.89</td></tr>
<tr><td>• 140102</td><td>33</td><td>8</td><td>NULL</td><td>\ 235</td><td>4</td><td>0.99</td><td>0.99</td></tr>
</table>

## dim_date table

## dim_customer table

<table>
<tr><th>date_key</th><th>year.</th><th>month</th><th>day</th><th>weekday</th><th>is_holiday</th><th>customer_sk</th><th>name</th><th>date_of_birth</th></tr>
<tr><td>140101</td><td>2014</td><td>jan</td><td>1</td><td>wed</td><td>yes</td><td>190</td><td>Alice</td><td>1979-03-29</td></tr>
<tr><td>140102</td><td>2014</td><td>jan</td><td>2</td><td>thu</td><td>no</td><td>&gt; 191</td><td>Bob</td><td>1961-09-02</td></tr>
<tr><td>140103</td><td>2014</td><td>jan</td><td>3</td><td>fri</td><td>no</td><td>192</td><td>Cecil</td><td>1991-12-13</td></tr>
</table>

## dim_promotion table

<table>
<tr><th>promotion_sk</th><th>name</th><th>ad_type</th><th>coupon_type</th></tr>
<tr><td>18</td><td>New Year sale</td><td>Poster</td><td>NULL</td></tr>
<tr><td>» 19</td><td>Aquarium deal</td><td>Direct mail</td><td>Leaflet</td></tr>
<tr><td>20</td><td colspan="2">Coffee &amp; cake bundle In-store sign</td><td>NULL</td></tr>
</table>

Figure 3-9. Example of a star schema for use in a data warehouse.

