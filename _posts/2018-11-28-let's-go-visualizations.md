It's been about 2 weeks since the latest Pokémon game release and let me tell you, it's amazing. In this version of the classic RPG we are back in pallet town, a remake of the original games. Pokémon Let's Go: Eevee & Pikachu are amazing, but you don't have to take my word for it. Let's go ask the good people of Twitter dot com. 

![](/images/pokemon_teaser.jpg)

## Pulling Tweets
We're going to use the RTweet package to pull tweets that use one of the three hashtags: #PokemonLet'sGo, #TeamEeve, #TeamPikachu

If you're unfamiliar with the Pokémon franchise, there are often 2 mostly identical games released at a time with the major difference being that some Pokés are only in one game or the other. In Pokemon Let's Go, your choice in game determines who rides around on your shoulder and becomes your new BFF. I am #TeamEevee foreva. Eevee has a combination of strength, a fun array of moves, and the potential to be anything. Plus, who wants to walk around with a [murderous death trap rat](https://tomrocksmaths.com/2017/07/04/pokemaths-how-many-pikachus-does-it-take-to-power-a-light-bulb/) on their shoulder?

Previously, I've made a developer license and prepped connecting to Twitter. 
```r
library(rtweet)
#### Connect to Twitter ####
setwd("C:/Users/mt186048/Documents/Projects - Data Science")
load("twitter authentication.Rdata")

create_token(
  app = "my_twitter_research_app",
  consumer_key = cred$consumerKey,
  consumer_secret = cred$consumerSecret,
  access_token = cred$oauthKey,
  access_secret = cred$oauthSecret
)
rm(cred)
```

We can then pull the last tweets that use one of our 3 hashtags. We're going to look for only English tweets, although I can assure you this is a great game in any language. By using the RetryOnRateLimit flag we can get more than the 18K Tweets that you're allowed to pull per 15 minutes. This took an hour or so to run, because each time we grabbed 18K tweets we waited 15 minutes to try again. 

```r
#### Pull Pokemon Tweets ####
poke_tbl <-  search_tweets("#PokemonLetsGo OR #TeamEevee OR #TeamPikachu"
        , n = 1000000
        , lang = "en"
        , include_rts = FALSE
        , retryonratelimit = TRUE
)
```

We end up with 55,085 tweets and 88 variables about these. Let's get exploring!

## Tweets Over Time
The RTweet package comes with a nifty function called ts_plot which will allow us to choose various intervals of time to see how many tweets are happening. Let's group by hour:
```r
ts_plot(poke_tbl,"hour")
```
![](/images/pokemon_tweets_over_time_1.PNG)

We can quickly see that even though we asked Twitter for 1 MILLION TWEETS, we did not get all tweets.  The release date was November 16th but our earliest tweets are the 18th. We also see there is a steady decline as the hype dies down.

Using GGPlot, let's gussy-up our plot a little with titles and a beautiful background of myself and my new best friend Eeevee.
```r
tm_grp <- data.frame(table(cut(poke_tbl$created_at, breaks="hour")))

ggplot(data = tm_grp, aes(x = as.POSIXct(Var1), y =Freq)) +
  background_image(readJPEG("pokemon_background.jpeg")) +
  geom_line(aes(group = 1), color="#FFFFFF",size=2) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) + 
  theme(plot.title = element_text(size=20, face="bold",margin = margin(10,0,10,0))) +
  theme(axis.ticks.y = element_blank(),axis.ticks.x = element_blank()) +
  labs(
    x = "",
    y = "Frequency of Tweets",
    title = "Time series of Pokemon Let's Go Tweets",
    subtitle = "Frequency of Twitter statuses calculated in one-hour intervals."
  )

```
![](/images/pokemon_tweets_over_time.PNG)


## Word Clouds of Hashtags
Yes yes yes I know, word clouds are this generation's Comic Sans. But they are a quick and easy way to see common words, so we're going for it. 

Our base data has a list of hashtags used in each tweet. We'll use pipes to:

 1. Split each list into individual hashtags
 2. Set all hashtags to lowercase
 3. Count how many times each hashtag occurs
 4. Only keep tags that happen at least 10 times

```r
library(dplyr)
library(tidytext)
library(stringr)
library(wordcloud2)

pokeTags <- poke_tbl %>% 
  unnest(hashtags) %>% 
  mutate(hashtags = tolower(hashtags)) %>%
  count(hashtags, sort = TRUE) %>%
  filter(n > 10)
```
![](/images/pokemon_hashtag_wordcloud.png)

As expected, lots of reference to Pikachu, Eevee, and shinies (rare colored critters that show up some times). The large number of Nintendo related tags come from people who tweet directly from the game, which is played on the Nintendo Switch and forces its own hashtag.

## What's Next
So far we have done some preliminary exploring and visualizing of our data set. No we haven't done any Machine Learning or model building, but we have a comfortable idea of what's in our dataset and what types of things we could use it to figure out. In the next post(s) we'll look at:

 - Who's more loved, Eevee or Pikachu?
 - What's the sentiment of tweets, does twitter dot com love this game as much as me?
 - What are the topics of tweets?
 - Are the people tweeting about Let's Go "gamers"? Do they normally tweet about games, or is this new for them?
 - What are the most popular tweets?
 - Which shiny pokes are being found (or at least tweeted about) the most?
