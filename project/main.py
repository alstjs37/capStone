from flask import Flask, request, render_template
from _kafka.web_producer import Producer

app = Flask(__name__)
producer = Producer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # 사용자로부터 입력 받은 값
    user_input = request.form['number']

    # 입력 받은 값이 정수인지 확인
    try:
        user_input_int = int(user_input)
        result_message = f'입력된 정수값: {user_input_int}'
    except ValueError:
        result_message = '올바른 정수값을 입력하세요.'
    else:
        producer.publish_to_kafka(user_input_int)

    return render_template('result.html', message=result_message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)