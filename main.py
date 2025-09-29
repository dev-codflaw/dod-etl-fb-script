from runner import run_scraper
from config import THREADS, MAX_RUNS

if __name__ == "__main__":
    run_scraper(total_threads=THREADS, max_runs=MAX_RUNS)
