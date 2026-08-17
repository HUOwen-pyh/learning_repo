"""MiniPL 带半开 span 的 lexer。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Tok: kind:str; text:str; start:int; end:int

def lex(src):
    out=[]; i=0
    while i<len(src):
        if src[i].isspace(): i+=1; continue
        start=i
        if src[i].isalpha():
            i+=1
            while i<len(src) and src[i].isalnum():i+=1
            text=src[start:i]; out.append(Tok("LET" if text=="let" else "ID",text,start,i))
        elif src[i].isdigit():
            i+=1
            while i<len(src) and src[i].isdigit():i+=1
            out.append(Tok("INT",src[start:i],start,i))
        elif src.startswith("==",i): i+=2; out.append(Tok("EQEQ","==",start,i))
        elif src[i] in "=+()": i+=1; out.append(Tok(src[start:i],src[start:i],start,i))
        else: raise SyntaxError(f"illegal {src[i]!r} at {i}")
    out.append(Tok("EOF","",len(src),len(src))); return out

def main() -> None:
    ts=lex("let x=12+3")
    assert [t.kind for t in ts]==["LET","ID","=","INT","+","INT","EOF"]
    assert ts[2].start==5 and lex("x==1")[1].kind=="EQEQ"
    try:lex("x@1")
    except SyntaxError as e: assert "1" in str(e)
    else:raise AssertionError
    print(ts)

if __name__ == "__main__":main()

# 动手改造：加入注释和字符串 token，并为未闭合字符串保留起始位置。
