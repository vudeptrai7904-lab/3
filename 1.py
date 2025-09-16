import requests
import time
cookies = {
    'INGRESSCOOKIE': '1758035368.658.345.408257|9de6a539c14bab7f9073ed2b75abad44',
    'modal-session': 'se-kRGJEsMBsBwgskxfBmAYQk:xx-cynIw8iJVYrHoYeGk6lEpG',
    'modal-last-used-workspace': 'glenniepalmasodcs',
    'modal-last-used-environment#glenniepalmasodcs': 'main',
    'ajs_anonymous_id': '60c441bd-a39b-4132-b418-4064b9efa72a',
    'ajs_user_id': 'us-C37KImDy34fSKauGxg0rPB',
    'ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog': '%7B%22distinct_id%22%3A%22us-C37KImDy34fSKauGxg0rPB%22%2C%22%24sesid%22%3A%5B1758037838826%2C%2201995313-507e-7cdb-933b-3da00be05df3%22%2C1758035398781%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fapps%2Fglenniepalmasodcs%2Fmain%22%7D%7D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=26c808d7885a431d88872dd9585a8521,sentry-public_key=d75f7cb747cd4fe8ac03973ae3d39fec,sentry-trace_id=797d226bc5680d3ea5b7623366d7d60c,sentry-sample_rand=0.9629902395444863',
    'content-type': 'application/json',
    'origin': 'https://modal.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '797d226bc5680d3ea5b7623366d7d60c-a85fdd4ddc8a23a5',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'INGRESSCOOKIE=1758035368.658.345.408257|9de6a539c14bab7f9073ed2b75abad44; modal-session=se-kRGJEsMBsBwgskxfBmAYQk:xx-cynIw8iJVYrHoYeGk6lEpG; modal-last-used-workspace=glenniepalmasodcs; modal-last-used-environment#glenniepalmasodcs=main; ajs_anonymous_id=60c441bd-a39b-4132-b418-4064b9efa72a; ajs_user_id=us-C37KImDy34fSKauGxg0rPB; ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog=%7B%22distinct_id%22%3A%22us-C37KImDy34fSKauGxg0rPB%22%2C%22%24sesid%22%3A%5B1758037838826%2C%2201995313-507e-7cdb-933b-3da00be05df3%22%2C1758035398781%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fapps%2Fglenniepalmasodcs%2Fmain%22%7D%7D',
}

