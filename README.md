# WGUPS_Routing_Program
A package delivery routing program displaying the use of various data structures and algorithms in Python.
This is an altered and abbreviated version of the paper that was required to be turned in with this program.

WGU STUDENTS: COPYING THIS WILL RESULT IN A > 30% SIMILARITY MATCH TO MY PAPER. DO YOUR OWN WORK!!

----------

The WGUPS Scenario

  This paper is the required analysis of a program developed for the Western Governors University Parcel Service. The goal of this program is to unite at least one self-adjusting data structure, hashing algorithms, and at least one named algorithm to route delivery trucks to meet the package delivery needs of the WGUPS. The paper analyzes the Big-O complexity and efficiency of the developed program, details the development environment, discusses the scalability, adaptability, and maintainability of the program. Also discussed are the self-adjusting data structure and algorithm implemented in the program along with other possible alternatives. Screenshots displaying the working program were included in the original paper but are not available with this.

----------

******stop reading here if you don't need all of the computer science-y details******

******WGU STUDENTS: COPYING THIS WILL RESULT IN A > 30% SIMILARITY MATCH TO MY PAPER. DO YOUR OWN WORK!!******


DEVELOPMENT ENVIRONMENT

	Software: Python version 3.9, PyCharm 2021.1 Community Edition
    Hardware: Desktop PC - Windows 10 Pro, Dual Core @3.50 GHz with 16 GB RAM
	Excel to CSV conversion: Manually removed header rows in Excel and exported to a CSV file. 
  
LOGIC COMMENTS

Program Outline/Overview:

  •	Read in the two data files  
    o	Read in the data for and create the distance table (table containing each possible combination of address pairs and the distance between the specified pair).   
    o	Read in the data for and create each package object which is placed in a hash table.
    
  •	Process the input data:  
    o	Sort packages into trucks according to special notes and delivery deadlines.    
    o	Utilize Nearest Neighbor algorithm* to sort the packages of each truck into an acceptably efficient delivery route.    
    o	Deliver the packages of each truck’s list keeping track of the following:    
      -	Truck’s traveled mileage.      
      -	Times of change of delivery status for each package.     
      
  •	Initiate a simple user interface to access the following information:  
    o	Package data:    
      -	Individually, either with or without a specified time being queried.      
      -	For all packages at a given point in time.      
	o	Total mileage of all trucks involved in delivering packages
  
  
*Nearest Neighbor algorithm
Utilizes data from the package objects stored in the hash table and data in the distance table to find the shortest distance from the last package (passed as a parameter to the method), then continuing through the truck’s package list to find the next closest possible delivery until all packages are sorted into a sequential route for that truck. Note: the truck sub-list parameter is a list of packages with the same delivery deadline, created from the complete truck’s package list 

ALGORITHM IDENTIFICATION
	In this program the Nearest Neighbor algorithm, a type of Greedy Algorithm, is used to determine an acceptably optimized path for the WGUPS delivery system. The phrase acceptably optimized is used in this case since this problem, which is much like the Traveling Salesman Problem, can have an increasingly large set of data points (packages, in this case), making it more and more difficult and computationally expensive to find the absolutely optimal solution. For this program, an acceptably optimized solution is one where all special notes requirements are met, all delivery deadlines are met, and the total miles traveled by all delivery trucks is less than 140.  

SPACE-TIME AND BIG-O

The Big-O notation for each of the files for this program are as follows:

  1.	main.py – O(N)
    a.	in menu feedback, option 2 loops to print all packages so is O(N)
	
  2.	package.py – O(1)
    a.	all methods in this class definition deal with updating, setting, getting, or printing only one package object – there are no loops
	
  3.	package_hash_table.py – O(N)
    a.	each method (remove, insert, search [the look-up], get id list, get package list) goes though the package hash table a maximum of one time so, O(N)
	
  4.	truck.py – O(N2)	
    a.	deliver packages: O(N)
    b.	organize truck route: O(N)
    c.	nearest neighbor sort: O(N2)
    d.	packages to trucks: O(N2)
	
  5.	import_data.py – O(N2)
    a.	fill distance table: O(N2)
    b.	fill package table: O(N)
    c.	get distance: O(N)
	
