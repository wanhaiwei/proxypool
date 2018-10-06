from multiprocessing import Process
from spiders.crawler import check, crawl_ip
from api import run


def proxypool_run():

    check_process = Process(target=check)
    crawl_process = Process(target=crawl_ip)
    run_process = Process(target=run)

    check_process.start()
    crawl_process.start()
    run_process.start()

    check_process.join()
    crawl_process.join()
    run_process.join()


if __name__ == '__main__':
    proxypool_run()
