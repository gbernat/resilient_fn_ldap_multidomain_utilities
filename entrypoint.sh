#!/bin/sh
APP_CONFIG_SHA=`sha256sum /etc/rescircuits/app.config`
resilient-circuits run & CIRCUITS_PID=`echo $!`
while true
do
if ! echo $APP_CONFIG_SHA | sha256sum --check
then
kill -9 $CIRCUITS_PID
break
fi
sleep 60
done