Overall time complexity of the program: O(N2)

WGU STUDENTS: COPYING THIS WILL RESULT IN A > 30% SIMILARITY MATCH TO MY PAPER. DO YOUR OWN WORK!!

SOFTWARE EFFICIENCY AND MAINTAINABILITY
  The overall efficiency of the program is O(N2). [See above for details]
  The maintainability of the program involves three main factors: clear and descriptive comments, method and variable names that are also descriptive and understandable, and using object-oriented concepts to help organize code segments. The methods in this program have comments describing what process it is doing as well as short descriptive comments of what is happening throughout the method. The methods and variables are also descriptive of either what they represent or what they do.
  The program is organized into five python files: a main file, three class files, and a file built for importing data from outside files. The three class files implement one of the following: a package object, a truck object, and a package hash table. Each class file contains its initialization method and any other method called by or specifically related to the file’s class object. The main.py file contains the code to start the program and to implement the user interface (a simple menu). Finally, the import_data.py file contains three methods: one to fill the package hash table from the provided package file, one to fill the distance list from the provided distance table, and one method to get the distance from the distance list.

SCALABILITY AND ADAPTABILITY
	 Both the chaining hash table of package objects and the list of distances between two addresses were created with the ability to add more packages and package information. Because they use a list data type as the basis of their construction, they can accommodate additional packages and their associated distance information.
	The nearest neighbor algorithm tends to become less efficient as the data set it processes becomes larger. In this case, the maximum number of possible data entries to be processed remains small, assuming the package capacity of the delivery trucks does not change. However, as the number of packages increase past what three full trucks can hold, there will also be additional executions of the nearest neighbor sort to accommodate either more trucks or more truck loads.

STRENGTHS OF THE CHOSEN ALGORITHM
  One of the strengths of the Nearest Neighbor algorithm is that it is relatively simple to understand and implement. The method begins with receiving a list of packages with the same time constraints from a truck. The package with the nearest address to the last delivery is found. That package is moved to the end of the sorted list of packages until there are no packages in the method’s received list of packages. Then the sorted list is returned.
  A second strength of using Nearest Neighbor algorithm for this program is specifically related to the size of lists that are being sorted. The trucks have a package limit of only 16. Because the list being sorted is a single list and is small, the Nearest Neighbor algorithm completes this sort quickly.
  
OTHER POSSIBLE ALGORITHMS AND THEIR DIFFERENCES
  The two other possible algorithms I will be looking at are Dijkstra’s Shortest Path algorithm and the Brute Force algorithm. Dijkstra’s Shortest Path algorithm is like the Nearest Neighbor algorithm except it implements a more complex graph data structure which includes the edge weight (distance) and the predecessor pointer in addition to the package data associated with each vertex. The Brute Force algorithm can be implemented with the same data structures to find every possible iteration of the delivery route and then compare them all to find the shortest route. They would meet the program’s requirements by coming up with either a reasonably short or the shortest (respectively) possible path for the given packages on a truck.
  Dijkstra’s Shortest Path algorithm  is like the Nearest Neighbor algorithm that is implemented in that it may not find the most optimized path, but it finds one that is reasonably optimized without using a great deal of computational resources. However, its implementation is more complex than the Nearest Neighbor because it uses a graph class object which tracks not only the ID/package data associated with a vertex, but also maintains a predecessor vertex and the distance as an edge weight. For Dijkstra’s, once the smallest edge weight of adjacent vertices is found, the information regarding the path order and path length are updated and maintained in the graph object. However, for the Nearest Neighbor the path order is stored by creating an ordered list of ID/package pairs and the total distance of the route must be calculated as the deliveries are made. 
	The Brute Force algorithm is expensive computationally and has the potential to also be spatially expensive. Since brute force determines every possible delivery route for a truck’s 16 packages, it uses a lot of computational time creating all the possible routes for a full truck. It could also use a great deal of memory if the algorithm creates all the routes before computing and comparing their lengths. Even if the comparison of the route lengths is done as the routes are created by comparing only two routes at a time and discarding the longer of the two, thus keeping memory use to a minimum, the computation of all of those routes and their total distance is more expensive than the nearest neighbor which searches the distance table for the next closest delivery address from the remaining packages in the truck list and builds an reasonably well-ordered list of packages.

