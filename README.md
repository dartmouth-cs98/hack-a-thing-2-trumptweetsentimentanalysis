# hack-a-thing-2-trumptweetsentimentanalysis
hack-a-thing-2-trumptweetsentimentanalysis created by GitHub Classroom

Trump Tweets is a side-project I made based on a hunch that the tweets of President Trump has an effect on the stock market. For this project, I used the python-twitter api, IBM Watson Tone Analyzer api, and AlphaVantage Stock api. The program will first pull the 200 most recent tweets from Donald Trump's account. Next, it analyzes the tone of each of these tweets and adds them to a dictionary containing the tones of all the tweets for that day. Finally, it pulls historic stock price information for the S&P 500 and calculates the day's price change. The `trump_tweets` dictionary contains the following structure:

`trump_tweets[date] = {[[tones for all the days tweets in a list], S&P 500 price change]}`

Once the data is pulled, parsed, and organized, the user is given an input prompt. When a date is entered, the program will find the most common tone of trumps tweets for the day and output the tone and the price change for the day. 

I am interested in using a sentiment analysis for my CS98 project, so this was a perfect way to test out the IBM Watson api and play around with how it worked. Additionally, I wanted to analyze an outside data source, so trump tweets were a good data set to try out.

I worked on this project alone since the assignment webpage says: "Who did what (if you worked with someone else)", so I ended up working on this by myself.

What didn't work: I wanted to make the stock market price change more specific than the entire day's movement, however all free apis only had historic data by day. To find hourly historic data, I would have needed to pay for a more advanced stock price api. If I were improving this project, I would try to find a better stock price api that gives more specific historic prices so I could see what impact the tweets had on the market in the subsequent hour. 
