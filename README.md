# موقع الاستعلام عن نتيجة الثانوية العامة 2026

موقع بسيط مبني بـ Streamlit يتيح لأكثر من 919 ألف طالب وطالبة الاستعلام عن نتيجتهم
بإدخال رقم الجلوس فقط.

## محتويات المشروع

```
project/
├── app.py                  # كود الموقع (Streamlit)
├── data/
│   └── results.parquet     # قاعدة بيانات النتيجة (مضغوطة، ~13 ميجا بدلاً من 36 ميجا)
├── requirements.txt        # المكتبات المطلوبة
├── .streamlit/config.toml  # ألوان وإعدادات الموقع
└── README.md
```

تم تحويل ملف الإكسل الأصلي (36 ميجا) إلى ملف Parquet مضغوط (13 ميجا تقريباً) لأن:
- حجمه أصغر بكثير فيسهل رفعه على GitHub.
- تحميله في الذاكرة عند فتح الموقع أسرع بكثير من قراءة إكسل بـ 919,396 صف في كل مرة.
- عمود رقم الجلوس مُستخدم كفهرس (index) فيبحث فيه الموقع فوراً بدون أي إبطاء.

## خطوات الرفع على GitHub

1. أنشئ مستودع (repository) جديد على GitHub، مثلاً باسم `thanaweya-results-2026`.
2. ارفع كل الملفات الموجودة داخل مجلد `project` (بما فيها مجلد `data` والملف المخفي `.streamlit`) كما هي، بنفس الأسماء والمسارات.
   - تأكد أن حجم `data/results.parquet` أقل من حد GitHub (100 ميجا) — حجمه الحالي حوالي 13 ميجا فلا توجد مشكلة.
3. تأكد أن `requirements.txt` في جذر المستودع (نفس مكان `app.py`).

عبر الموقع مباشرة:
- ادخل إلى الريبو على GitHub → Add file → Upload files → اسحب كل الملفات وارفعها → Commit.

أو عبر Git من جهازك:
```bash
git init
git add .
git commit -m "نتيجة الثانوية العامة 2026"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

## خطوات النشر على Streamlit Community Cloud

1. ادخل على https://share.streamlit.io وسجل الدخول بحساب GitHub.
2. اضغط **New app**.
3. اختر المستودع الذي رفعته، والفرع `main`، وحدد **Main file path** = `app.py`.
4. اضغط **Deploy**. سيقوم Streamlit تلقائياً بتثبيت المكتبات من `requirements.txt` وتشغيل الموقع.
5. بعد دقيقة أو دقيقتين سيكون الموقع متاحاً على رابط بصيغة:
   `https://REPO_NAME-xxxxx.streamlit.app`

## اختبار الموقع محلياً قبل الرفع (اختياري)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ملاحظات مهمة

- **الخصوصية**: قاعدة البيانات تحتوي على أسماء حقيقية لطلاب حقيقيين. أي شخص يعرف رقم
  جلوس آخر يمكنه رؤية اسمه ونتيجته (تماماً كموقع نتيجة رسمي). إذا أردت طبقة حماية إضافية
  (مثل طلب جزء من الاسم أو الرقم القومي للتأكيد)، يجب توفير هذه البيانات في الملف الأصلي أولاً.
- **تحديث البيانات**: إذا تغيّر ملف الإكسل مستقبلاً، أعد فقط تشغيل سكربت التحويل الموجود في نهاية
  هذا الملف لإنشاء `results.parquet` جديد، ثم استبدل الملف القديم به وارفعه على GitHub.

### سكربت إعادة توليد ملف Parquet من إكسل جديد

```python
import pandas as pd

df = pd.read_excel("النتيجة_الجديدة.xlsx")
df["seating_no"] = df["seating_no"].astype("int32")
df["total_degree"] = df["total_degree"].astype("int16")
df["student_case_desc"] = df["student_case_desc"].astype("category")
df.to_parquet("data/results.parquet", compression="gzip", index=False)
```
