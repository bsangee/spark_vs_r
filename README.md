# Spark vs R
Repository for collaboration between Eastman and Virginia Tech regarding R and Spark performance

## Goal
Understand the business value of using Spark.  When does the performance benefit outweigh the setup and training costs of Spark?

## Measures
Interested in time to compute various analytics using R and Spark.  Spark's capabilities are detailed online.  The picture below highlights the methods to be measured.

![Picture](www/SparkML.png)

## Data
Data comes from two places:
* Airline Data (http://stat-computing.org/dataexpo/2009/)
* Text Data (http://archive.ics.uci.edu/ml/datasets/Bag+of+Words)

### Data subgroups
We're interested in testing the above measures on 'small', 'medium' and 'big' data as well as 'narrow' and 'wide' data.  The definitions of these are as follows:

            Narrow   Wide
           -----------------
     Small |   1   |   4   |
    Medium |   2   |   5   |
       Big |   3   |   6   |
           -----------------

#### Airline Data

                ?????    ????
              ------------------
         1988 |       |        |
    1987-1995 |       |        |
    1987-2008 |       |        |
              ------------------
