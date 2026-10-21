[76] Mark D. Ryan: “Enhanced Certificate Transparency and End-to-End Encrypted Mail,” at Network and Distributed System Security Symposium (NDSS), February 2014. doi:10.14722/ndss.2014.23379 [77] “Software Engineering Code of Ethics and Professional Practice,” Association for Computing Machinery, acm.org, 1999. [78] François Chollet: “Software development is starting to involve important ethical choices,” twitter.com, October 30, 2016. [79] Igor Perisic: “Making Hard Choices: The Quest for Ethics in Machine Learning,” engineering.linkedin.com, November 2016. [80] John Naughton: “Algorithm Writers Need a Code of Conduct,” theguar‐ dian.com, December 6, 2015. [81] Logan Kugler: “What Happens When Big Data Blunders?,” Communications of the ACM, volume 59, number 6, pages 15–16, June 2016. doi:10.1145/2911975 [82] Bill Davidow: “Welcome to Algorithmic Prison,” theatlantic.com, February 20, 2014. [83] Don Peck: “They’re Watching You at Work,” theatlantic.com, December 2013. [84] Leigh Alexander: “Is an Algorithm Any Less Racist Than a Human?” theguar‐ dian.com, August 3, 2016. [85] Jesse Emspak: “How a Machine Learns Prejudice,” scientificamerican.com, December 29, 2016. [86] Maciej Cegłowski: “The Moral Economy of Tech,” idlewords.com, June 2016. [87] Cathy O’Neil: Weapons of Math Destruction: How Big Data Increases Inequality and Threatens Democracy. Crown Publishing, 2016. ISBN: 978-0-553-41881-1 [88] Julia Angwin: “Make Algorithms Accountable,” nytimes.com, August 1, 2016. [89] Bryce Goodman and Seth Flaxman: “European Union Regulations on Algorith‐ mic Decision-Making and a ‘Right to Explanation’,” arXiv:1606.08813, August 31, 2016. [90] “A Review of the Data Broker Industry: Collection, Use, and Sale of Consumer Data for Marketing Purposes,” Staff Report, United States Senate Committee on Com‐ merce, Science, and Transportation, commerce.senate.gov, December 2013. [91] Olivia Solon: “Facebook’s Failure: Did Fake News and Polarized Politics Get Trump Elected?” theguardian.com, November 10, 2016. [92] Donella H. Meadows and Diana Wright: Thinking in Systems: A Primer. Chelsea Green Publishing, 2008. ISBN: 978-1-603-58055-7

<!-- page 573 -->

[93] Daniel J. Bernstein: “Listening to a ‘big data’/‘data science’ talk,” twitter.com, May 12, 2015. [94] Marc Andreessen: “Why Software Is Eating the World,” The Wall Street Journal, 20 August 2011. [95] J. M. Porup: “‘Internet of Things’ Security Is Hilariously Broken and Getting Worse,” arstechnica.com, January 23, 2016. [96] Bruce Schneier: Data and Goliath: The Hidden Battles to Collect Your Data and Control Your World. W. W. Norton, 2015. ISBN: 978-0-393-35217-7 [97] The Grugq: “Nothing to Hide,” grugq.tumblr.com, April 15, 2016. [98] Tony Beltramelli: “Deep-Spying: Spying Using Smartwatch and Deep Learning,” Masters Thesis, IT University of Copenhagen, December 2015. Available at arxiv.org/abs/1512.05616 [99] Shoshana Zuboff: “Big Other: Surveillance Capitalism and the Prospects of an Information Civilization,” Journal of Information Technology, volume 30, number 1, pages 75–89, April 2015. doi:10.1057/jit.2015.5 [100] Carina C. Zona: “Consequences of an Insightful Algorithm,” at GOTO Berlin, November 2016. [101] Bruce Schneier: “Data Is a Toxic Asset, So Why Not Throw It Out?,” schne‐ ier.com, March 1, 2016. [102] John E. Dunn: “The UK’s 15 Most Infamous Data Breaches,” techworld.com, November 18, 2016. [103] Cory Scott: “Data is not toxic - which implies no benefit - but rather hazardous material, where we must balance need vs. want,” twitter.com, March 6, 2016. [104] Bruce Schneier: “Mission Creep: When Everything Is Terrorism,” schneier.com, July 16, 2013. [105] Lena Ulbricht and Maximilian von Grafenstein: “Big Data: Big Power Shifts?,” Internet Policy Review, volume 5, number 1, March 2016. doi:10.14763/2016.1.406 [106] Ellen P. Goodman and Julia Powles: “Facebook and Google: Most Powerful and Secretive Empires We’ve Ever Known,” theguardian.com, September 28, 2016. [107] Directive 95/46/EC on the protection of individuals with regard to the process‐ ing of personal data and on the free movement of such data, Official Journal of the European Communities No. L 281/31, eur-lex.europa.eu, November 1995. [108] Brendan Van Alsenoy: “Regulating Data Protection: The Allocation of Respon‐ sibility and Risk Among Actors Involved in Personal Data Processing,” Thesis, KU Leuven Centre for IT and IP Law, August 2016.

