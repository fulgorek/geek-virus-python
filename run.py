#!/usr/bin/python

from joblib import Parallel, delayed
import requests
import json

## Configuration
email = 'johnDoe@gmail.com'

# Number of processes to run in parallel = #cores.
jobs  = 1

### --------------------------------- ###
base_url       = 'https://9zld4zwegj.execute-api.us-east-1.amazonaws.com/dev'
challenge_url  = base_url + '/challenge/start'
challenge_post = base_url + '/challenge/submission'


def post(url, data):
  return requests.post(url, data=data).text

def get(url):
  return requests.get(url).text

def is_infected(patient):
  dna = {}
  for p in patient:
    if p in dna:
      dna[p] += 1
    else:
      dna[p] = 1
  dna = sorted(dna.items(), key=lambda x:x[1])
  return dna[4][0] == 'T' and (dna[4][1] != dna[3][1])

data = json.loads(post(challenge_url, json.dumps({ "email" : email })))
id   = data['populationId']

population =  data['population']
def cb(patient):
  return is_infected(get(patient))

infections = Parallel(n_jobs=jobs, verbose=5, backend="multiprocessing")(delayed(cb)(p) for p in population)
s = int(sum(infections) * 100 / len(population))

print post(challenge_post, json.dumps({ "populationId": id, "sicknessPercentage": s }))
