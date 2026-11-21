function updateDateTime() {
    const now = new Date();
    
    // --- 1. يوم الأسبوع ---
    const dayIndex = now.getDay();
    const arabicWeekdays = {
        0: "الأَحَدُ",
        1: "الإِثْنَيْنُ",
        2: "الثُّلَاثَاءُ",
        3: "الأَرْبِعَاءُ",
        4: "الخَمِيسُ",
        5: "الجُمُعَةُ",
        6: "السَّبْتُ"
    };
    
    // --- 2. الوقت ---
    const hours = String(now.getHours()).padStart(2, '0')
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const timeString = `${hours}:${minutes}`;
    
    // --- 3. التاريخ والشهر والسنة (منفصلة) ---
    const dayOfMonth = String(now.getDate()).padStart(2, '0');
    const monthIndex = now.getMonth();
    const year = now.getFullYear();
    
    const arabicMonths = {
        0: "جَانفِي",
        1: "فِيفري",
        2: "مَارس",
        3: "أَفريل",
        4: "مَاي",
        5: "جُوَان",
        6: "جُوِيلِيَة",
        7: "أُوت",
        8: "سِبتمبر",
        9: "أُكتُوبَر",
        10: "نُوفَمْبَر",
        11: "دِيسَمْبَر"
    };
    
    const dateString = `${dayOfMonth} ${arabicMonths[monthIndex]}`;
    const yearString = `${year}`;
    
    // --- 4. تحديث عناصر HTML بأمان ---
    const weekdayElement = document.getElementById('weekday_span');
    const timeElement = document.getElementById('time_span');
    const dateElement = document.getElementById('date_span');
    const yearElement = document.getElementById('year_span');
    
    if (weekdayElement && timeElement && dateElement && yearElement) {
        weekdayElement.textContent = arabicWeekdays[dayIndex];
        timeElement.textContent = timeString;
        dateElement.textContent = dateString;
        yearElement.textContent = yearString;
    }
}

// التشغيل الفوري والتحديث كل دقيقة
updateDateTime();
setInterval(updateDateTime, 60000);
