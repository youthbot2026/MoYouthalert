import os
import requests
from bs4 import BeautifulSoup

# قراءة البيانات بأمان من خادم جيتهاب المخفي
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# الرابط المباشر لصفحة رحلات اعرف بلدك
URL_TO_MONITOR = "https://apps.emys.gov.eg/youth/trip_public"

def send_telegram_message(message):
    """دالة لإرسال التنبيه الفوري لهاتفك عبر تيليجرام"""
    # تعديل الرابط ليكون صحيحاً وموجهاً للسيرفر الرسمي للتيليجرام
    telegram_url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            print("✅ تم إرسال رسالة التنبيه الفوري إلى تيليجرام بنجاح!")
        else:
            print(f"⚠️ فشل إرسال الرسالة، رد سيرفر تليجرام: {response.text}")
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")

def monitor_youth_trips():
    print("🚀 بدء فحص صفحة رحلات اعرف بلدك الحالية...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
    }

    no_trips_text = "لا توجد رحلات متاحة للحجز حالياً"

    try:
        # إرسال طلب للموقع لجلب الصفحة
        response = requests.get(URL_TO_MONITOR, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            
            # التحقق مما إذا كانت جملة "لا توجد رحلات" غير موجودة في الصفحة
            if no_trips_text not in page_text:
                print("🚨🚨 بشرى سارة! حدث تغيير في الصفحة وتم فتح الحجز!")
                message = (
                    "🚨 **تنبيه هام جداً: رحلات اعرف بلدك!**\n\n"
                    "🔥 يبدو أنه تم فتح باب الحجز لرحلات جديدة الآن أو حدث تعديل في الصفحة!\n\n"
                    f"🔗 [اضغط هنا للدخول والحجز فوراً]({URL_TO_MONITOR})"
                )
                send_telegram_message(message)
            else:
                print("⏳ تم الفحص بنجاح: لا تزال الرسالة موجودة والموقع مستقر. لا توجد رحلات جديدة حالياً.")
        else:
            print(f"⚠️ فشل الاتصال بالموقع، كود الاستجابة من السيرفر: {response.status_code}")
            
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع أثناء الفحص: {e}")

if __name__ == "__main__":
    monitor_youth_trips()
