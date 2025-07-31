from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lexicon_loader

app = FastAPI()
templates = Jinja2Templates(directory="demo_web/templates")

# 挂载静态文件（TU/图片目录）
app.mount("/TU", StaticFiles(directory="TU"), name="tu")

LEXICON = lexicon_loader.load_lexicon()

def lookup_words_with_images(text):
    results = []
    for char in text:
        entries = lexicon_loader.lookup(char, LEXICON)
        if entries:
            entry = entries[0]
            img_names = entry.get('img_names', [])
            img_url = None
            for img_name in img_names:
                img_name = img_name.strip()
                if img_name and os.path.exists(os.path.join('TU', f"{img_name}.png")):
                    img_url = f"/TU/{img_name}.png"
                    break
            results.append({
                "char": char,
                "img_url": img_url,
                "explain": entry.get("explain", ""),
            })
        else:
            results.append({
                "char": char,
                "img_url": None,
                "explain": "[未找到]",
            })
    return results

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "input_text": "", "cards": []})

@app.post("/", response_class=HTMLResponse)
async def post_index(request: Request, input_text: str = Form(...)):
    cards = lookup_words_with_images(input_text)
    return templates.TemplateResponse("index.html", {"request": request, "input_text": input_text, "cards": cards})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True) 