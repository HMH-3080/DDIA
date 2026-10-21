<!-- page 1 -->

O'REI

ILLY

L Desiging n t t Daa-Inensiv / e Applications

THE BIG IDEAS BEHIND RELIABLE, SCALABLE, AND MAINTAINABLE SYSTEMS

Martin Kleppmann

<!-- page 2 -->

## Designing Data-Intensive Applications

Data is at the center of many challenges in system design today. Difficult issues need to be figured out, such as scalability, consistency, reliability, efficiency, and maintainability. In addition, we have an overwhelming variety of tools, including relational databases, NoSQL datastores, stream or batch processors, and message brokers. What are the right choices for your application? How do you make sense of all these buzzwords?

In this practical and comprehensive guide, author Martin Kleppmann helps you navigate this diverse landscape by examining the pros and cons of various technologies for processing and storing data. Software keeps changing, but the fundamental principles remain the same. With this book, software engineers and architects will learn how to apply those ideas in practice, and how to make full use of data in modern applications.

• Peer under the hood of the systems you already use, and learn how to use and operate them more effectively
• Make informed decisions by identifying the strengths and weaknesses of different tools
• Navigate the trade-offs around consistency, scalability, fault tolerance, and complexity
• Understand the distributed systems research upon which modern databases are built
• Peek behind the scenes of major online services, and learn from their architectures

Martin Kleppmann is a researcher in distributed systems at the University of Cambridge, UK. Previously he was a software engineer and entrepreneur at internet companies including LinkedIn and Rapportive, where he worked on large-scale data infrastructure. Martin is a regular conference speaker, blogger, and open source contributor.

“This book is awesome. It bridges the huge gap between distributed systems theory and practical engineering.

I wish it had existed a decade ago, so I could have read it then and saved myself all the mistakes along the way.” —Jay Kreps Creator of Apache Kafka and CEO of Confluent

“This book should be required reading for software engineers.

Designing Data-Intensive Applications is a rare resource that connects theory and practice to help developers make smart decisions as they design and implement data infrastructure and systems.’

—Kevin Scott Chief Technology Officer at Microsoft

DATA | HADOOP

Twitter: @oreillymedia facebook.com/oreilly

US $44.99 CAN $59.99

ISBN: 978-1-449-37332-0

<!-- page 3 -->

## Designing Data-Intensive Applications

The Big Ideas Behind Reliable, Scalable, and Maintainable Systems

Martin Kleppmann

Beijing Boston Farnham Sebastopol Tokyo

<!-- page 4 -->

978-1-449-37332-0

[LSI]

Designing Data-Intensive Applications

by Martin Kleppmann

Copyright © 2017 Martin Kleppmann. All rights reserved.

Printed in the United States of America.

Published by O’Reilly Media, Inc., 1005 Gravenstein Highway North, Sebastopol, CA 95472.

O’Reilly books may be purchased for educational, business, or sales promotional use. Online editions are also available for most titles (http://oreilly.com/safari). For more information, contact our corporate/insti‐ tutional sales department: 800-998-9938 or corporate@oreilly.com.

Editors: Ann Spencer and Marie Beaugureau Indexer: Ellen Troutman-Zaig Production Editor: Kristen Brown Interior Designer: David Futato

Copyeditor: Rachel Head

Cover Designer: Karen Montgomery

Proofreader: Amanda Kersey

Illustrator: Rebecca Demarest

March 2017:

First Edition

Revision History for the First Edition

2017-03-01: First Release

See http://oreilly.com/catalog/errata.csp?isbn=9781449373320 for release details.

The O’Reilly logo is a registered trademark of O’Reilly Media, Inc. Designing Data-Intensive Applications, the cover image, and related trade dress are trademarks of O’Reilly Media, Inc.

While the publisher and the author have used good faith efforts to ensure that the information and instructions contained in this work are accurate, the publisher and the author disclaim all responsibility for errors or omissions, including without limitation responsibility for damages resulting from the use of or reliance on this work. Use of the information and instructions contained in this work is at your own risk. If any code samples or other technology this work contains or describes is subject to open source licenses or the intellectual property rights of others, it is your responsibility to ensure that your use thereof complies with such licenses and/or rights.

<!-- page 5 -->

Technology is a powerful force in our society. Data, software, and communication can be used for bad: to entrench unfair power structures, to undermine human rights, and to protect vested interests. But they can also be used for good: to make underrepresented people’s voices heard, to create opportunities for everyone, and to avert disasters. This book is dedicated to everyone working toward the good.

<!-- page 6 -->

<!-- page 7 -->

Computing is pop culture. […] Pop culture holds a disdain for history. Pop culture is all about identity and feeling like you’re participating. It has nothing to do with cooperation, the past or the future—it’s living in the present. I think the same is true of most people who write code for money. They have no idea where [their culture came from].

—Alan Kay, in interview with Dr Dobb’s Journal (2012)

<!-- page 8 -->

<!-- page 9 -->

## Table of Contents

Preface. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xiii

## Part I. Foundations of Data Systems

1. Reliable, Scalable, and Maintainable Applications. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3 Thinking About Data Systems 4 Reliability 6 Hardware Faults 7 Software Errors 8 Human Errors 9 How Important Is Reliability? 10 Scalability 10 Describing Load 11 Describing Performance 13 Approaches for Coping with Load 17 Maintainability 18 Operability: Making Life Easy for Operations 19 Simplicity: Managing Complexity 20 Evolvability: Making Change Easy 21 Summary 22 2. Data Models and Query Languages. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27 Relational Model Versus Document Model 28 29 The Birth of NoSQL The Object-Relational Mismatch 29 Many-to-One and Many-to-Many Relationships 33 Are Document Databases Repeating History? 36

<!-- page 10 -->

