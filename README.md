# Harita Botu

Bu proje, kullanıcıların belirli şehirleri haritada görüntülemelerini ve şehirleri daha sonra görüntülemek için kaydetmelerini sağlayan bir bottur.

## Ana Özellikler

- **Haritada şehirleri görüntüleme**: Bot, seçilen şehirleri Cartopy ve Matplotlib kütüphanelerini kullanarak haritada görüntüleyebilir.
- **Şehirleri kaydetme**: Kullanıcılar, ilgilendikleri şehirleri kişisel listelerine kaydedebilir.
- **Kaydedilen şehirleri görüntüleme**: İstek üzerine, bot kullanıcı tarafından kaydedilen tüm şehirlerin listesini çıkartabilir.

## Teknolojiler

- **Python 3**: Programlama dili.
- **SQLite**: Kullanıcı ve şehir bilgilerini depolamak için veri tabanı.
- **Matplotlib and Cartopy**: Grafiksel veri temsilleri oluşturmak için kütüphaneler.
- **Discord.py**: Botları oluşturmak ve yönetmek için kütüphane.

## Kurulum ve Başlangıç

1. **Depoyu klonlayın:**
    ```bash
    git clone <depo_baglantisi>
    cd <depo_adi>
    ```
2. **Bağımlılıkları yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Ortam değişkenlerini yapılandırın:**
Projenin kök dizinindeki `config.py` dosyasını açın ve gerekli değişkenleri ayarlayın:
    ```bash
    TOKEN=<token_degeriniz>
    ```
4. **Botu çalıştırın:**
    ```bash
    python bot.py
    ```

## Bot komutları listesi:

- `!start` - Botu başlatın ve hoş geldiniz mesajı alın."
- `!help_me` - Mevcut komutların listesini alın. "
- `!show_city <şehir_adı>` - Verilen şehri haritada görüntüleyin."
- `!remember_city <şehir_adı>` - Verilen şehri kaydedin."
- `!show_my_cities` -  Tüm hatırlanan şehirleri görüntüleyin."
        
