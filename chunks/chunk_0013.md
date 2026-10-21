The ease with which you can modify a data system, and adapt it to changing require‐ ments, is closely linked to its simplicity and its abstractions: simple and easy-tounderstand systems are usually easier to modify than complex ones. But since this is such an important idea, we will use a different word to refer to agility on a data sys‐ tem level: evolvability [34].

## Summary

In this chapter, we have explored some fundamental ways of thinking about dataintensive applications. These principles will guide us through the rest of the book, where we dive into deep technical detail.

An application has to meet various requirements in order to be useful. There are functional requirements (what it should do, such as allowing data to be stored, retrieved, searched, and processed in various ways), and some nonfunctional require‐ ments (general properties like security, reliability, compliance, scalability, compatibil‐ ity, and maintainability). In this chapter we discussed reliability, scalability, and maintainability in detail.

Reliability means making systems work correctly, even when faults occur. Faults can be in hardware (typically random and uncorrelated), software (bugs are typically sys‐ tematic and hard to deal with), and humans (who inevitably make mistakes from time to time). Fault-tolerance techniques can hide certain types of faults from the end user.

Scalability means having strategies for keeping performance good, even when load increases. In order to discuss scalability, we first need ways of describing load and performance quantitatively. We briefly looked at Twitter’s home timelines as an example of describing load, and response time percentiles as a way of measuring per‐

<!-- page 45 -->

formance. In a scalable system, you can add processing capacity in order to remain reliable under high load.

Maintainability has many facets, but in essence it’s about making life better for the engineering and operations teams who need to work with the system. Good abstrac‐ tions can help reduce complexity and make the system easier to modify and adapt for new use cases. Good operability means having good visibility into the system’s health, and having effective ways of managing it.

There is unfortunately no easy fix for making applications reliable, scalable, or main‐ tainable. However, there are certain patterns and techniques that keep reappearing in different kinds of applications. In the next few chapters we will take a look at some examples of data systems and analyze how they work toward those goals.

Later in the book, in Part III, we will look at patterns for systems that consist of sev‐ eral components working together, such as the one in Figure 1-1.

## References

[1] Michael Stonebraker and Uğur Çetintemel: “‘One Size Fits All’: An Idea Whose Time Has Come and Gone,” at 21st International Conference on Data Engineering (ICDE), April 2005.

[2] Walter L. Heimerdinger and Charles B. Weinstock: “A Conceptual Framework for System Fault Tolerance,” Technical Report CMU/SEI-92-TR-033, Software Engi‐ neering Institute, Carnegie Mellon University, October 1992. [3] Ding Yuan, Yu Luo, Xin Zhuang, et al.: “Simple Testing Can Prevent Most Criti‐ cal Failures: An Analysis of Production Failures in Distributed Data-Intensive Sys‐ tems,” at 11th USENIX Symposium on Operating Systems Design and Implementation (OSDI), October 2014. [4] Yury Izrailevsky and Ariel Tseitlin: “The Netflix Simian Army,” techblog.net‐ flix.com, July 19, 2011. [5] Daniel Ford, François Labelle, Florentina I. Popovici, et al.: “Availability in Glob‐ ally Distributed Storage Systems,” at 9th USENIX Symposium on Operating Systems Design and Implementation (OSDI), October 2010. [6] Brian Beach: “Hard Drive Reliability Update – Sep 2014,” backblaze.com, Septem‐ ber 23, 2014. [7] Laurie Voss: “AWS: The Good, the Bad and the Ugly,” blog.awe.sm, December 18, 2012.

<!-- page 46 -->

[8] Haryadi S. Gunawi, Mingzhe Hao, Tanakorn Leesatapornwongsa, et al.: “What Bugs Live in the Cloud?,” at 5th ACM Symposium on Cloud Computing (SoCC), November 2014. doi:10.1145/2670979.2670986

[9] Nelson Minar: “Leap Second Crashes Half the Internet,” somebits.com, July 3, 2012. [10] Amazon Web Services: “Summary of the Amazon EC2 and Amazon RDS Ser‐ vice Disruption in the US East Region,” aws.amazon.com, April 29, 2011. [11] Richard I. Cook: “How Complex Systems Fail,” Cognitive Technologies Labora‐ tory, April 2000. [12] Jay Kreps: “Getting Real About Distributed System Reliability,” blog.empathy‐ box.com, March 19, 2012. [13] David Oppenheimer, Archana Ganapathi, and David A. Patterson: “Why Do Internet Services Fail, and What Can Be Done About It?,” at 4th USENIX Symposium on Internet Technologies and Systems (USITS), March 2003. [14] Nathan Marz: “Principles of Software Engineering, Part 1,” nathanmarz.com, April 2, 2013. [15] Michael Jurewitz: “The Human Impact of Bugs,” jury.me, March 15, 2013. [16] Raffi Krikorian: “Timelines at Scale,” at QCon San Francisco, November 2012. [17] Martin Fowler: Patterns of Enterprise Application Architecture. Addison Wesley, 2002. ISBN: 978-0-321-12742-6 [18] Kelly Sommers: “After all that run around, what caused 500ms disk latency even when we replaced physical server?” twitter.com, November 13, 2014. [19] Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, et al.: “Dynamo: Ama‐ zon’s Highly Available Key-Value Store,” at 21st ACM Symposium on Operating Sys‐ tems Principles (SOSP), October 2007. [20] Greg Linden: “Make Data Useful,” slides from presentation at Stanford Univer‐ sity Data Mining class (CS345), December 2006. [21] Tammy Everts: “The Real Cost of Slow Time vs Downtime,” webperformanceto‐ day.com, November 12, 2014. [22] Jake Brutlag: “Speed Matters for Google Web Search,” googleresearch.blog‐ spot.co.uk, June 22, 2009. [23] Tyler Treat: “Everything You Know About Latency Is Wrong,” bravenew‐ geek.com, December 12, 2015.

<!-- page 47 -->

