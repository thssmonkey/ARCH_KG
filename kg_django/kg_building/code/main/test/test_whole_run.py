import os, sys
import time
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import buildSpecFromRawText, extract_main, filter, filter_repeat, renew_spec
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))
from neo4jGraph import write2neo4j

def run_whole_process():
    print("Start whole_run...")
    time_start = time.time()
    buildSpecFromRawText.main_run()
    print('[buildSpecFromRawText] time cost: ', time.time() - time_start, ' s')
    extract_main.main_run()
    print('[extract_main] time cost: ', time.time() - time_start, ' s')
    filter.main_run()
    print('[filter] time cost: ', time.time() - time_start, ' s')
    filter_repeat.main_run()
    print('[filter_repeat] time cost: ', time.time() - time_start, ' s')
    renew_spec.main_run()
    print('[renew_spec] time cost: ', time.time() - time_start, ' s')
    write2neo4j.main_run()
    print('[write2neo4j] time cost: ', time.time() - time_start, ' s')
    print("whole_run Ending...")

run_whole_process()
