# Bulanık Mantık ile Deprem Risk Analizi Raporu

## Ders Bilgileri

- **Ders Adı:** Bulanık Mantık
- **Proje Konusu:** Bulanık Mantık ile Deprem Risk Analizi
- **Hazırlayan:** Muhammet Ali Furkan Karamert

## 1. Projenin Amacı

Bu projenin amacı, deprem riski üzerinde etkili olan farklı faktörleri bulanık mantık yöntemiyle değerlendirerek kullanıcıya anlaşılır bir risk sonucu sunmaktır. Geleneksel sistemlerde risk değerlendirmesi genellikle kesin sınırlar üzerinden yapılırken, bu projede giriş değerleri düşük, orta, yüksek gibi bulanık kümelerle yorumlanmıştır. Böylece gerçek hayattaki belirsizlikler daha esnek ve gerçekçi şekilde modellenmiştir.

## 2. Kullanılan Yöntem

Projede Mamdani tipi bulanık çıkarım sistemi kullanılmıştır. Kullanıcıdan alınan giriş değerleri öncelikle üyelik fonksiyonlarına göre bulanıklaştırılmıştır. Daha sonra tanımlanan kural tabanı kullanılarak risk seviyesi belirlenmiştir. Son aşamada ise durulaştırma işlemi ile bulanık sonuç sayısal bir risk değerine dönüştürülmüştür.

Durulaştırma yöntemi olarak centroid yöntemi kullanılmıştır. Bu yöntem, elde edilen birleşik bulanık alanın ağırlık merkezini hesaplayarak tek bir risk puanı üretir.

## 3. Giriş Değişkenleri

Projede deprem riskini etkileyen temel değişkenler dikkate alınmıştır. Bu değişkenler genel olarak zemin yapısı, bina yaşı, kat sayısı, fay hattına uzaklık ve yapı kalitesi gibi risk üzerinde doğrudan etkili faktörlerden oluşmaktadır.

Her giriş değişkeni için uygun üyelik fonksiyonları tanımlanmıştır. Örneğin bina yaşı genç, orta ve eski olarak; risk çıktısı ise düşük, orta, yüksek ve kritik gibi seviyelerle ifade edilmiştir.

## 4. Kural Tabanı

Projede toplam 40 adet bulanık kural kullanılmıştır. Bu kurallar, farklı giriş kombinasyonlarına göre sistemin risk seviyesini belirlemesini sağlar.

Örnek olarak:

- Eğer bina yaşı eski ve zemin kötü ise risk yüksektir.
- Eğer fay hattına uzaklık az ve yapı kalitesi düşük ise risk kritiktir.
- Eğer bina yeni ve zemin iyi ise risk düşüktür.

Kural tabanı oluşturulurken riskin sadece tek bir değişkene bağlı olmadığı, birden fazla faktörün birlikte değerlendirilmesi gerektiği dikkate alınmıştır.

## 5. Python Arayüzü

Proje Python dili kullanılarak geliştirilmiştir. Arayüz kısmında Streamlit kullanılmıştır. Streamlit sayesinde kullanıcı giriş değerlerini kolayca değiştirebilmekte ve sistemin ürettiği risk sonucunu anlık olarak görebilmektedir.

Arayüzde kullanıcıya risk puanı, risk seviyesi ve grafiksel gösterimler sunulmaktadır. Bu sayede proje yalnızca sayısal çıktı veren bir sistem değil, aynı zamanda görsel olarak anlaşılır bir karar destek uygulaması haline getirilmiştir.

## 6. Grafikler ve Görselleştirme

Projede üyelik fonksiyonları, kural aktivasyonları ve durulaştırma grafiği görsel olarak gösterilmiştir. Durulaştırma grafiğinde düşük, orta, yüksek ve kritik risk kümelerinin kesilmiş alanları gösterilerek sistemin hangi risk seviyelerine ne kadar tepki verdiği anlaşılır hale getirilmiştir.

Centroid noktası grafik üzerinde işaretlenmiş ve elde edilen risk puanı kullanıcıya sunulmuştur. Bu grafikler, bulanık mantık sisteminin nasıl çalıştığını daha açık şekilde göstermektedir.

## 7. Sonuç

Bu proje ile deprem riski gibi kesin sınırlarla ifade edilmesi zor olan bir problem bulanık mantık yöntemiyle modellenmiştir. Kullanıcıdan alınan değerler, üyelik fonksiyonları ve 40 kuraldan oluşan kural tabanı ile değerlendirilmiştir.

Sonuç olarak sistem, farklı senaryolara göre düşük, orta, yüksek veya kritik risk seviyeleri üretebilmektedir. Proje, bulanık mantığın belirsizlik içeren problemlerde etkili bir karar destek yöntemi olarak kullanılabileceğini göstermektedir.

## 8. Değerlendirme

Geliştirilen sistem, kullanıcı dostu arayüzü ve grafiksel çıktıları sayesinde hem teknik hem de görsel açıdan anlaşılır bir yapıdadır. Kuralların dengelenmesiyle sistemin farklı giriş durumlarında daha tutarlı sonuçlar vermesi sağlanmıştır.

Bu çalışma, deprem risk değerlendirmesi için temel bir bulanık mantık modeli sunmaktadır. İlerleyen aşamalarda daha fazla değişken eklenerek, gerçek deprem ve yapı verileriyle sistemin doğruluğu artırılabilir.

## 9. Sistemin Güçlü ve Zayıf Yönleri

### Güçlü Yönler

- Sistem, kesin sınırlar yerine esnek değerlendirmeler yaptığı için gerçek hayattaki belirsizlikleri daha başarılı şekilde modelleyebilmektedir.

- Birden fazla risk faktörü aynı anda değerlendirildiği için daha gerçekçi sonuçlar üretilebilmektedir.

- Kullanılan 40 adet bulanık kural sayesinde farklı senaryolara uygun risk analizleri yapılabilmektedir.

- Streamlit arayüzü sayesinde kullanıcı dostu ve anlaşılır bir kullanım sunulmuştur.

- Grafiksel gösterimler sayesinde üyelik fonksiyonları, kural aktivasyonları ve durulaştırma işlemleri görsel olarak takip edilebilmektedir.

- Centroid durulaştırma yöntemi sayesinde sistem tek bir sayısal risk puanı üretebilmektedir.

- Sistem modüler yapıda geliştirildiği için ilerleyen süreçte yeni değişkenler ve yeni kurallar kolayca eklenebilir.

### Zayıf Yönler

- Sistemin doğruluğu büyük ölçüde oluşturulan kural tabanına bağlıdır. Yanlış veya eksik kurallar sonuçların doğruluğunu etkileyebilir.

- Kullanılan veriler gerçek zamanlı deprem veya yapı verileriyle desteklenmediği için sonuçlar tamamen teorik değerlendirmelere dayanmaktadır.

- Çok fazla giriş değişkeni eklendiğinde kural sayısı hızlı şekilde artacağı için sistemin yönetimi zorlaşabilir.

- Üyelik fonksiyonlarının sınır değerleri uzman görüşüne göre belirlendiğinden farklı uzmanlar farklı sonuçlar üretebilir.

- Sistem şu an temel seviyede bir karar destek modeli olarak geliştirilmiştir. Gerçek mühendislik analizlerinin yerini tamamen alamaz.

- Büyük veri kümeleri veya gerçek zamanlı analizler için performans optimizasyonu gerekebilir.