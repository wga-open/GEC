from flask import Flask, render_template, request

app = Flask(__name__)

# mock 转换函数
def convert_text(text):
    # 这里可以接入你的实际转换逻辑
    # 目前只是简单地在每个字前加上“图”字
    return ' '.join(['图' for _ in text if _ != ',']) + ' ' + text

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    input_text = ''
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        result = convert_text(input_text)
    return render_template('index.html', input_text=input_text, result=result)

if __name__ == '__main__':
    app.run(debug=True) 