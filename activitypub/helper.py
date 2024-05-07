# -*- encoding: utf-8 -*-
'''
helper.py
----
put some words here


@Time    :   2024/05/07 17:50:50
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import re
import hashlib
import base64
from urllib.parse import urlparse
from typing import Dict, Tuple, List
from httpsig import HeaderSigner, HeaderVerifier


def generate_digest(raw_body: str) -> Tuple[str, str]:
    sha256_digest_str = base64.b64encode(
        hashlib.sha256(raw_body.encode()).digest()).decode()
    return 'SHA-256', sha256_digest_str


def verify_digest(raw_body: str, received_digest: str) -> bool:
    _, b64_calculated_digest = generate_digest(raw_body)
    return received_digest == b64_calculated_digest


def generate_signature(url_path: str, key_id: str, secret: str, headers: dict, algorithm="rsa-sha256", method="POST") -> Dict[str, str]:
    headers_to_sign_with_body = [
        "(request-target)", "host", "date", "digest", "content-type"
    ]
    headers_to_sign_without_body = [
        "(request-target)", "host", "date", "content-type"
    ]
    signer = HeaderSigner(
        key_id=key_id,
        secret=secret,
        algorithm=algorithm,
        headers=headers_to_sign_with_body if 'digest' in headers else headers_to_sign_without_body,
        sign_header="Signature"
    )
    signed_headers = signer.sign(
        headers,
        method=method,
        path=url_path
    )
    return signed_headers


def verify_signature(url_path: str, secret: str, headers: dict, method: str = 'POST') -> bool:
    match = re.search(r'headers="([^"]+)"', headers.get('signature'))
    if match:
        headers_to_sign = match.group(1)
    else:
        return False
    verifier = HeaderVerifier(
        headers=headers,
        method=method,
        path=url_path,
        secret=secret,
        required_headers=headers_to_sign.split(' '),
        sign_header='Signature',
    )
    return verifier.verify()
