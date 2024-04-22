#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:03:53 2024

@author: emre
"""
#!/Users/emre/opt/anaconda3/envs/SP/bin/python

import importlib
import subprocess

def check_and_install_libraries():
    required_libraries = ['pandas', 'asyncio', 'aiodns', 're', 'logging']
    missing_libraries = []
    
    for lib in required_libraries:
        try:
            importlib.import_module(lib)
        except ImportError:
            missing_libraries.append(lib)
    
    if missing_libraries:
        print("Installing missing libraries...")
        subprocess.run(["pip", "install"] + missing_libraries, check=True)
        print("Libraries installed successfully.")

    # Import modules after verifying installation
    global pd, asyncio, aiodns, re, logging
    import pandas as pd
    import asyncio
    import re
    import logging
    import aiodns
    
check_and_install_libraries()
EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

async def get_mx_records_async(domain):
    resolver = aiodns.DNSResolver()
    try:
        mx_records = await resolver.query(domain, 'MX')
        return [str(mx.host) for mx in mx_records] if mx_records else None
    except Exception as e:
        logging.error(f"Failed to retrieve MX records for {domain}: {e}")
        return None

async def email_verify(email):
    # Check for "u003" in the email address
    if "u003" in email:
        return False, "Email contains invalid characters."
    
    if not re.match(EMAIL_REGEX, email):
        return False, "Invalid email format."
    
    domain = email.split('@')[-1]
    mx_records = await get_mx_records_async(domain)
    if not mx_records:
        return False, "Domain has no MX records or does not exist."
    
    return True, "Domain has MX records."


async def verify_and_remove_invalid_emails(df):
    indices_to_drop = []
    for index, row in df.iterrows():
        email = row['Email']
        result, _ = await asyncio.ensure_future(email_verify(email))
        if not result:
            indices_to_drop.append(index)

    df = df.drop(indices_to_drop)  
    return df



