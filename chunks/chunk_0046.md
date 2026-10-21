Removing a field is just like adding a field, with backward and forward compatibility concerns reversed. That means you can only remove a field that is optional (a required field can never be removed), and you can never use the same tag number again (because you may still have data written somewhere that includes the old tag number, and that field must be ignored by new code).

## Datatypes and schema evolution

What about changing the datatype of a field? That may be possible—check the docu‐ mentation for details—but there is a risk that values will lose precision or get trunca‐ ted. For example, say you change a 32-bit integer into a 64-bit integer. New code can easily read data written by old code, because the parser can fill in any missing bits with zeros. However, if old code reads data written by new code, the old code is still using a 32-bit variable to hold the value. If the decoded 64-bit value won’t fit in 32 bits, it will be truncated.

A curious detail of Protocol Buffers is that it does not have a list or array datatype, but instead has a repeated marker for fields (which is a third option alongside required and optional). As you can see in Figure 4-4, the encoding of a repeated field is just what it says on the tin: the same field tag simply appears multiple times in the record. This has the nice effect that it’s okay to change an optional (singlevalued) field into a repeated (multi-valued) field. New code reading old data sees a list with zero or one elements (depending on whether the field was present); old code reading new data sees only the last element of the list.

Thrift has a dedicated list datatype, which is parameterized with the datatype of the list elements. This does not allow the same evolution from single-valued to multivalued as Protocol Buffers does, but it has the advantage of supporting nested lists.

<!-- page 144 -->

## Avro

Apache Avro [20] is another binary encoding format that is interestingly different from Protocol Buffers and Thrift. It was started in 2009 as a subproject of Hadoop, as a result of Thrift not being a good fit for Hadoop’s use cases [21].

Avro also uses a schema to specify the structure of the data being encoded. It has two schema languages: one (Avro IDL) intended for human editing, and one (based on JSON) that is more easily machine-readable.

Our example schema, written in Avro IDL, might look like this:

record Person { string userName; union { null, long } favoriteNumber = null; array<string> interests; }

The equivalent JSON representation of that schema is as follows:

{ "type": "record", "name": "Person", "fields": [ {"name": "userName", "type": "string"}, {"name": "favoriteNumber", "type": ["null", "long"], "default": null}, "type": {"type": "array", "items": "string"}} {"name": "interests", ] }

First of all, notice that there are no tag numbers in the schema. If we encode our example record (Example 4-1) using this schema, the Avro binary encoding is just 32 bytes long—the most compact of all the encodings we have seen. The breakdown of the encoded byte sequence is shown in Figure 4-5.

If you examine the byte sequence, you can see that there is nothing to identify fields or their datatypes. The encoding simply consists of values concatenated together. A string is just a length prefix followed by UTF-8 bytes, but there’s nothing in the enco‐ ded data that tells you that it is a string. It could just as well be an integer, or some‐ thing else entirely. An integer is encoded using a variable-length encoding (the same as Thrift’s CompactProtocol).

<!-- page 145 -->

## Avro

Byte sequence (32 bytes):

0c 4d 61 72 74 69 6e 02 £2 14 04 16 64 61 79 64 72 65 61 6d 69 6e 67 0e 68 61 63 6b 69 6e 67 00

<table>
<tr><th>Breakdown:</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td>length 6 sign 0 0 0 0 1 1 0 0</td><td colspan="6">M 0c 4d 61 72 74 69 6e</td><td></td><td colspan="3">0 0 1 0 1 0 0 1 1 1 0 0 1</td></tr>
<tr><td>union branch 1 (long, not null)</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>0 0 0 0 0 0 1 0</td><td colspan="3">£2 14  02</td><td></td><td></td><td colspan="3">1 1 1 0 0 1 0</td><td colspan="2">0 0 0 1 0 10 0]</td></tr>
<tr><td>2 array items follow</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>0 0 0 0 0 1 0 0</td><td>04</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>11</td><td>d</td><td>a</td><td>Y</td><td>d</td><td>x</td><td>e</td><td>a</td><td>m</td><td>n</td><td>g</td></tr>
<tr><td></td><td colspan="10">64 61 79 64 72 65 61 6d 69 6e 67 6</td></tr>
<tr><td></td><td>h.</td><td>a</td><td>c</td><td>k</td><td></td><td>n.</td><td>g</td><td></td><td colspan="2">end of array</td></tr>
<tr><td>0 0 0</td><td colspan="7">Oe 68 61 63 6b 69 6e 67</td><td></td><td>00</td><td></td></tr>
</table>

Figure 4-5. Example record encoded using Avro.

To parse the binary data, you go through the fields in the order that they appear in the schema and use the schema to tell you the datatype of each field. This means that the binary data can only be decoded correctly if the code reading the data is using the exact same schema as the code that wrote the data. Any mismatch in the schema between the reader and the writer would mean incorrectly decoded data.

So, how does Avro support schema evolution?

The writer’s schema and the reader’s schema

With Avro, when an application wants to encode some data (to write it to a file or database, to send it over the network, etc.), it encodes the data using whatever version of the schema it knows about—for example, that schema may be compiled into the application. This is known as the writer’s schema.

When an application wants to decode some data (read it from a file or database, receive it from the network, etc.), it is expecting the data to be in some schema, which is known as the reader’s schema. That is the schema the application code is relying on —code may have been generated from that schema during the application’s build process.

The key idea with Avro is that the writer’s schema and the reader’s schema don’t have to be the same—they only need to be compatible. When data is decoded (read), the

<!-- page 146 -->

Avro library resolves the differences by looking at the writer’s schema and the reader’s schema side by side and translating the data from the writer’s schema into the reader’s schema. The Avro specification [20] defines exactly how this resolution works, and it is illustrated in Figure 4-6.

