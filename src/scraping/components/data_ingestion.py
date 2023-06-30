import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup

import urllib.request as request
from dataclasses import dataclass
from pathlib import Path
import time

from src.utils.common import get_size
from zipfile import ZipFile
from src import logger
from src.exception import CustomException

from src.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):

        """
        :param data_ingestion_config: Configuration for data ingestion
        """
        self.config=config
      
    def file_download(self):
        if not os.path.exists(self.config.destination_folder):
            filename,headers=request.get(
                url=self.config.source_URL,
                filename=self.config.local_data_file
                                         ) 
        
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.destination_folderle))}") 
        
    def request_url(self):
        """
        
        # note the braces at the end
        base_url = 'https://cschedule=1A&changes=0&page={}'
        for page_num in range(1, 100):
            url = base_url.format(page_num)
            page = requests.get(url)  # use `url` here, not `base_url`
            ...  # rest of your code"
        """
        
        for i in range(1,50):
            url=f"https://books.toscrape.com/catalogue/category/books_1/page-{i}.html"
            r= requests.get()
            time.sleep(2)
            soup = BeautifulSoup(r.text, 'html.parser')

        return soup.find_all('article', class_='product_pod')
    def parse(self,articles):
    
        for item in articles:
            
            image = item.find('img')
            title = image.attrs['alt']
            starTag =item.find('p')
            star = starTag['class'][1]
            price = item.find('p', class_='price_color').text
            price = float(price[2:])
            article={'Title':title,'Price': price,'Star Rating':star}
            
            self.config.local_data_file.append(article)
    def output(self):
        """Read data as dataframe
        
        Keyword arguments:
        argument -- use pandas library
        Return: csv format
        """
        try:
       
            df = pd.DataFrame( os.makedirs(os.path.dirname(self.config.local_data_file),exist_ok=True))
            df.to_csv(self.config.output_folder,index=False,header=True)
            return (self.config.output_folder)
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionConfig:

        """
        Method Name :   initiate_data_ingestion
        Description :   This function initiates a data ingestion steps
        Output      :   Returns data ingestion artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        logger.info("Entered the initiate_data_ingestion method of Data ingestion class")
        try:
            
            logger.info("Fetched the data from url")
            self.request_url()

            logger.info("parse the beautifulsoup")
            self.parse()

            logger.info("Exited the initiate_data_ingestion method of Data ingestion class")
            self.output()


        except Exception as e:
            raise CustomException(e, sys) from e
        
        
if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()