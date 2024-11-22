def add_kv(query: str, sep: str, **kv) -> str:
    return query + sep.join([i+"=?" for i in kv.keys()])
