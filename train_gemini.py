import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import MarkdownTextSplitter
from langchain.docstore.document import Document
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import PyPDF2
import html2text
import re
from dotenv import load_dotenv
import os
import numpy as np


class Gemini:
    def __init__(self, gemini_api, website_url, training_data_dir) -> None:

        self.data: str = "" # store trainig text
        self.chat_history = []

        print('Gemini Configuration....')
        genai.configure(api_key=gemini_api)
        self.model = genai.GenerativeModel('gemini-pro')

        print('Text embedding....')
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        print('Loading knowledge base...')
        self.knowledge_base = self._load_knowledge_base(website_url, training_data_dir)


    def get_data_from_website(self, url):
        """
        Retrieve text content and metadata from a given URL.

        Args:
            url (str): The URL to fetch content from.

        Returns:
            tuple: A tuple containing the text content (str) and metadata (dict).
        """

        response = requests.get(url)
        if response.status_code == 500:
            print("Server error")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        html = str(soup)
        html2text_instance = html2text.HTML2Text()
        html2text_instance.images_to_alt = True
        html2text_instance.body_width = 0
        html2text_instance.single_line_break = True
        text = html2text_instance.handle(html)

        try:
            page_title = soup.title.string.strip()
        except:
            page_title = url.path[1:].replace("/", "-")

        meta_description = soup.find("meta", attrs={"name": "description"})
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})

        if meta_description:
            text += meta_description.get("content")
        else:
            text += page_title

        if meta_keywords:
            meta_keywords = meta_description.get("content")
        else:
            meta_keywords = ""

        #metadata = {'title': page_title,
        #            'url': url,
        #            'description': description,
        #            'keywords': meta_keywords}

        return text


    def _crawl_website(self, start_url) -> list:
        """ Extract all the urls in a website starting from 'start_url'"""
        urls = [start_url]
        visited_urls = set()

        while len(urls) != 0:
            current_url = urls.pop()
            
            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)
            
            try:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.content, "html.parser")

                link_elements = soup.select("a[href]")
                for link_element in link_elements:
                    url = link_element['href']
                    full_url = urljoin(current_url, url)  # Convert relative URLs to absolute URLs
                    
                    if full_url.startswith(start_url) and full_url not in visited_urls:
                        urls.append(full_url)
                        
            except requests.RequestException as e:
                print(f"Error accessing {current_url}: {e}")

        return visited_urls


    def _extract_text_from_pdf(self, pdf_path) -> str:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

        return text

   
    def _create_chunks(self, text: str):
        text_splitter = MarkdownTextSplitter(chunk_size=2048, chunk_overlap=128)
        chunks = text_splitter.split_text(text)
        
        return chunks


    def _clean_text(self, data: str) -> str:
        data = re.sub(r"(\w)-\n(\w)", r"\1\2", data)
        data = re.sub(r"(?<!\n)\n(?!\n)", " ", data)
        data = re.sub(r"\n{2,}", "\n", data)

        return data

    def _load_knowledge_base(self, website_url=None, training_data_dir=None):
        
        knowledge_base = {}

        if website_url:
            crawled_urls: list = self._crawl_website(website_url)
            for url in crawled_urls:
                self.data += self.get_data_from_website(url)
        
        if training_data_dir:
            for file_name in os.listdir(training_data_dir):
                file_path = os.path.join(training_data_dir, file_name)

                if file_name.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        self.data += text.replace('\n', ' ')
                elif file_name.endswith('.pdf'):
                    self.data += self._extract_text_from_pdf(file_path)
                else:
                    continue

                print(f'Processed {file_name}')

        self.data = self._clean_text(self.data)

        if self.data.strip():
            chunks = self._create_chunks(self.data)
            embeddings = self.embedding_model.encode(chunks)
            knowledge_base[file_name] = {
                'chunks': chunks,
                'embeddings': embeddings
                }
            print(f"{len(chunks)} chunks created")

        return knowledge_base
    

    def _find_relevant_context(self, query, top_k=4):
        relevant_chunks = []
        query_embedding = self.embedding_model.encode([query])[0]

        for doc in self.knowledge_base.values():
            similarities = np.dot(doc['embeddings'], query_embedding)
            top_indices = np.argsort(similarities)[-top_k:]

            for idx in top_indices:
                relevant_chunks.append(doc['chunks'][idx])
            
        return "\n".join(relevant_chunks)



    def get_response(self, query: str) -> str:
        context = self._find_relevant_context(query)

        prompt = f""" 
        Your prompt....
        """

        try:
            response = self.model.generate_content(prompt)
            response_txt = response.text.strip()
            response_txt = re.sub(r'\{\{response_start\}\}|\{\{response_end\}\}|Answer:', '', response_txt)
        except Exception as e:
            response_txt = f"Sorry, I couldn't process this request. Error: {str(e)}"

        self.chat_history.append({'question': query, 'answer': {response_txt}})

        return response_txt