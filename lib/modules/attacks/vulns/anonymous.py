import socket
import subprocess
from urllib.parse import urlparse

from lib.utils.container import Services
from .. import AttackPlugin


class Anonymous(AttackPlugin):
    def process(self, start_url, crawled_urls):
        output = Services.get('output')

        output.test('Scanning anonymous cipher vuln...')
        ip = ''
        port = '443'
        try:
            ip += socket.gethostbyname(urlparse(start_url).hostname)
            socket.inet_aton(ip)
            r = subprocess.Popen(
                ['timeout', '4', 'openssl', 's_client', '-connect', ip + ":" + str(port), "-cipher", "aNULL"],
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE).communicate()[0]
            if 'handshake failure' not in r:
                output.finding('That site is vulnerable to Anonymous Cipher, CVE-2007-1858.')
        except Exception as e:
            print(e)
