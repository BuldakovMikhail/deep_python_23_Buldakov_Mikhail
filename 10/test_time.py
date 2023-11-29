#! /usr/bin/env python3

import json
import ujson
import cjson
import unittest
from faker import Faker

import time


def test_time():
    N = 100000
    M = 10

    fake = Faker()

    dicts = []

    for _ in range(M):
        json_dict = {}
        for i in range(N):
            json_dict[fake.name()] = i

        dicts.append(json_dict)

    start_time = time.process_time()
    for d in dicts:
        res = cjson.dumps(d)
    end_time = time.process_time()

    print(f"Dumps time cjson: {(end_time - start_time) / M} (sec)")

    start_time = time.process_time()
    for d in dicts:
        res = ujson.dumps(d)
    end_time = time.process_time()

    print(f"Dumps time ujson: {(end_time - start_time) / M} (sec)")

    start_time = time.process_time()
    for d in dicts:
        res = json.dumps(d)
    end_time = time.process_time()

    print(f"Dumps time json: {(end_time - start_time) / M} (sec)")


    strs = []
    for d in dicts:
        strs.append(cjson.dumps(d))


    start_time = time.process_time()
    for d in strs:
        res = cjson.loads(d)
    end_time = time.process_time()

    print(f"Loads time cjson: {(end_time - start_time) / M} (sec)")

    start_time = time.process_time()
    for d in strs:
        res = ujson.loads(d)
    end_time = time.process_time()

    print(f"Loads time ujson: {(end_time - start_time) / M} (sec)")

    start_time = time.process_time()
    for d in strs:
        res = json.loads(d)
    end_time = time.process_time()

    print(f"Loads time json: {(end_time - start_time) / M} (sec)")

    
test_time()