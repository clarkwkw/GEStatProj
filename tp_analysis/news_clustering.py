import preprocessing

news_dir = "./news_crawler/guardian/texts"

news_samples = preprocessing.news_sample.get_samples(news_dir)

print(news_samples[0].id)