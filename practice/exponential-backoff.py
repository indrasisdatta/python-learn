# Implement an exponential backoff strategy that doubles the wait time between retries, starting from 1 second, but stops after 5 retries.

import time

waitTime = 1
retryCount = 0
maxRetryCount = 5

while retryCount < maxRetryCount:
    print('Retry count: ', retryCount+1, ' Wait time: ', waitTime)
    time.sleep(waitTime)
    retryCount += 1
    waitTime *= 2
    
    