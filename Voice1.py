from aip import AipSpeech

# 配置你的百度云应用信息
APP_ID = '56826083'
API_KEY = 'pbUgUQoK1Jq9bndliLZNZ8jy'
SECRET_KEY = '1oRwsO6y7HE0y0tgkAmfzsUperpksy6p'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取音频文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()

file_path = 'D:\\360MoveData\\Users\\YWL\\Documents\\录音\\voice1.wav'  # 音频文件路径

# 调用百度云语音识别API
result = client.asr(get_file_content(file_path), 'wav', 16000, {
    'dev_pid': 1537,  # 普通话(支持简单的英文识别) 使用输入法模型。详见文档中“语种参数列表”
})

# 打印识别结果
if result['err_no'] == 0:
    print("识别结果:", result['result'][0])
else:
    print("识别失败，错误码：", result['err_no'])