WGU STUDENTS: COPYING THIS WILL RESULT IN A > 30% SIMILARITY MATCH TO MY PAPER. DO YOUR OWN WORK!!
    
SELF-ADJUSTING DATA STRUCTURES
	The chaining hash table in this program is built using lists which are mutable data types, giving the hash table the ability to adapt to a growing number of packages to be delivered. Because the package ID numbers are sequential integers, the distribution of packages to the hash table’s ten buckets (or rows depending on how you choose to visualize it) is almost exactly even. The result of such an even distribution is that a search within one bucket of the hash table will not be significantly more resources than a search in any other bucket in that hash table. The hash table is an efficient look-up for the provided scenario. However, it does lose efficiency as the buckets’ chains get longer.  

EXPLANATION OF DATA STRUCTURE (CHAINING HASH TABLE)
	The chaining hash table defined in package_hash_table.py is the self-adjusting data structure that stores and retrieves the full collection of package data for this program. The full table is a list of lists of lists. The top-level or outer most list containing the hashed value of the package ID (using hash(ID) modulo table length of 10) creating ten “buckets” or lists into which a short list of [package ID, package] pairs can be placed. Because the table is built using lists, it is relatively simple to add or remove a package from a bucket as needed.
	Because the package IDs are sequential integers, the hash method creates a table that has an even distribution of [ID, package] pairs. This makes it so a search of any one of the table’s buckets is not significantly longer than any other because each bucket (a.k.a., list) contains a near equal number of [ID, package] entries to search. Utilizing lists organized by hashed ID values allows for a shorter search time because the hashed ID value will only be found in one of the table’s buckets, so only that bucket needs to be searched rather than the entire collection of [ID, package] pairs.

DATA STRUCTURE EFFICIENCY
  The look-up function is designed to find a single package within the package hash table which has been built using lists. The result is a table-like structure where the table’s top or first row corresponds to a hashed package ID value of 0, the second row corresponds to a hashed package ID value of 1, and so on through the last row corresponding to a hashed package ID of 9. Because the package IDs stored in these rows, or “buckets,” are sequential integers, it requires ten packages to add a single new [ID, package] pair to each of the table’s rows. 
  This structure allows the look-up function’s time efficiency to reduce slowly as the overall number of packages increase. For example, the loading of the original package data creates a chaining hash table of 10 rows that are 4 [ID, package] pairs deep. When the look-up finds the row that corresponds to the hashed ID number, it only has the four packages in that row to perform a linear search to find the specified ID in a worst-case scenario. Increasing the number of packages in the table by 10 only increases the more costly linear search’s worst-case by 1 (up to 5 package IDs to search from the initial 4) for any ID look-up.

DATA STRUCTURE OVERHEAD & IMPLICATIONS
	There is a direct relationship between the number of packages being delivered and the space used to store said packages. For every package, the package’s ID and the package’s object location is stored as a key-value pair in a bucket of the hash table. No matter how many [ID, package] pairs are added to the hash table, each requires the same amount of space be added to the end of their corresponding list.
	In this program, the use of the hash table is not related to neither the trucks nor the package’s address. When the user looks up either a single package or a list of all packages in the user interface, the request runs directly though the hash table. Because of this, changes to the number of trucks or cities should not affect look-up time – only a change in the number of packages would affect a change.

WGU STUDENTS: COPYING THIS WILL RESULT IN A > 30% SIMILARITY MATCH TO MY PAPER. DO YOUR OWN WORK!!

