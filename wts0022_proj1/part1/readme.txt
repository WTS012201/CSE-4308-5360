Name:   William Sigala
ID:     1001730022

C++ was used for this task. I don't believe that it is omega compatible.

Code is structured as follows: 
-   Edge object at top of file
-   Functions for Loading in data from file
-   Graph object used for the searches.
-   Graph data at the top
-   Constructor for graph using the data from the file
-   The print_route method for the search
-   The find_route algorithm used for both uniformed and informed search
-   main

To compile, use g++ with standard c++17:
g++ -std=c++17 find_route.cpp -o find_route

Run program as specified in the instructions
ex: ./find_route input1.txt Bremen Kassel