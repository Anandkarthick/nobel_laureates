import requests
import random

class NobelData:

    def __init__(self) -> None:
        self.base_api_url = "http://api.nobelprize.org/2.0/nobelPrizes"
        self.user_agents=[ "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 RuxitSynthetic/1.0 v9860405151 t2359546008474051152 athfa3c3975 altpub cvcv=2 smf=0 svfu=1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 RuxitSynthetic/1.0 v6110379358065498852 t1971513496641754615 ath1fb31b7a altpriv cvcv=2 smf=0 svfu=1",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 RuxitSynthetic/1.0 v8256685072510535690 t4837746627378653889 athe94ac249 altpriv cvcv=2 smf=0 svfu=1",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 RuxitSynthetic/1.0 v5053857487158656312 t7257912775283346076 ath5ee645e0 altpriv cvcv=2 smf=0 svfu=1",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 RuxitSynthetic/1.0 v3335015056 t6703941201591042144 athfa3c3975 altpub cvcv=2 smf=0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 RuxitSynthetic/1.0 v7758678051478134788 t4763100215355965436 ath259cea6f altpriv cvcv=2 smf=0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 RuxitSynthetic/1.0 v173982583758727822 t8360729428027585528 ath259cea6f altpriv cvcv=2 smf=0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 RuxitSynthetic/1.0 v3335017705 t6006063806750198674 athfa3c3975 altpub cvcv=2 smf=0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 RuxitSynthetic/1.0 v5595057010161675774 t5747064355914000718 ath259cea6f altpriv cvcv=2 smf=0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 RuxitSynthetic/1.0 v4786524870233058218 t8056460500199558789 ath5ee645e0 altpriv cvcv=2 smf=0 svfu=1"]
        self.headers={}
    
    def _get_data(self, url=None, params={}):
        self.headers = {
                "Accept": "*/*",
                "Content-Type" :"application/json",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": random.choice(self.user_agents), 
                'From': 'ak@domain.com'  # This is another valid field
                }
        counter = 0
        response = {}
        while counter <=5:
            response = requests.request("GET", url or self.base_api_url, params=params, headers=self.headers)

            if counter == 5:
                raise(NotImplementedError("Too many attempts"))

            if response.status_code == 200:
                break
            else:
                counter += 1
                print(f"Attempting request again {counter}")
                continue

        return response.json()

    def get_data(self,
                nobelPrizeYear,
                yearTo,
                limit, 
                offset):
        params = {"nobelPrizeYear":nobelPrizeYear,
                    "yearTo": yearTo,
                    "limit" : limit,
                    "offset": offset}
        return self._get_data(params=params)

if __name__ == "__main__":
    nb = NobelData()
    print(nb.get_data(1990, 2000))


