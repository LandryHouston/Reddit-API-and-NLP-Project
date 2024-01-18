# Reddit API and NLP Project

## Project Objective

In this project, we take a look at two subreddits r/Anxiety and r/Depression. The goal of this project is to develop a natural language processing model that can predict which subreddit the post came from. The purpose of comparing these two subreddits can offer several benefits such as being able to help provide targeted support, research opportunities, and understanding the overlap between depression and anxiety. A model that is considered to be successful minimizes both false positives and negatives. This project aids in deciding which subreddit someone can relate to more and possibly helps them get a better direction on the support they need.

## Subreddit API Web Scraping

I used Python and the requests library to gather information from new subreddit posts such as Title and Text. I made a function that pulls as much data as the Reddit API will let us, from the subreddit of choice. On the initial scrape, it will export the data to a CSV file. After the initial scrape, future scrapes will compare the new data to the existing data and remove duplicates. The nonduplicates are then added to the existing CSV file. Every time the script is run, the date and time, number of new posts pulled, and total number of posts pulled are logged and saved as a text file.

I did set up a Windows scheduler to automatically run a batch file that runs the Python script every hour. On average, 10 to 20 posts are pulled per hour from each subreddit.

## Data

In the data folder, you'll find both raw and clean datasets for each subreddit, as well as a combined clean dataset. The data consists of 5 rows containing essential information from each post that will help the model with its predictions.

### Data Dictionary

| Feature   | Type     | Description               |
| --------- | -------- | ------------------------- |
| id        | object   | Post ID                   |
| subreddit | object   | Reddit community          |
| date      | datetime | Date of post (yyyy-mm-dd) |
| title     | object   | Title of post             |
| text      | object   | Text within a post        |

## Data Cleaning and Analysis

The data collected was cleaned first by removing rows containing null values. The only column with null values is the 'text' column. They are considered null because they do not contain any text. This is usually because there will be a picture or video link instead of text and the text will be posted as the first comment if at all. This is a very small amount of posts being removed because most posts in these subreddits contain only text.

The 'date' column was converted from Coordinated Universal Time (UTC) to datetime for readability. The hour and minute of the post were irrelevant so I only saved the year, month, and day. The data was then saved as clean_reddit_anxiety.csv and clean_reddit_depression.csv. A CSV of the combined data was also saved as clean_combined.csv.

Additional columns were made to help analyze the data such as text and title word count, and text and title length. By doing this we can notice that on average, post titles from each subreddit are the same, however, text from the Depression subreddit is much lengthier.

I was also able to get the most commonly used words from the posts. Apart from "anxious" or "depressed" being common, they both include similar descriptive words about how someone is feeling.

## NLP Model

Before modeling the data had to undergo a preprocessing step which involved tokenizing the text, removing stop words, and stemming the words. The target column also needed to be binarized, changing Depression to 0 and Anxiety to 1.

Eleven different models were created using a different mixture of vectorization and classification methods.

A vectorizer is a tool that converts text data into numerical vectors.<br>
Vectorizers used include:

-   CountVectorizer
-   TfidfVectorizer.

A classifier is a machine learning model that assigns categories or labels to input data based on its features. It learns patterns from training data and makes predictions on new, unseen data.<br>
Classifiers used include:

-   RandomForestClassifier
-   ExtraTreesClassifier
-   KNeighborsClassifier
-   GradientBoostingClassifier
-   BernoulliNB
-   LogisticRegression

A pipeline along with a grid search cross-validation technique made it easy to set parameters and make predictions on the data.

One model stood out as the best due to having low false positives and negatives as well as a high prediction score compared to the others. This model utilized a TfidfVectorizer and LogisticRegression resulting in predictions above 90% accuracy

## Conclusion

In summary, I was able to successfully create a natural language processing model to predict whether Reddit posts belong to r/Anxiety or r/Depression. The process included web scraping, data cleaning, and the development of nine models. The standout model, using TfidfVectorizer and Logistic Regression, achieved over 90% accuracy with low false positives and negatives. This model can guide individuals to the most relevant subreddit for support, contributing to a more personalized mental health community.