OTHER POSSIBLE DATA STRUCTURES
	A list of key-value pairs could be used in place of a hash table to meet the requirements of this scenario. A list, being a mutable object, would allow a package to be removed, added, or even assigned to a different ID number (key) if the program had need for it, much like the hash table that is used which is built using lists.  The space requirement of a simple list would be slightly less than a hash table as it would not have an index-style list or array of a hash table to provide direction to the table’s sub-lists (a.k.a., rows or buckets). This data structure could be used with a variety of search algorithms including a linear search with time complexity of O(N) or a binary search with a search complexity of O(log N).
	An AVL tree as described in our course materials is another possible data structure for this program. Given that the provided number of packages to be delivered is 40, the height of the AVL tree for this program would be 6 levels high. For our current number of packages, it provides no real improvement on look-up time performance. Since a hash table with ten buckets, holding 40 items is only 4 buckets deep compared to the AVL’s search tree with 40 items being 6 levels high, the hash table’s search is more efficient. Between 60 – 70 total packages to be delivered, the performance of the AVL tree and the hash table are approximately the same. However, as the number of packages to be delivered approaches 100, the time efficiency of the look-up begins to favor of the AVL tree. This time efficiency of the AVL tree continues to grow rapidly as the number of packages to be delivered grows beyond 100 making it the better choice for larger groups of packages.

DATA STRUCTURE DIFFERENCES
	The list of key-value pairs is a simpler implementation than the hash table. They are both mutable data structures because they are built using a list. The hash table is a bit more complex because it is essentially a list of lists which contain a short key-value pair, also in a list. The table’s additional level of complexity is in the array of lists which make it possible to improve time performance of searches though the use of hashing.
	The AVL tree is more complex than the implemented hash table. In addition to the key-value pair, the AVL tree (a type of Binary Search Tree) node also keeps track of the parent node, left child node, and right child node.  When inserting or removing the AVL tree must take into consideration the node’s balance factor and adjust the AVL tree (rebalancing) to keep it balanced. The implementation needed to keep the AVL tree balanced makes it more complex to implement than the hash table. However, the structure of the AVL tree makes it much more efficient for look-up functions if it is storing many items.
The submission accurately describes attributes of both data structures identified in part K2 and compares these to Part D’s data structure attributes.

VERIFICATION OF REQUIREMENTS FOR PROGRAM'S DATA STRUCTURE & ALGORITHM
  The data structure and algorithm for this program have met the following defined requirements:
    •	Any special note that may have been defined for a package has been met.
    •	All packages were delivered on time as defined by the package’s delivery deadline
    •	The total number of miles traveled by all the delivery trucks is 111.9

HOW WOULD I APPROACH THIS DIFFERENTLY?
  There are several things I would do differently if I were to do a project like this again. To keep this paper a reasonable length, here are some of the bigger changes I would make:
   1. Better planning to use the actual package more rather than the package ID. This would reduce the number of times the program does a search for the package. Also, it would hopefully reduce some of the confusion I had as to whether the code of a method was using the package or the package ID and whether a search for the package was needed to make a call for the package’s information such as an address or delivery deadline.
   2. The implementation of the distance table was the first thing I worked on for this program and could have been much better. If implemented with a table-like structure like the package hash table was, the search for distance values could be greatly reduced from their current liner search. This is a good example on how a little work up front, or in the initialization of the program can save much time and energy in later parts of the program. This is especially true if the number of packages to be delivered is greatly increased.
   3. Another change I would make to the initial intake of data is to reformat the delivery deadline for each package to a 24-hour, or military time, format. There are a small number of time comparisons with the delivery deadline piece of data as the packages are being sorted into trucks and into routes. Having the delivery deadline in the package object in a 24-hour format would make the coding for these comparisons much easier.
   4. Finally, I would alter the way the packages are sorted “onto trucks”. This is because I believe the optimization of the routes could be better. However, this is not something I have yet put a great deal of thought into how I would change & implement this.

WGU STUDENTS: COPYING THIS WILL RESULT IN A > 30% SIMILARITY MATCH TO MY PAPER. DO YOUR OWN WORK!! (Yes, about this I am a jerk. You can learn this just like I did!)