json_data = {
    'tutorial': 'get_started',
    'code': 'import modal\nimport asyncio\nimport tempfile\nimport subprocess\nimport os\nimport time\nimport random\nfrom typing import List\n\n# ---- Khởi tạo app ----\napp = modal.App("nodejs-workers")\n\n# ---- Build lightweight CPU image ----\nimage = (\n    modal.Image.debian_slim()\n    .apt_install("git", "curl", "gnupg", "nodejs")\n)\n\n# ---- Worker async, CPU=1, safe concurrency ----\n@app.function(\n    image=image,\n    cpu=1,                 # giữ 1 core\n    timeout=3600,\n    concurrency_limit=1    # chỉ 1 job Modal cùng lúc\n)\ndef run_tool_async_batch(cookies_list: List[str]):\n    """\n    This wrapper runs the asyncio loop inside the Modal function.\n    The real work is done by _async_main which uses asyncio subprocesses.\n    """\n    asyncio.run(_async_main(cookies_list))\n\nasync def _async_main(cookies_list: List[str]):\n    # số subprocess Node.js chạy đồng thời trong 1 worker\n    max_concurrent_subprocs = 2  # giữ nhỏ để tiết kiệm CPU\n    sem = asyncio.Semaphore(max_concurrent_subprocs)\n\n    # đảm bảo repo đã clone (synchronous safe)\n    if not os.path.exists("ha1"):\n        proc = await asyncio.create_subprocess_exec(\n            "git", "clone", "https://github.com/buiminhnhatfhacv-lang/ha1.git",\n            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE\n        )\n        await proc.communicate()\n\n    async def run_one(cookie: str, idx: int):\n        attempt = 0\n        while attempt < 3:\n            await sem.acquire()\n            try:\n                # tạo file cookie tạm bằng sync I/O (nhanh)\n                with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:\n                    f.write(cookie)\n                    cookie_path = f.name\n\n                # start node subprocess async\n                proc = await asyncio.create_subprocess_exec(\n                    "node", "app.js", "--cookies", cookie_path,\n                    cwd="ha1",\n                    stdout=asyncio.subprocess.PIPE,\n                    stderr=asyncio.subprocess.PIPE\n                )\n\n                try:\n                    # chờ kết thúc với timeout (ví dụ 10 phút)\n                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10*60)\n                    rc = proc.returncode\n                except asyncio.TimeoutError:\n                    # timeout -> kill và retry\n                    try:\n                        proc.kill()\n                    except Exception:\n                        pass\n                    rc = -1\n                    stdout, stderr = b"", b"Timeout"\n\n                # remove tempfile\n                try:\n                    os.unlink(cookie_path)\n                except Exception:\n                    pass\n\n                if rc == 0:\n                    print(f"[{idx}] OK")\n                    return True\n                else:\n                    attempt += 1\n                    backoff = min(20, 2 ** attempt + random.random())\n                    print(f"[{idx}] Fail rc={rc}. stderr={stderr[:200]!r}. Backoff {backoff:.1f}s (attempt {attempt})")\n                    await asyncio.sleep(backoff)\n            except Exception as e:\n                attempt += 1\n                backoff = min(20, 2 ** attempt + random.random())\n                print(f"[{idx}] Exception {e}. Backoff {backoff:.1f}s (attempt {attempt})")\n                await asyncio.sleep(backoff)\n            finally:\n                sem.release()\n\n        print(f"[{idx}] All retries failed.")\n        return False\n\n    # tạo tasks nhưng start chạy theo semaphore\n    tasks = [asyncio.create_task(run_one(cookie, i)) for i, cookie in enumerate(cookies_list)]\n\n    # chờ tất cả\n    results = await asyncio.gather(*tasks, return_exceptions=False)\n    print("Batch finished. Results:", results)\n\n# ---- Entry point ----\n@app.local_entrypoint()\ndef main():\n    # Thay cookies_list bằng dữ liệu thật của bạn\n    cookies_list = [\n        \'{"session":"se-111"}\',\n        \'{"session":"se-222"}\',\n        \'{"session":"se-333"}\',\n        \'{"session":"se-444"}\',\n        \'{"session":"se-555"}\',\n    ]\n\n    print("Starting async batch job (CPU=1).")\n    run_tool_async_batch.remote(cookies_list)\n',
    'modalEnvironment': 'main',
    'winsize': {
        'rows': 11,
        'cols': 57,
    },
}

