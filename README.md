# Table of Contents
1. [Introduction](README.md#introduction)
2. [Summary of Approach](README.md#summary-of-approach)
3. [Dependencies](README.md#dependencies)
4. [Run Instructions](README.md#run-instructions)

# Introduction

I've taken a few computer science classes over the course of my education, but by training I'm a Statistician. That's what my Masters Degree is in. So while I can analyze data and implement algorithms, I'm by no means a computer scientist. I hope what I've written lives up to expectations or at least the expectations you would have for what "clean" code looks like. I definitely had an interesting time writing it. If there are any questions, I can be reached at info@victorwying.com.

# Summary of Approach

An outer loop that iterates over each line of the .log file and an inner loop  checks whether or not the information contained in the $i^{th}$ line of the .log file either identifies the start of a new session or the end or extension of an "active" one.

Two Python dictionaries need to be defined -- 1) the "Active" dictionary of information of currently active user sessions (those where at least one request has been observed but where the threshold for inactivity has not been exceeded) containing the following information for each of the $n_i$ dictionary key-value pairs that exist in the current state of the Active dictionary -- that is, the state of the dictionary during the $i^{th}$ iteration of the outer loop, which is the one corresponding to the $i^{th}$ line of the log.csv file:

  * an IP address IP$_j$
  * $t_{1,j}$ := the date-time of IP$_j$'s first page request
  * $t_{n,j}$ := the date-time of IP$_j$'s last page request so far
  * $n_{j,i}$ := the running total of page requests from IP$_j$ at time $i$

The "Add" dictionary also contain the above information, but for IP addresses waiting to be added to the Active dictionary.

Here is an outline of the process:

1. For every line of the log file ($i = 1, ..., n$):
  i) Is the IP address in the dictionary of "active" sessions?
    A) If not, make a note of this somewhere, so that it can be added later.
    B) If so, then continue to step 2.
2. For the $j=1,...,n_i$ IPs in the **Active** dictionary during the $i^{th} iteration of the outer loop:
    A) Does the amount of time between $IP_j$'s last page request and the current page request exceed the threshold value? 
      i) If so, then add an entry for $IP_j$ into sessionize.txt.
        a) Did the page request come from $IP_j$?
          1a) If so, then it defines the start of a new session and should be added to the list (technically, dictionary) of IPs( and associated information (first/latest page requests and number of page requests so far)).
          1b) If not, proceed to step A) and continue for $IP_{j+1}.
      ii) If not, did the page request come from $IP_j$?
        a) If not, then proceed to step A) and continue for $IP_{j+1}$.
        b) If so, then update the entry for $IP_j$ in the Active dictionary

Maybe a diagram illustrates this better:

![First second illustration](images/approach.png)

# Dependencies

The following libraries and modules are required:

    sys
    csv
    datetime.dt
    datetime.timedelta

I wrote my script in Python 3.

# Run Instructions

Run the executable `run.sh` script in the topmost folder of my submission or enter the following in the terminal:

    python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
    
# Conclusion

I hope I get accepted.

Have a pleasant day!# insight-data-engineering-coding-challenge
