# Melbourne-StackOverFlow-users-ranking
Application for user to input StackOverFlow profile URL, and see his ranking among all Melbourne StackOverFlow users.
#### _**To quickly understand how this program works, watch ['this'](https://youtu.be/hm2J23zugUU) video clips!**_


## How to run the code
1.  Download 'app.py' and 'data.csv' in the same folder.
2.	Run 'app.py' file. 
3.	After running the script, we can see the user interface, input any StackOverFlow profile's URL. (e.g.: https://stackoverflow.com/users/696257/dkulkarni)
4.	Click button 'See your ranking in Melbourne'.
5.	Result shows (1)your reputation, (2)your rank in Melbourne, (3)percentage over all Melbourne StackOverFlow users, and (4)where you are at the Histogram of Melbourne StackOverFlow users' reputation.
6.  The 'data analysis.py' is used to estimate total users number, 'scrap data.py' is the file to scrap reputation information of all Melbourne StackOverFlow users.

## Implementation details
#### Step1. Statistics of all StackOverFlow users' reputation in Melbourne

<div align=center><img width="300" height="300" src="https://github.com/suinaowawa/Melbourne-StackOverFlow-users-ranking/blob/master/figures/3.PNG"/></div>

The website to scrap all users reputation is ['this'](https://stackoverflow.com/users?page=%d&tab=Reputation&filter=all)

On each page, search through all users and filter out the user location with 'Melbourne', record their reputation and page number in pandas dataframe.

On this website there are in total 304,877 and it's keep growing! To scrap all data requires a huge amount of time. 

Realizing that most of the users are those with low reputation 1, in this program a total of 93,878 pages were scrapped, and 5,664 Melbourne users were found. The rest of the users are all with reputation 1.

#### Step2. Data analysis

<div align=center><img width="400" height="300" src="https://github.com/suinaowawa/Melbourne-StackOverFlow-users-ranking/blob/master/figures/2.PNG"/></div>

Because there remaining many pages unsearched. We need to estimate the remaining Melbourne users. 

By plotting the relationship between page number with founder users count, we can do the curve fitting on the data and estimate the total Melbourne users.

Using polynomial fit of degrees 3, the estimated total Melbourne users are 151,601, given a total pages of 304,877.

#### Step3. The Appication

![Alt text](https://github.com/suinaowawa/Melbourne-StackOverFlow-users-ranking/blob/master/figures/1.PNG)

When user input the URL, get the reputation from that URL, then compare it with the data we got in step1 by reordering the pandas dataframe by the reputation column.

When we get the rank, divide by the total Melbourne users we estimate in step2 to get the percentage.
The histogram is to let the users have a more comprehensive understanding of which level they are at.

#### Total time for scrap data: 29.5 h
