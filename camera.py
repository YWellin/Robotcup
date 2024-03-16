import cv2
import pyaudio
import wave
import threading

class Robot:
    def __init__(self):
        """
        初始化Robot类。
        """
        self.camera_on = False  # 用于控制摄像头开关
        self.microphone_on = False  # 用于控制麦克风开关

    def start_camera(self):
        """
        启动摄像头并显示视频流。
        """
        self.camera_on = True
        cap = cv2.VideoCapture(0)  # 0代表电脑的默认摄像头
        if not cap.isOpened():
            print("Cannot open camera")
            return
        
        while self.camera_on:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame. Exiting ...")
                break
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) == ord('q'):  # 按'q'键退出
                break
        
        cap.release()
        cv2.destroyAllWindows()

    def start_recording(self, filename="recording.wav", duration=5):
        """
        使用麦克风进行录音，并保存为wav文件。
        """
        self.microphone_on = True
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=2,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
        
        frames = []
        for _ in range(0, int(44100 / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))
        
        self.microphone_on = False

    def activate(self):
        """
        同时启动摄像头和录音功能。
        """
        camera_thread = threading.Thread(target=self.start_camera)
        recording_thread = threading.Thread(target=self.start_recording)
        
        camera_thread.start()
        recording_thread.start()
        
        camera_thread.join()
        recording_thread.join()

# 使用示例
robot = Robot()
# 启动robot的摄像头和录音功能
robot.activate()
