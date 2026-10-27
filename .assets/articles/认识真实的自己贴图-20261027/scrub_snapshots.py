"""提交研究快照前移除验证页的网络地址与临时搜索校验参数。"""

from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clean(item) for item in value]
    if not isinstance(value, str):
        return value
    value = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[network-address-redacted]', value)
    value = re.sub(r'(?i)(token(?:=|%3D))[^&\s\"<>]+', r'\1[temporary-search-token-redacted]', value)
    return re.sub(r'(VerifyCode[:：]\s*)\w+', r'\1[redacted]', value)


if __name__ == '__main__':
    files = list((HERE / 'snapshots').glob('*.json'))
    for path in files:
        data = clean(json.loads(path.read_text()))
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'已清理{len(files)}份快照中的网络与临时校验信息')