<!-- page 574 -->

[109] Michiel Rhoen: “Beyond Consent: Improving Data Protection Through Con‐ sumer Protection Law,” Internet Policy Review, volume 5, number 1, March 2016. doi: 10.14763/2016.1.404 [110] Jessica Leber: “Your Data Footprint Is Affecting Your Life in Ways You Can’t Even Imagine,” fastcoexist.com, March 15, 2016. [111] Maciej Cegłowski: “Haunted by Data,” idlewords.com, October 2015. [112] Sam Thielman: “You Are Not What You Read: Librarians Purge User Data to Protect Privacy,” theguardian.com, January 13, 2016. [113] Conor Friedersdorf: “Edward Snowden’s Other Motive for Leaking,” theatlan‐ tic.com, May 13, 2014. [114] Phillip Rogaway: “The Moral Character of Cryptographic Work,” Cryptology ePrint 2015/1162, December 2015.

<!-- page 575 -->

Please note that the definitions in this glossary are short and sim‐ ple, intended to convey the core idea but not the full subtleties of a term. For more detail, please follow the references into the main text.

## asynchronous

Not waiting for something to complete (e.g., sending data over the network to another node), and not making any assumptions about how long it is going to take. See “Synchronous Versus Asynchro‐ nous Replication” on page 153, “Synchro‐ nous Versus Asynchronous Networks” on page 284, and “System Model and Reality” on page 306.

## atomic

1. In the context of concurrent operations: describing an operation that appears to take effect at a single point in time, so another concurrent process can never encounter the operation in a “halffinished” state. See also isolation.
2. In the context of transactions: grouping together a set of writes that must either all be committed or all be rolled back, even if faults occur. See “Atomicity” on page 223 and “Atomic Commit and Two-Phase Commit (2PC)” on page 354.

## backpressure

Forcing the sender of some data to slow down because the recipient cannot keep

up with it. Also known as flow control. See “Messaging Systems” on page 441.

## batch process

A computation that takes some fixed (and usually large) set of data as input and pro‐ duces some other data as output, without modifying the input. See Chapter 10.

## bounded

Having some known upper limit or size.

Used for example in the context of net‐ work delay (see “Timeouts and Unboun‐ ded Delays” on page 281) and datasets (see the introduction to Chapter 11).

## Byzantine fault

A node that behaves incorrectly in some arbitrary way, for example by sending contradictory or malicious messages to other nodes. See “Byzantine Faults” on page 304.

## cache

A component that remembers recently used data in order to speed up future reads of the same data. It is generally not complete: thus, if some data is missing from the cache, it has to be fetched from some underlying, slower data storage

<!-- page 576 -->

system that has a complete copy of the data.

## CAP theorem

