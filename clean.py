#!/usr/bin/env python3 
import json
import sys
import re
#import ./filters
from urllib.parse import urlparse,parse_qs,unquote

pending_subscriptions={}
pending_disambiguations={}

unprocessed=[]


def put_subscription(domain,query_string):
    if domain in pending_subscriptions:
        pending_subscriptions[domain].append(query_string)
    else:
        pending_subscriptions[domain]=[query_string]

def do_filter(u):
    for (rule,action,param) in filters:
        r= re.match(rule,u)
        if r:
            return action(u,param,r)
        

def process_url(u):
    u=u.strip()
    new = do_filter(u)
    while True:
        if new == False:
            unprocessed.append(u)
            break
        if new == None:
            break
        u = new
        new = do_filter(u)
    
    
def unpause_url(u,param,match):
    o = urlparse(u)        
    f=o.fragment
    d=parse_qs(f)
    if "uri" in d:
        return d["uri"][0]
    elif "url" in d:
        return d["uri"][0]
    else:
        return False

def add_twitter_post(u,param,match):
    #diasambiguate whether you wnt the sub or the whole thing
    pass

def add_subscription(u,param,match):
    name=unquote(match.group(1))
    put_subscription(param,name)
    return None


filters=(
    (r"chrome-extension://[^/]+/suspended.*",unpause_url,None),
    #(r"http://twitter.com/[^/]+/status/[0-9]+",add_twitter_post,None),
    (r"https{0,1}://twitter.com/([^/]+)/{0,1}",add_subscription,"twitter.com"),

)

if __name__ == "__main__":
    if len(sys.argv)>1:
        with open(sys.argv[1]) as f:
            for l in f:
                process_url(l)
    else:
        print("Provide list ^D(EOF) when done")
        while True:
            try:
                input_ = input()
                process_url(input_)
            except EOFError:
                break #This is intended
    
    for k in pending_subscriptions:
        print(k)
        for u in pending_subscriptions[k]:
            print(u)
        print()
    print()
    print("###Unprocessable")
    for u in unprocessed:
        print(u)