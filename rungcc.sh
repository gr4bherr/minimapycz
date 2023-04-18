#!/bin/bash

g++ main.cpp -o main.out -lpqxx -lpq -I/usr/include/python3.10 -lpython3.10 && ./main.out
