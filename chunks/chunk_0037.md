Usually, facts are captured as individual events, because this allows maximum flexi‐ bility of analysis later. However, this means that the fact table can become extremely large. A big enterprise like Apple, Walmart, or eBay may have tens of petabytes of transaction history in its data warehouse, most of which is in fact tables [56].

Some of the columns in the fact table are attributes, such as the price at which the product was sold and the cost of buying it from the supplier (allowing the profit mar‐ gin to be calculated). Other columns in the fact table are foreign key references to other tables, called dimension tables. As each row in the fact table represents an event, the dimensions represent the who, what, where, when, how, and why of the event.

For example, in Figure 3-9, one of the dimensions is the product that was sold. Each row in the dim_product table represents one type of product that is for sale, including

<!-- page 117 -->

its stock-keeping unit (SKU), description, brand name, category, fat content, package size, etc. Each row in the fact_sales table uses a foreign key to indicate which prod‐ uct was sold in that particular transaction. (For simplicity, if the customer buys sev‐ eral different products at once, they are represented as separate rows in the fact table.)

Even date and time are often represented using dimension tables, because this allows additional information about dates (such as public holidays) to be encoded, allowing queries to differentiate between sales on holidays and non-holidays.

The name “star schema” comes from the fact that when the table relationships are visualized, the fact table is in the middle, surrounded by its dimension tables; the connections to these tables are like the rays of a star.

A variation of this template is known as the snowflake schema, where dimensions are further broken down into subdimensions. For example, there could be separate tables for brands and product categories, and each row in the dim_product table could ref‐ erence the brand and category as foreign keys, rather than storing them as strings in the dim_product table. Snowflake schemas are more normalized than star schemas, but star schemas are often preferred because they are simpler for analysts to work with [55].

In a typical data warehouse, tables are often very wide: fact tables often have over 100 columns, sometimes several hundred [51]. Dimension tables can also be very wide, as they include all the metadata that may be relevant for analysis—for example, the dim_store table may include details of which services are offered at each store, whether it has an in-store bakery, the square footage, the date when the store was first opened, when it was last remodeled, how far it is from the nearest highway, etc.

## Column-Oriented Storage

If you have trillions of rows and petabytes of data in your fact tables, storing and querying them efficiently becomes a challenging problem. Dimension tables are usu‐ ally much smaller (millions of rows), so in this section we will concentrate primarily on storage of facts.

Although fact tables are often over 100 columns wide, a typical data warehouse query only accesses 4 or 5 of them at one time ("SELECT *" queries are rarely needed for analytics) [51]. Take the query in Example 3-1: it accesses a large number of rows (every occurrence of someone buying fruit or candy during the 2013 calendar year), but it only needs to access three columns of the fact_sales table: date_key, product_sk, and quantity. The query ignores all other columns.

<!-- page 118 -->

Example 3-1. Analyzing whether people are more inclined to buy fresh fruit or candy, depending on the day of the week

SELECT dim_date.weekday, dim_product.category, SUM(fact_sales.quantity) AS quantity_sold FROM fact_sales JOIN dim_date ON fact_sales.date_key = dim_date.date_key JOIN dim_product ON fact_sales.product_sk = dim_product.product_sk WHERE dim_date.year = 2013 AND dim_product.category IN ('Fresh fruit', 'Candy') GROUP BY dim_date.weekday, dim_product.category;

How can we execute this query efficiently?

In most OLTP databases, storage is laid out in a row-oriented fashion: all the values from one row of a table are stored next to each other. Document databases are simi‐ lar: an entire document is typically stored as one contiguous sequence of bytes. You can see this in the CSV example of Figure 3-1.

In order to process a query like Example 3-1, you may have indexes on fact_sales.date_key and/or fact_sales.product_sk that tell the storage engine where to find all the sales for a particular date or for a particular product. But then, a row-oriented storage engine still needs to load all of those rows (each consisting of over 100 attributes) from disk into memory, parse them, and filter out those that don’t meet the required conditions. That can take a long time.

The idea behind column-oriented storage is simple: don’t store all the values from one row together, but store all the values from each column together instead. If each col‐ umn is stored in a separate file, a query only needs to read and parse those columns that are used in that query, which can save a lot of work. This principle is illustrated in Figure 3-10.

Column storage is easiest to understand in a relational data model, but it applies equally to nonrelational data. For example, Parquet [57] is a columnar storage format that supports a document data model, based on Google’s Dremel [54].

<!-- page 119 -->

## fact_sales table

<table>
<tr><th>date_key</th><th>product_sk</th><th>store_sk</th><th colspan="2">promotion_sk customer_sk</th><th>quantity</th><th>net_price</th><th>discount_price</th></tr>
<tr><td>140102</td><td>69</td><td>4</td><td>NULL</td><td>NULL</td><td>1</td><td>13.99</td><td>13.99</td></tr>
<tr><td>140102</td><td>69</td><td>5</td><td>19</td><td>NULL</td><td>3</td><td>14.99</td><td>9.99</td></tr>
<tr><td>140102</td><td>69</td><td>5</td><td>NULL</td><td>191</td><td>1</td><td>14.99</td><td>14.99</td></tr>
<tr><td>140102</td><td>74</td><td>3</td><td>23</td><td>202</td><td>5</td><td>0.99</td><td>0.89</td></tr>
<tr><td>140103</td><td>31</td><td>2</td><td>NULL</td><td>NULL</td><td>1</td><td>2.49</td><td>2.49</td></tr>
<tr><td>140103</td><td>31</td><td>3</td><td>NULL</td><td>NULL</td><td>3</td><td>14.99</td><td>9.99</td></tr>
<tr><td>140103</td><td>31</td><td>3</td><td>21</td><td>123</td><td>1</td><td>49.99</td><td>39.99</td></tr>
<tr><td>140103</td><td>31</td><td>8</td><td>NULL</td><td>233</td><td>1</td><td>0.99</td><td>0.99</td></tr>
</table>

## Columnar storage layout:

<table>
<tr><th>date_key file contents:</th><th>140102, 140102, 140102, 140102, 140103, 140103, 140103, 140103</th></tr>
<tr><td>product_sk file contents:</td><td>69, 69, 69, 74, 31, 31, 31, 31</td></tr>
<tr><td>store_sk file contents:</td><td>4, 5, 5, 3, 2, 3, 3, 8</td></tr>
<tr><td>promotion_sk file contents:</td><td>NULL, 19, NULL, 23, NULL, NULL, 21, NULL</td></tr>
<tr><td>customer_sk file contents:</td><td>NULL, NULL, 191, 202, NULL, NULL, 123, 233</td></tr>
<tr><td>quantity file contents:</td><td>1, 3, 1, 5, 1, 3, 1, 1</td></tr>
<tr><td>net_price file contents:</td><td>13.99, 14.99, 14.99, 0.99, 2.49, 14.99, 49.99, 0.99</td></tr>
<tr><td>discount_price file contents:</td><td>13.99, 9.99, 14.99, 0.89, 2.49, 9.99, 39.99, 0.99</td></tr>
</table>

Figure 3-10. Storing relational data by column, rather than by row.

The column-oriented storage layout relies on each column file containing the rows in the same order. Thus, if you need to reassemble an entire row, you can take the 23rd entry from each of the individual column files and put them together to form the 23rd row of the table.

## Column Compression

