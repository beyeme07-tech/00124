"""
Futbol İçerik Üretici
- RSS feedlerden güncel haberler çeker
- Claude API ile 3 farklı içerik türü üretir
- Sonuçları icerikler.md dosyasına yazar
"""

import feedparser
import anthropic
import json
import os
from datetime import datetime

# ── Ayarlar ──────────────────────────────────────────────
RSS_FEEDS = [
    "https://www.goal.com/feeds/tr/news",           # Goal.com Türkçe
    "https://feeds.bbci.co.uk/sport/football/rss.xml",  # BBC Sport
    "https://www.transfermarkt.com.tr/rss/news",    # Transfermarkt
]

PAYLASIM_SAATLERI = ["09:00", "14:00", "20:00"]  # Kaç saatte bir üretileceğini belirler

ICERIK_TURLERI = [
    {
        "ad": "Haber Özeti",
        "emoji": "📰",
        "prompt": """Sen bir futbol içerik uzmanısın. Aşağıdaki futbol haberini Instagram ve Twitter için uygun, 
        akıcı Türkçe ile özetle. Dikkat çekici bir başlık yaz, ardından 3-4 cümlelik özet ekle. 
        Sonuna 5 adet ilgili hashtag ekle. Haber: {haber}"""
    },
    {
        "ad": "İstatistik & Analiz",
        "emoji": "📊",
        "prompt": """Sen bir futbol analisti olarak görev yapıyorsun. Aşağıdaki futbol haberini analiz et.
        Rakamları, istatistikleri ve önemli detayları ön plana çıkar. Merak uyandıran, bilgilendirici bir 
        paylaşım yaz (maksimum 3 paragraf). Sona hashtag ekle. Haber: {haber}"""
    },
    {
        "ad": "Ateşli Yorum",
        "emoji": "🔥",
        "prompt": """Sen taraflı, heyecanlı bir futbol yorumcususun. Aşağıdaki haberi okuyucuyu heyecanlandıracak,
        tartışma başlatacak şekilde yorumla. Keskin, güçlü bir dil kullan. 2-3 cümle, ardından 
        okuyuculara soru sor. Sona hashtag ekle. Haber: {haber}"""
    }
]
# ─────────────────────────────────────────────────────────


def haberleri_getir(limit=5):
    """RSS feedlerden en güncel haberleri çeker."""
    haberler = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                baslik = entry.get("title", "")
                ozet = entry.get("summary", entry.get("description", ""))
                # HTML taglerini temizle
                import re
                ozet = re.sub(r'<[^>]+>', '', ozet)
                if baslik and len(ozet) > 50:
                    haberler.append({
                        "baslik": baslik,
                        "ozet": ozet[:800],
                        "kaynak": feed.feed.get("title", url),
                        "link": entry.get("link", "")
                    })
        except Exception as e:
            print(f"Feed hatası ({url}): {e}")

    # Tekrarları kaldır, limit uygula
    seen = set()
    unique = []
    for h in haberler:
        if h["baslik"] not in seen:
            seen.add(h["baslik"])
            unique.append(h)
    return unique[:limit]


def icerik_uret(haber, tur):
    """Claude API ile belirli türde içerik üretir."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    haber_metni = f"Başlık: {haber['baslik']}\n\nDetay: {haber['ozet']}"
    prompt = tur["prompt"].format(haber=haber_metni)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def markdown_olustur(haberler, tum_icerikler):
    """Üretilen içerikleri okunabilir Markdown formatında yazar."""
    bugun = datetime.now().strftime("%d %B %Y, %H:%M")
    
    md = f"""# ⚽ Günlük Futbol İçerikleri
**Üretilme tarihi:** {bugun}

---

> 💡 **Nasıl kullanılır?** Her içeriği istediğin platforma kopyala-yapıştır yap.
> Instagram için görsel ekle, Twitter/X için uzunsa kısalt.

---

"""
    for i, (haber, icerikler) in enumerate(zip(haberler, tum_icerikler), 1):
        md += f"## 🗞️ Haber {i}: {haber['baslik']}\n"
        md += f"*Kaynak: {haber['kaynak']}*\n\n"
        
        for tur, icerik in zip(ICERIK_TURLERI, icerikler):
            md += f"### {tur['emoji']} {tur['ad']}\n"
            md += f"```\n{icerik}\n```\n\n"
        
        md += "---\n\n"
    
    return md


def main():
    print("🚀 Futbol içerik üretimi başlıyor...")
    
    # API key kontrolü
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise ValueError("ANTHROPIC_API_KEY environment variable eksik!")
    
    # Haberleri getir
    print("📡 Haberler çekiliyor...")
    haberler = haberleri_getir(limit=3)
    
    if not haberler:
        print("❌ Hiç haber bulunamadı.")
        return
    
    print(f"✅ {len(haberler)} haber bulundu.")
    
    # Her haber için içerik üret
    tum_icerikler = []
    for i, haber in enumerate(haberler, 1):
        print(f"\n🤖 Haber {i} için içerik üretiliyor: {haber['baslik'][:60]}...")
        icerikler = []
        for tur in ICERIK_TURLERI:
            print(f"  → {tur['emoji']} {tur['ad']} üretiliyor...")
            try:
                icerik = icerik_uret(haber, tur)
                icerikler.append(icerik)
            except Exception as e:
                print(f"  ❌ Hata: {e}")
                icerikler.append(f"İçerik üretilemedi: {e}")
        tum_icerikler.append(icerikler)
    
    # Markdown dosyasına yaz
    md_icerik = markdown_olustur(haberler, tum_icerikler)
    with open("icerikler.md", "w", encoding="utf-8") as f:
        f.write(md_icerik)
    
    print("\n✅ Tamamlandı! icerikler.md dosyası güncellendi.")
    print(f"📄 {len(haberler)} haber için {len(haberler) * len(ICERIK_TURLERI)} içerik üretildi.")


if __name__ == "__main__":
    main()
