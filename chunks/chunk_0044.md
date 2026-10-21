JSON is less verbose than XML, but both still use a lot of space compared to binary formats. This observation led to the development of a profusion of binary encodings for JSON (MessagePack, BSON, BJSON, UBJSON, BISON, and Smile, to name a few) and for XML (WBXML and Fast Infoset, for example). These formats have been adopted in various niches, but none of them are as widely adopted as the textual ver‐ sions of JSON and XML.

Some of these formats extend the set of datatypes (e.g., distinguishing integers and floating-point numbers, or adding support for binary strings), but otherwise they keep the JSON/XML data model unchanged. In particular, since they don’t prescribe a schema, they need to include all the object field names within the encoded data. That is, in a binary encoding of the JSON document in Example 4-1, they will need to include the strings userName, favoriteNumber, and interests somewhere.

<!-- page 138 -->

Example 4-1. Example record which we will encode in several binary formats in this chapter

{ "userName": "Martin", "favoriteNumber": 1337, "interests": ["daydreaming", "hacking"] }

Let’s look at an example of MessagePack, a binary encoding for JSON. Figure 4-1 shows the byte sequence that you get if you encode the JSON document in Example 4-1 with MessagePack [14]. The first few bytes are as follows:

1. The first byte, 0x83, indicates that what follows is an object (top four bits = 0x80) with three fields (bottom four bits = 0x03). (In case you’re wondering what hap‐ pens if an object has more than 15 fields, so that the number of fields doesn’t fit in four bits, it then gets a different type indicator, and the number of fields is encoded in two or four bytes.)
2. The second byte, 0xa8, indicates that what follows is a string (top four bits = 0xa0) that is eight bytes long (bottom four bits = 0x08).
3. The next eight bytes are the field name userName in ASCII. Since the length was indicated previously, there’s no need for any marker to tell us where the string ends (or any escaping).
4. The next seven bytes encode the six-letter string value Martin with a prefix 0xa6, and so on.

The binary encoding is 66 bytes long, which is only a little less than the 81 bytes taken by the textual JSON encoding (with whitespace removed). All the binary encodings of JSON are similar in this regard. It’s not clear whether such a small space reduction (and perhaps a speedup in parsing) is worth the loss of human-readability.

In the following sections we will see how we can do much better, and encode the same record in just 32 bytes.

<!-- page 139 -->

## MessagePack

Byte sequence (66 bytes):

83 a8 75 73 65 72 4e 61 6d 65 a6 4d 61 72 74 69 6e ae 66 61 76 6£ 72 69 74 65 4e 75 6d 62 65 72 cd 05 39 a9 69 6e 74 65 72 65 73 74 73 92 ab 64 61 79 64 72 65 61 6d 69 6e 67 a7 68

61 63 6b 69 6e 67

Breakdown:

<table>
<tr><th>object</th><th>string</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th>string</th><th></th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td>(3 entries)</td><td>◦ (length 8)</td><td>u</td><td>s</td><td>e</td><td>N</td><td>a</td><td>m</td><td>e</td><td>(length 6)</td><td>M</td><td>a</td><td>x</td><td>七</td><td>-i</td><td>n</td></tr>
<tr><td>83</td><td>a8</td><td colspan="5">75 73 65 72 4e 61</td><td colspan="2">6d 65</td><td>a6</td><td colspan="6">4d 61 72 74 69 6e</td></tr>
<tr><td></td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>(length 14)</td><td>f</td><td>a</td><td>v o</td><td></td><td></td><td>t</td><td>e</td><td>N m u</td><td>b</td><td>e</td><td>x</td><td></td><td></td><td></td></tr>
<tr><td></td><td>ae</td><td colspan="11">66 61 76 6f 72 69 74 65 4e 75 6d 62 65 72</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>uint16</td><td colspan="2">1337</td><td>(length 9)</td><td></td><td>i</td><td>n</td><td>t</td><td>e x e</td><td>s</td><td>t</td><td>s</td><td></td><td></td><td></td></tr>
<tr><td></td><td>cd</td><td colspan="2">05 39</td><td>a9</td><td></td><td colspan="7">69 66 74 65 72 65 73 74 73</td><td></td><td></td><td></td></tr>
<tr><td>array</td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td colspan="2">(2 entries) (length 11)</td><td>d</td><td>a</td><td>d y</td><td>x</td><td>e</td><td>a</td><td>m</td><td>n</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>92.</td><td>ab</td><td colspan="8">64 61 79 64 72 65 61 6d 69 6e 67</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>string</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>(length 7)</td><td>h</td><td>a</td><td>c k</td><td>1</td><td>n</td><td>g</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>a7</td><td colspan="6">68 61 63 6b 69 6e 67</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
</table>

