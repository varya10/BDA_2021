import json, re, unicodedata, nltk
#from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

cnt = 0
def get_stopwords(text):
	stop_en = set(stopwords.words('english'))
	#tokens = word_tokenize(text)
	filtered = [word for word in text.split() if word.lower() not in stop_en]
	res = ' '.join(filtered)
	return res


with open('sample_data.json', 'r', encoding='utf-8') as infile:
	with open('preprocessed_fin.txt', 'w', encoding='utf-8') as out:
		for element in infile:
			json_object = json.loads(element)
			#blank lines \n, \r, etc.
			tweet = re.sub(r'(\r\n)+|\r+|\n+|\t+', ' ', json_object['text'])
			#username/hashtags
			tweet = re.sub(r"@[A-Za-z0-9_]+","", tweet)
			tweet = re.sub(r"#[A-Za-z0-9_]\S+",'', tweet)
			#url/address
			tweet = re.sub(r'https?://\S+', ' ', tweet)
			tweet = re.sub(r'HTTPS?://\S+', ' ', tweet)
			tweet = re.sub(r"www\.\w+([-.]\w+)*\.\w+([-.]\w+)*", ' ', tweet)
			tweet = re.sub(r'\/\w\S+\.html\S+|\/\w\S+\.html|\w+\.html', ' ', tweet)
			#pics
			tweet = re.sub(r"pic.twitter\S+", " ",tweet)
			tweet = re.sub(r'\S+\.(jpg|jpeg|png|gif)', ' ', tweet)
			#leftover
			tweet = re.sub(r'&amp;|amp;', '&', tweet)
			tweet = re.sub(r'&.,|&#\d+', '', tweet)
			#normalise unicode chars
			tweet = unicodedata.normalize('NFKD', tweet).encode('ascii','ignore').decode('ascii')
			#remove punctuation
			tweet = re.sub(r'[^\w\s]', ' ', tweet)
			#multiple whitespace to one
			tweet = re.sub(r' +', ' ', tweet)
			#filter stopwords
			tweet = get_stopwords(tweet)
			#print(tweet)
			out.write(tweet)
			out.write('\n')
			cnt += 1