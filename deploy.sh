#!/bin/bash
tar -zcvf initio.tar.gz . --exclude .git
scp initio.tar.gz pi@jimi5:webiopi-test

