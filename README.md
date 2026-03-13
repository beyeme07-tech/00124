# ⚽ Futbol İçerik Botu

Her gün otomatik olarak güncel futbol haberleri çeken ve Claude AI ile 3 farklı formatta içerik üreten sistem.

## 🚀 Kurulum (10 dakika)

### 1. Bu repoyu GitHub'a yükle
```bash
git init
git add .
git commit -m "İlk yükleme"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/futbol-bot.git
git push -u origin main
```

### 2. Anthropic API Anahtarı Al
1. [console.anthropic.com](https://console.anthropic.com) adresine git
2. Hesap oluştur → **$5 ücretsiz kredi** geliyor
3. "API Keys" → "Create Key" → Kopyala

### 3. GitHub Secret Ekle
1. GitHub'da reponun **Settings** sekmesine git
2. Sol menüden **Secrets and variables → Actions**
3. **New repository secret** tıkla
4. Name: `ANTHROPIC_API_KEY`
5. Value: az önce kopyaladığın anahtar
6. **Add secret** tıkla

### 4. GitHub Actions'ı Etkinleştir
1. Reponun **Actions** sekmesine git
2. "I understand my workflows, go ahead and enable them" tıkla

---

## 📅 Çalışma Saatleri

Bot her gün **3 kez** çalışır:
| UTC | Türkiye Saati |
|-----|--------------|
| 07:00 | 10:00 |
| 12:00 | 15:00 |
| 18:00 | 21:00 |

İstersen `.github/workflows/icerik_uret.yml` dosyasındaki `cron` satırlarını değiştirerek saatleri ayarlayabilirsin.

---

## 📄 Çıktı Nasıl Görünür?

Her çalışmadan sonra `icerikler.md` dosyası güncellenir. İçinde 3 haber için 3'er farklı içerik bulunur:

- 📰 **Haber Özeti** → Bilgilendirici, hashtag'li paylaşım
- 📊 **İstatistik & Analiz** → Rakam odaklı, analitik içerik  
- 🔥 **Ateşli Yorum** → Tartışma başlatan, soru soran içerik

Beğendiğin içeriği kopyala → Instagram/Twitter'a yapıştır!

---

## 💰 Maliyet

| Bileşen | Maliyet |
|---------|---------|
| GitHub Actions | **Ücretsiz** (ayda 2000 dk) |
| Claude API | ~$0.01 per çalışma (~$1/ay) |
| RSS Feedler | **Ücretsiz** |

---

## ✏️ Özelleştirme

`icerik_uret.py` dosyasında:
- `RSS_FEEDS` → Farklı haber kaynakları ekle
- `ICERIK_TURLERI` → İçerik türlerini ve promptları değiştir
- `limit=3` → Kaç haber işleneceğini ayarla
