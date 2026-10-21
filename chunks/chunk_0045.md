Similarly to Figure 4-1, each field has a type annotation (to indicate whether it is a string, integer, list, etc.) and, where required, a length indication (length of a string, number of items in a list). The strings that appear in the data (“Martin”, “daydream‐ ing”, “hacking”) are also encoded as ASCII (or rather, UTF-8), similar to before.

The big difference compared to Figure 4-1 is that there are no field names (userName, favoriteNumber, interests). Instead, the encoded data contains field tags, which are numbers (1, 2, and 3). Those are the numbers that appear in the schema definition. Field tags are like aliases for fields—they are a compact way of saying what field we’re talking about, without having to spell out the field name.

The Thrift CompactProtocol encoding is semantically equivalent to BinaryProtocol, but as you can see in Figure 4-3, it packs the same information into only 34 bytes. It does this by packing the field type and tag number into a single byte, and by using variable-length integers. Rather than using a full eight bytes for the number 1337, it is encoded in two bytes, with the top bit of each byte used to indicate whether there are still more bytes to come. This means numbers between –64 and 63 are encoded in one byte, numbers between –8192 and 8191 are encoded in two bytes, etc. Bigger numbers use more bytes.

## Thrift CompactProtocol

Byte sequence (34 bytes):

<table>
<tr><th>18 06 4d 61 72 74 69 6e 16 £2 14 19 28 0b 64 61 79 64 72 65</th></tr>
<tr><td>61 6d 69 6e 67 07 68 61 63 6b 69 6e 67 00</td></tr>
</table>

<table>
<tr><th>Breakdown:</th><th></th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td>м gth 6  field tag = 1 type 8 (string)</td><td>а</td><td></td><td>t</td><td>i n</td><td></td><td>1337</td></tr>
<tr><td colspan="5">18 [06 [4d 61 72 74 69 60] |0 0 0 1 1 0 0 0</td><td></td><td>0 0 1 0 1 0 0 1 1 1 00 1</td></tr>
<tr><td>field tag += 1 type 6 (i64)</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>26 (2 24 | 0 0 0 1 0 1 1 0</td><td></td><td></td><td></td><td></td><td></td><td>0 0 0 1 0 1 0 0</td></tr>
<tr><td>field tag += 1 type 9 (list)</td><td colspan="5">2 list items item type 8 (string)</td><td></td></tr>
<tr><td>19] |20| | 0 0 0 1 1 0 0 1</td><td colspan="3">( s</td><td>]</td><td></td><td></td></tr>
<tr><td colspan="2">lenghii d a</td><td colspan="2">y d r.</td><td>e</td><td>a m</td><td>n g</td></tr>
<tr><td colspan="7">0b 64 61 79 64 72 65 61 6d 69 6e 67</td></tr>
<tr><td>length7 h</td><td>a</td><td>c</td><td>k</td><td>n.</td><td>g</td><td>end of struct</td></tr>
<tr><td colspan="6">07 68 61 63 6b 69 6e 67</td><td>00</td></tr>
</table>

Figure 4-3. Example record encoded using Thrift’s CompactProtocol.

Finally, Protocol Buffers (which has only one binary encoding format) encodes the same data as shown in Figure 4-4. It does the bit packing slightly differently, but is

<!-- page 142 -->

otherwise very similar to Thrift’s CompactProtocol. Protocol Buffers fits the same record in 33 bytes.

Protocol Buffers

Byte sequence (33 bytes):

0a 06 4d 61 72 74 69 6e 10 b9 0a 1a 0b 64 61 79 64 72 65 61 6d 69 6e 67 1a 07 68 61 63 6b 69 6e 67

Breakdown:

<table>
<tr><th>field tag = 1 type 2 (string) 0 0 0 0 1 0 1 0</th><th>length 6 0a 06</th><th colspan="5">M a 4d 61 72 74 69 6e</th><th></th><th colspan="3">0 0 0 1 0 1 0 0 1 1 1 0 0 1</th></tr>
<tr><td>field tag = 2 type 0 (varint)</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>0 00 1 0 0 0 0</td><td colspan="2">10 [b9 0a</td><td></td><td></td><td colspan="3">1 0 1 1 1 0 0 1</td><td></td><td colspan="2">0 0 0 0 1 0 1</td></tr>
<tr><td>field tag = 3 type 2 (string)</td><td>length 11</td><td>d a</td><td>y</td><td>d</td><td>x</td><td>e</td><td>a</td><td>m</td><td>n</td><td>g</td></tr>
<tr><td>0 0 0 1 1 | 0 1 0</td><td>1a 0b</td><td colspan="9">64 61 79 64 72 65 61 6d 69 6e 67</td></tr>
<tr><td>field tag = 3 type 2 (string) | 0 0 0 1 1 0 1 0</td><td>length 7| 1a 07</td><td colspan="6">a h 68 61 63 6b 69 6e 67</td><td></td><td></td><td></td></tr>
</table>

Figure 4-4. Example record encoded using Protocol Buffers.

One detail to note: in the schemas shown earlier, each field was marked either required or optional, but this makes no difference to how the field is encoded (nothing in the binary data indicates whether a field was required). The difference is simply that required enables a runtime check that fails if the field is not set, which can be useful for catching bugs.

## Field tags and schema evolution

We said previously that schemas inevitably need to change over time. We call this schema evolution. How do Thrift and Protocol Buffers handle schema changes while keeping backward and forward compatibility?

As you can see from the examples, an encoded record is just the concatenation of its encoded fields. Each field is identified by its tag number (the numbers 1, 2, 3 in the sample schemas) and annotated with a datatype (e.g., string or integer). If a field value is not set, it is simply omitted from the encoded record. From this you can see that field tags are critical to the meaning of the encoded data. You can change the name of a field in the schema, since the encoded data never refers to field names, but you cannot change a field’s tag, since that would make all existing encoded data invalid.

<!-- page 143 -->

You can add new fields to the schema, provided that you give each field a new tag number. If old code (which doesn’t know about the new tag numbers you added) tries to read data written by new code, including a new field with a tag number it doesn’t recognize, it can simply ignore that field. The datatype annotation allows the parser to determine how many bytes it needs to skip. This maintains forward com‐ patibility: old code can read records that were written by new code.

What about backward compatibility? As long as each field has a unique tag number, new code can always read old data, because the tag numbers still have the same meaning. The only detail is that if you add a new field, you cannot make it required. If you were to add a field and make it required, that check would fail if new code read data written by old code, because the old code will not have written the new field that you added. Therefore, to maintain backward compatibility, every field you add after the initial deployment of the schema must be optional or have a default value.

