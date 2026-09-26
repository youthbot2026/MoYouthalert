import os
import time
import requests
from bs4 import BeautifulSoup

# قراءة البيانات بأمان من خادم جيتهاب المخفي
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
# الرابط المباشر لصفحة رحلات اعرف بلدك
URL_TO_MONITOR = "https://apps.emys.gov.eg/youth/trip_public"

def send_telegram_message(message):
    """دالة لإرسال التنبيه الفوري لهاتفك عبر تيليجرام"""
    telegram_url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(telegram_url, json=payload)
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")

def monitor_youth_trips():
    print("🚀 بدء مراقبة صفحة رحلات اعرف بلدك بنجاح...")
    
    # رأس الطلب لتبدو المراقبة وكأنها متصفح حقيقي لتجنب حظر السيرفر
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
    }

    # النص الحالي الذي نبحث عن اختفائه أو تغيره
    no_trips_text = "لا توجد رحلات متاحة للحجز حالياً"

    while True:
        try:
            # إرسال طلب للموقع لجلب الصفحة
            response = requests.get(URL_TO_MONITOR, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # قراءة محتوى الصفحة
                soup = BeautifulSoup(response.content, 'html.parser')
                page_text = soup.get_text()
                
                # التحقق مما إذا كانت جملة "لا توجد رحلات" غير موجودة في الصفحة
                if no_trips_text not in page_text:
                    print("🚨🚨 بشرى سارة! حدث تغيير في الصفحة وتم فتح الحجز!")
                    
                    # نص الرسالة التي ستصلك على هاتفك
                    message = (
                        "🚨 **تنبيه هام جداً: رحلات اعرف بلدك!**\n\n"
                        "🔥 يبدو أنه تم فتح باب الحجز لرحلات جديدة الآن أو حدث تعديل في الصفحة!\n\n"
                        f"🔗 [اضغط هنا للدخول والحجز فوراً]({URL_TO_MONITOR})"
                    )
                    send_telegram_message(message)
                    
                    # لمنع إرسال آلاف الرسائل المكررة بعد فتح الحجز، سينتظر السكريبت نصف ساعة قبل الفحص التالي إذا فتح الحجز
                    time.sleep(60) 
                else:
                    print("⏳ تم الفحص: لا تزال الرسالة (لا توجد رحلات متاحة) موجودة. الموقع مستقر.")
            else:
                print(f"⚠️ فشل الاتصال بالموقع، كود الاستجابة من السيرفر: {response.status_code}")
                
        except Exception as e:
            print(f"❌ حدث خطأ غير متوقع أثناء الفحص: {e}")
            
        # انتظر 60 ثانية (دقيقة واحدة) قبل الفحص التالي
        # يمكنك تقليلها إلى 30 ثانية إذا كنت تريد سرعة أكبر، ولكن دقيقة ممتازة لتجنب الحظر
        time.sleep(60)

if __name__ == "__main__":
    monitor_youth_trips()
