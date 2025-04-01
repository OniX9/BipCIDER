import os
import time
import random
import requests
from mnemonic import Mnemonic
from bip32utils import BIP32Key
from hashlib import sha256
from wordlist.wordslist_cache import bip32_words
from requests.auth import HTTPProxyAuth
from utils.proxies import proxies

class BitUtils:
    baseurl = "https://blockstream.info/api/address/"
    # Function to get single balance from Blockstream API
    def get_balance(self, address):
        url = url = f"{self.baseurl}{address}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get("chain_stats", {}).get("funded_txo_sum", 0) / 1e8  # Convert from satoshis to BTC
            else:
                print(f"Error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
    # # Function to get balances for a batch of addresses using a single API call
    # def get_balances_batch(self, addresses):
    #     url = f"{self.baseurl}batch"
    #     try:
    #         response = requests.post(url, json={"addresses": addresses})
    #         if response.status_code == 200:
    #             data = response.json()
    #             balances = {
    #                 address: (info.get("chain_stats", {}).get("funded_txo_sum", 0) / 1e8)  # Convert from satoshis to BTC
    #                 for address, info in data.items()
    #             }
    #             return balances
    #         else:
    #             print(f"Error: {response.status_code}")
    #             return None
    #     except requests.exceptions.RequestException as e:
    #         print(f"Request failed: {e}")
    #         return None

    # Alternative approach to prevent 429 using retries.
    def get_balance_with_retry(self, address:str):
        url = f"{self.baseurl}{address}"
        retries = 5
        backoff_factor = 1  # seconds

        for attempt in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("chain_stats", {}).get("funded_txo_sum", 0) / 1e8  # Convert from satoshis to BTC
                elif response.status_code == 429:
                    wait_time = backoff_factor * (2 ** attempt)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Press Ctrl+C to stop the process")
                    print(f"Rate limit hit. Retrying in {wait_time} seconds")
                    time.sleep(wait_time)
                else:
                    print(f"Error: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return None
            except KeyboardInterrupt:
                raise

        print("Max retries reached. Could not fetch balance.")
        return None


    # Alternative approach to prevent 429 using proxy rotation & retries.
    def get_balance_with_proxy(self, address:str, proxies:list):
        url = f"{self.baseurl}{address}"
        retries = 5
        backoff_factor = 1  # seconds

        for attempt in range(retries):
            try:
                # Randomly select a proxy with credentials
                selected_proxy = random.choice(proxies)
                proxy_host = selected_proxy["host"]
                proxy_port = selected_proxy["port"]
                proxy_user = selected_proxy["username"]
                proxy_pass = selected_proxy["password"]

                proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
                proxy_dict = {
                    "http": proxy_url,
                    "https": proxy_url,
                }

                # print(f"Using proxy: {proxy_host}:{proxy_port}")

                response = requests.get(url, proxies=proxy_dict, auth=HTTPProxyAuth(proxy_user, proxy_pass))

                if response.status_code == 200:
                    data = response.json()
                    return data.get("chain_stats", {}).get("funded_txo_sum", 0) / 1e8  # Convert from satoshis to BTC
                elif response.status_code == 429:
                    wait_time = backoff_factor * (2 ** attempt)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Press Ctrl+C to stop the process")
                    print(f"Rate limit hit. Retrying in {wait_time} seconds with a new proxy...")
                    time.sleep(wait_time)
                else:
                    print(f"Error: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return None

        print("Max retries reached. Missed an address.")
        return None


    # Function to check if seed phrase is active
    def check_btc_seed(self, phrase):
        mnemo = Mnemonic("english")
        seed = mnemo.to_seed(phrase)

        # Generate BIP32 master key
        master_key = BIP32Key.fromEntropy(seed[:32])

        # Derive first receiving address (m/44'/0'/0'/0/0)
        purpose = master_key.ChildKey(44 + 0x80000000)
        coin_type = purpose.ChildKey(0 + 0x80000000)
        account = coin_type.ChildKey(0 + 0x80000000)
        change = account.ChildKey(0)
        address_key = change.ChildKey(0)

        address = address_key.Address()
        balance = 0

        if len(proxies) > 0:
            balance = self.get_balance_with_proxy(address, proxies)
        else:
            balance = self.get_balance_with_retry(address)


        return address, balance
    
    def seed_phrase_listgen(self, wordslist_language = bip32_words):
        # Generate seed phrase using wordslist cache
        # Instantaneous but less functional
        selected_words = random.sample(wordslist_language, 12)
        phrase = " ".join(selected_words)
        return phrase

    def seed_phrase_txtgen(self):
        # Generate seed phrase using mnemonic library
        # Slower but more versatile
        mnemo = Mnemonic("english")
        result = mnemo.generate(strength=128)
        return result

