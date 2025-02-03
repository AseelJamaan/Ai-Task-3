import speech_recognition as sr
import openai
import pyttsx3
import os
import pocketsphinx


# الخطوة 1: تسجيل الصوت من المايك
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording... Please speak now!")
        try:
            # تسجيل الصوت
            recognizer.adjust_for_ambient_noise(source)  # تحسين الجودة
            audio = recognizer.listen(source, timeout=20)  # تسجيل حتى 10 ثوانٍ
            print("Recording complete.")
            # تحويل الصوت إلى نص
            text = recognizer.recognize_sphinx(audio)  # استخدام محرك Sphinx
            print(f"Transcribed Text: {text}")
            return text
        except sr.UnknownValueError:
            return "Error: Could not understand the audio."
        except sr.RequestError as e:
            return f"Error: Could not request results; {str(e)}"
        except Exception as e:
            return f"Error during recording: {str(e)}"

# الخطوة 2: إرسال النص إلى ChatGPT
def get_chatgpt_response(prompt):
    openai.api_key = "your api key"  # أدخلي مفتاح الـ API الخاص بك هنا
    try:
        # استخدام واجهة API الصحيحة
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # النموذج الذي تريد استخدامه
            prompt=prompt  # النص الذي سيتم إرساله إلى ChatGPT
        )
        return response['choices'][0]['text']  # استرجاع النص من الرد
    except Exception as e:
        return f"Error during ChatGPT response: {str(e)}"

# الخطوة 3: تحويل النص إلى صوت
def text_to_speech_and_play(text):
    try:
        # تحويل النص إلى صوت وحفظه كملف
        engine = pyttsx3.init()
        output_file = "response.mp3"
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        # تشغيل الصوت الناتج باستخدام مشغل الوسائط
        print("Playing the response...")
        os.system(f"start {output_file}")  # للويندوز
        # ملاحظة: إذا كنت على macOS، استخدم `open {output_file}`
        # وإذا كنت على Linux، استخدم `xdg-open {output_file}`
    except Exception as e:
        print(f"Error during text-to-speech: {str(e)}")

# الخطوة 4: تشغيل المهمة كاملة
def main():
    # تسجيل الصوت
    input_text = record_audio()
    if input_text.startswith("Error"):
        print(input_text)
        return

    # إرسال النص إلى ChatGPT
    print("Sending text to ChatGPT...")
    response_text = get_chatgpt_response(input_text)
    if response_text.startswith("Error"):
        print(response_text)
        return

    print(f"ChatGPT Response: {response_text}")

    # تحويل النص إلى صوت وتشغيله
    text_to_speech_and_play(response_text)

# تشغيل البرنامج
if __name__ == "__main__":
    main()
