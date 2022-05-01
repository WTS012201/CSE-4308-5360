Name:   William Sigala
ID:     1001730022

Python was used for both task.
Code is structured as follows: 
-   In task1/compute_a_posteriori.py 
-   prob_candy is used for calculating probability of a candy at a position in the sequence
-   prob_hyp is the recursive function used for calculating every probability
    of each hypothesis at a position in the sequence.
-   main

-   In task2/bnet.py 
-   In class bnet 
-   case method for calculating probability of a specific case
-   truth_vals for making a table for unspecified values
-   computeProbability for calculating probability of the joint distribution
-   In main at the bottom, computeProbability of numerator and denominator (if "given" in args) and divide 