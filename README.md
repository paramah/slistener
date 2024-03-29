# Supervisord simple event listener

### Configuration

Environment variables:

- **EVENT** (required) supervisord event name
- **PROCESSNAME** (required) process name
- **DELAY** (required) delay in seconds
- **EXECUTE** (required) command to execute

supervisord configuration example:

```
[program:php-fpm]
command=/usr/sbin/php-fpm7.2 -R -F
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
redirect_stderr=true


[eventlistener:php-fpm-listener]
command=<path_to>/listener.py
numprocs=1
events=PROCESS_STATE_STARTING
autorestart=true
stderr_logfile=errorlogfile
stdout_logfile=applogfile
environment=DEBUG="true",EVENT="PROCESS_STATE_STARTING",PROCESSNAME="php-fpm",DELAY="2","EXECUTE"="/bin/echo testing"
```
