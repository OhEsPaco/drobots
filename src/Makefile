#!/usr/bin/make -f
# -*- mode:makefile -*-

start-grid: /tmp/db/registry /tmp/db/nodoUno /tmp/db/nodoDos /tmp/db/nodoTres /tmp/db/nodoCuatro
	icegridnode --Ice.Config=nodoUno.config &
	while ! netstat -lptn 2> /dev/null | grep ":4061"; do sleep 1; done
	icegridnode --Ice.Config=nodoDos.config &
	icegridnode	--Ice.Config=nodoTres.config &
	icegridnode --Ice.Config=nodoCuatro.config &
	icegridadmin --Ice.Config=locator.config -uuser -ppass -e "application add 'application.xml'"&
	icegridadmin --Ice.Config=locator.config -uuser -ppass -e "application update 'application.xml'"

stop-grid:
	for node in nodoDos nodoTres nodoCuatro nodoUno; do \
	    icegridadmin --Ice.Config=locator.config -uuser -ppass -e "node shutdown $$node"; \
	done
	killall icegridnode

/tmp/db/%:
	mkdir -p $@

clean: stop-grid
	rm *~
	rm -r /tmp/db