response = requests.post(
    'https://modal.com/api/playground/glenniepalmasodcs/run',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"tutorial":"get_started","code":"import modal\\nimport asyncio\\nimport tempfile\\nimport subprocess\\nimport os\\nimport time\\nimport random\\nfrom typing import List\\n\\n# ---- Khởi tạo app ----\\napp = modal.App(\\"nodejs-workers\\")\\n\\n# ---- Build lightweight CPU image ----\\nimage = (\\n    modal.Image.debian_slim()\\n    .apt_install(\\"git\\", \\"curl\\", \\"gnupg\\", \\"nodejs\\")\\n)\\n\\n# ---- Worker async, CPU=1, safe concurrency ----\\n@app.function(\\n    image=image,\\n    cpu=1,                 # giữ 1 core\\n    timeout=3600,\\n    concurrency_limit=1    # chỉ 1 job Modal cùng lúc\\n)\\ndef run_tool_async_batch(cookies_list: List[str]):\\n    \\"\\"\\"\\n    This wrapper runs the asyncio loop inside the Modal function.\\n    The real work is done by _async_main which uses asyncio subprocesses.\\n    \\"\\"\\"\\n    asyncio.run(_async_main(cookies_list))\\n\\nasync def _async_main(cookies_list: List[str]):\\n    # số subprocess Node.js chạy đồng thời trong 1 worker\\n    max_concurrent_subprocs = 2  # giữ nhỏ để tiết kiệm CPU\\n    sem = asyncio.Semaphore(max_concurrent_subprocs)\\n\\n    # đảm bảo repo đã clone (synchronous safe)\\n    if not os.path.exists(\\"ha1\\"):\\n        proc = await asyncio.create_subprocess_exec(\\n            \\"git\\", \\"clone\\", \\"https://github.com/buiminhnhatfhacv-lang/ha1.git\\",\\n            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE\\n        )\\n        await proc.communicate()\\n\\n    async def run_one(cookie: str, idx: int):\\n        attempt = 0\\n        while attempt < 3:\\n            await sem.acquire()\\n            try:\\n                # tạo file cookie tạm bằng sync I/O (nhanh)\\n                with tempfile.NamedTemporaryFile(\\"w\\", delete=False, suffix=\\".json\\") as f:\\n                    f.write(cookie)\\n                    cookie_path = f.name\\n\\n                # start node subprocess async\\n                proc = await asyncio.create_subprocess_exec(\\n                    \\"node\\", \\"app.js\\", \\"--cookies\\", cookie_path,\\n                    cwd=\\"ha1\\",\\n                    stdout=asyncio.subprocess.PIPE,\\n                    stderr=asyncio.subprocess.PIPE\\n                )\\n\\n                try:\\n                    # chờ kết thúc với timeout (ví dụ 10 phút)\\n                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10*60)\\n                    rc = proc.returncode\\n                except asyncio.TimeoutError:\\n                    # timeout -> kill và retry\\n                    try:\\n                        proc.kill()\\n                    except Exception:\\n                        pass\\n                    rc = -1\\n                    stdout, stderr = b\\"\\", b\\"Timeout\\"\\n\\n                # remove tempfile\\n                try:\\n                    os.unlink(cookie_path)\\n                except Exception:\\n                    pass\\n\\n                if rc == 0:\\n                    print(f\\"[{idx}] OK\\")\\n                    return True\\n                else:\\n                    attempt += 1\\n                    backoff = min(20, 2 ** attempt + random.random())\\n                    print(f\\"[{idx}] Fail rc={rc}. stderr={stderr[:200]!r}. Backoff {backoff:.1f}s (attempt {attempt})\\")\\n                    await asyncio.sleep(backoff)\\n            except Exception as e:\\n                attempt += 1\\n                backoff = min(20, 2 ** attempt + random.random())\\n                print(f\\"[{idx}] Exception {e}. Backoff {backoff:.1f}s (attempt {attempt})\\")\\n                await asyncio.sleep(backoff)\\n            finally:\\n                sem.release()\\n\\n        print(f\\"[{idx}] All retries failed.\\")\\n        return False\\n\\n    # tạo tasks nhưng start chạy theo semaphore\\n    tasks = [asyncio.create_task(run_one(cookie, i)) for i, cookie in enumerate(cookies_list)]\\n\\n    # chờ tất cả\\n    results = await asyncio.gather(*tasks, return_exceptions=False)\\n    print(\\"Batch finished. Results:\\", results)\\n\\n# ---- Entry point ----\\n@app.local_entrypoint()\\ndef main():\\n    # Thay cookies_list bằng dữ liệu thật của bạn\\n    cookies_list = [\\n        \'{\\"session\\":\\"se-111\\"}\',\\n        \'{\\"session\\":\\"se-222\\"}\',\\n        \'{\\"session\\":\\"se-333\\"}\',\\n        \'{\\"session\\":\\"se-444\\"}\',\\n        \'{\\"session\\":\\"se-555\\"}\',\\n    ]\\n\\n    print(\\"Starting async batch job (CPU=1).\\")\\n    run_tool_async_batch.remote(cookies_list)\\n","modalEnvironment":"main","winsize":{"rows":11,"cols":57}}'.encode()
#response = requests.post('https://modal.com/api/playground/glenniepalmasodcs/run', cookies=cookies, headers=headers, data=data)
url = 'https://modal.com/api/playground/glenniepalmasodcs/run'
delay = 3  

def main():
    while True:
        try:
            resp = requests.post(
                url,
                cookies=cookies,
                headers=headers,
                json=json_data,
                timeout=10  
            )
            print(f"Đã tạo worker thành công | Status: {resp.status_code}")
        except requests.exceptions.Timeout:
            print("Request bị timeout, thử lại sau...")
        except Exception as e:
            print(f"Tạo worker với lỗi: {e}")

        for i in range(delay, 0, -1):
            print(f"Đợi {i} giây...", end="\r", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    main()




