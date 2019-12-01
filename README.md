## Web-Monitor - website availability & performance monitoring

#### Overview:
Web-monitor is an application for monitoring availability & performance of given (by user) websites.  
Application requests websites for availability with corresponding check intervals and compute metrics over three timeframes: 2 minutes, 10 minutes and 1 hours.


Availability & performance metrics provided by application:
* Average/maximum time response
* Website availability
* HTTP status code count (2xx, 4xx, 5xx)

Additionally, program has an alerting module that can notify user if availability is below 80% for the past 2 minutes.
#### Configuration and how to run:
**Configuration**

The configuration is stored in `config.json` file. Initial schema is stored as an example in file.  
You can add new website by specifying website URL (as string) and interval check (as time in seconds).
   
**Running the application**

After proper configuration you are able to run the program.   
Initially, you have to create virtual env using your favourite tool (pyenv, virtualenv, etc.) or just use base interpreter.
After that you are able to install requirements (only `reqeusts` library) and run app:
```
$> pip install -r requirements.txt
$> python web_monitor.py
```
Lastly, use -h for help.
```
$> python web_monitor.py -h
```


 
#### Possible improvements/different approaches:
* Aggregate metrics for memory and computation optimization
    * Use information from previous metric snapshot to compute current one
* Write tests for all modules not only for alerting one
* Create more metrics
    * request size
    * packet loss
    * SSL certificate expiration
* Possibility to input configuration from command line
* Configurable timeframes, refresh rate and metrics per website
* Logging to file ()
 
#### Notes:
Code tested on Python 3.8.0