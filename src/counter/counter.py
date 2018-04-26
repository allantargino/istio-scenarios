import asyncio
import subprocess
import random
import re
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        return response.status

async def run(n, base_ip):
    base_url = 'http://{}/frontend/add/{}/{}'
    tasks = []
    async with ClientSession() as session:
        for i in range(n):
            url = base_url.format(base_ip, random.randint(1, 100), random.randint(1, 100))
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)

if __name__ == '__main__':
    n = 100 # requests

    ingress_query = subprocess.run(['kubectl', 'get', 'ingress', '--field-selector=metadata.name=gatewaycalculator'], stdout=subprocess.PIPE)
    output = ingress_query.stdout.decode("utf-8") 
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)[0]

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(n, ip))
    loop.run_until_complete(future)
    result = future.result()

    count_len = len(result)
    count_200 = float(result.count(200)) / count_len * 100
    count_500 = float(result.count(500)) / count_len * 100
    count_other = 100 - count_500-count_200

    print('Successful responses:\t%f %%' % count_200)
    print('Error responses:\t%f %%' % count_500)
    print('Other responses:\t%f %%' % count_other)