Figure 4-1. Example record (Example 4-1) encoded using MessagePack.

## Thrift and Protocol Buffers

Apache Thrift [15] and Protocol Buffers (protobuf) [16] are binary encoding libraries that are based on the same principle. Protocol Buffers was originally developed at Google, Thrift was originally developed at Facebook, and both were made open source in 2007–08 [17].

Both Thrift and Protocol Buffers require a schema for any data that is encoded. To encode the data in Example 4-1 in Thrift, you would describe the schema in the Thrift interface definition language (IDL) like this:

struct Person { 1: required string 2: optional i64 userName, favoriteNumber, 3: optional list<string> interests }

<!-- page 140 -->

The equivalent schema definition for Protocol Buffers looks very similar:

message Person { required string user_name = 1; optional int64 favorite_number = 2; } repeated string interests = 3;

Thrift and Protocol Buffers each come with a code generation tool that takes a schema definition like the ones shown here, and produces classes that implement the schema in various programming languages [18]. Your application code can call this generated code to encode or decode records of the schema.

What does data encoded with this schema look like? Confusingly, Thrift has two dif‐ ferent binary encoding formats,iii called BinaryProtocol and CompactProtocol, respec‐ tively. Let’s look at BinaryProtocol first. Encoding Example 4-1 in that format takes 59 bytes, as shown in Figure 4-2 [19].

Thrift BinaryProtocol

Byte sequence (59 bytes):

0b 00 01 00 00 00 06 4d 61 72 74 69 6e 0a 00 02 00 00 00 00 00 00 05 39 0 00 03 0b 00 00 00 02 00 00 00 0b 64 61 79 64 72 65 61 6d 69 6e 67 00 00 00 07 68 61 63 6b 69 6e 67 00

Breakdown:

<table>
<tr><th>field tag = 1 type 11 (string)  f length 6</th><th>M.</th><th>a</th><th></th><th>t</th><th>i</th><th>n</th><th></th><th></th><th></th></tr>
<tr><td>00 01 00 00 00 06 0b</td><td colspan="6">4d 61 72 74 69 6e</td><td></td><td></td><td></td></tr>
<tr><td>1337 field tag = 2 type 10 (i64)</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td colspan="4">00 02 00 00 00 00 00 00 05 39 Oa</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>field tag = 3 item type 11 (string) type 15 (list)</td><td></td><td colspan="2">2 list items</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>00 03 0f 0b</td><td colspan="4">00 00 00 02</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>length 11</td><td>d.</td><td>a</td><td>y</td><td>d</td><td>x</td><td>e</td><td>a</td><td>n</td><td>g</td></tr>
<tr><td>00 00 00 0&gt;</td><td colspan="9">64 61 79 64 72 65 61 6d 69 6e 67</td></tr>
<tr><td>length 7</td><td>h</td><td>a</td><td>c</td><td>k</td><td>1.</td><td>n</td><td>g</td><td colspan="2">end of struct</td></tr>
<tr><td>00 00 00 07</td><td colspan="7">68 61 63 6b 69 6e 67</td><td>00</td><td></td></tr>
</table>

Figure 4-2. Example record encoded using Thrift’s BinaryProtocol.

iii. Actually, it has three—BinaryProtocol, CompactProtocol, and DenseProtocol—although DenseProtocol is only supported by the C++ implementation, so it doesn’t count as cross-language [18]. Besides those, it also has two different JSON-based encoding formats [19]. What fun!

<!-- page 141 -->

