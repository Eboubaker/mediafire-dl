#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import os.path as osp
import re
import shutil
import sys
import tempfile
import six
import tqdm
import requests
import sys

CHUNK_SIZE = 512 * 1024  # 512KB

def extractDownloadLink(url):
    user_agent = None
    try:
        from seleniumbase import SB
        from seleniumbase.config import settings
        settings.HIDE_DRIVER_DOWNLOADS = True

        with SB(uc=True, incognito=True, locale="en", ad_block=True, ) as sb:
            user_agent = sb.get_user_agent()
            sb.uc_open_with_reconnect(url, 4)
            sb.uc_gui_click_captcha()
            download_link = sb.find_element("css selector", "a[href^='https://download']")
            link = download_link.get_attribute("href")
            return link

    except Exception as e:
        print(f"ERROR: {e}, user agent: {user_agent}", file=sys.stderr,)
        sys.exit(1)

def download(url, output=None, quiet=False):
    url_origin = url

    # Need to redirect with confiramtion
    url = extractDownloadLink(url)

    if url is None:
        print('Permission denied: %s' % url_origin, file=sys.stderr)
        print(
            "Maybe you need to change permission over "
            "'Anyone with the link'?",
            file=sys.stderr,
        )
        return
    
    res = requests.get(url, allow_redirects=False, stream=True)

    if output is None:
        m = re.search(
            'filename="(.*)"', res.headers['Content-Disposition']
        )
        output = m.groups()[0]
        output = output.encode('iso8859').decode('utf-8')
        # output = osp.basename(url)

    output_is_path = isinstance(output, six.string_types)

    if not quiet:
        print('Downloading...', file=sys.stderr)
        print('From:', url_origin, file=sys.stderr)
        print(
            'To:',
            osp.abspath(output) if output_is_path else output,
            file=sys.stderr,
        )

    if output_is_path:
        tmp_file = tempfile.mktemp(
            suffix=tempfile.template,
            prefix=osp.basename(output),
            dir=osp.dirname(output),
        )
        f = open(tmp_file, 'wb')
    else:
        tmp_file = None
        f = output

    try:
        total = res.headers.get('Content-Length')
        if total is not None:
            total = int(total)
        if not quiet:
            pbar = tqdm.tqdm(total=total, unit='B', unit_scale=True)
        for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            if not quiet:
                pbar.update(len(chunk))
        if not quiet:
            pbar.close()
        if tmp_file:
            f.close()
            shutil.move(tmp_file, output)
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        try:
            if tmp_file:
                os.remove(tmp_file)
        except OSError:
            pass
    return output


def main():
    desc = 'Simple command-line script to download files from mediafire, it uses Seleniumbase to bypass cf challange'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('url', nargs='+')
    parser.add_argument('-o', '--output', help='output filename')
    args = parser.parse_args()

    if len(args.url) == 1 and args.output:
        download(args.url[0], args.output, quiet=False)
    else:
        for url in args.url:
            download(url, output=None, quiet=False)

if __name__ == "__main__":
    main()
