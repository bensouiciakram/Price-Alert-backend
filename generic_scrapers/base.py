from re import sub 
from abc import abstractmethod
from parsel import Selector

class BaseExtractor():
    def __init__(self, url, price_xpath, title_xpath, image_xpath,
                 price_cleanup=None, title_cleanup=None, image_cleanup=None, **kwargs):
        self.url = url
        self.price_xpath = price_xpath
        self.title_xpath = title_xpath
        self.image_xpath = image_xpath
        self.price_cleanup = price_cleanup
        self.title_cleanup = title_cleanup
        self.image_cleanup = image_cleanup

    def apply_cleanup(self,text:str,cleanup:str) -> str:
        return sub(cleanup,'',text)

    def clean_price(self,price:str) -> float:
        cleaned_price = self.apply_cleanup(price,self.price_cleanup)
        return float(cleaned_price)

    def clean_title(self,title:str) -> str:
        return self.apply_cleanup(title,self.title_cleanup)
    
    def clean_image(self,image:str) -> str:
        return self.apply_cleanup(image,self.image_cleanup)

    def scrape_product_metadata(self) -> dict:
        response = self.get_response()
        price = response.xpath(self.price_xpath).get()
        title = response.xpath(self.title_xpath).get()
        image = response.xpath(self.image_xpath).get()
        product_metadata ={
            'price':self.clean_price(price),
            'title':self.clean_title(title),
            'image':self.clean_image(image)
        }
        print(f'Data successfully extracted : \n',product_metadata)
        return product_metadata

    @abstractmethod 
    def get_response(self) -> Selector :
        print(f'Visiting {self.url}')
        pass 