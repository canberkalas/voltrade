# voltrade SRSIbot-python ile binance api kullanarak futures işlemlerde 5x kaldıraç ile işlem yapıyor,Stoch RSI 80 üzerinde iken, K çizgisi D yi aşşağı keser ise short pozisyon, Stoch RSI değeri 20 altında iken, K çizgisi D yi yukar yönlü keser ise long pozisyon açıyor.pozisyon %1.3 kara ulaştığında kapatıyor ve pozisyon %0.43 zarara ulaştığında pozisyonu kapatıyor.botun kullanıcı tarafından açılıp-kapatılması gerekiyor, açık olduğunda sürekli olarak bahsedilen doğru işlem noktasını kontrol ediyor.

Bu kod gerçek para ile çalışacak şekilde tasarlanmıştır, bu nedenle önce bir sanal para hesabı oluşturmanızı ve bu hesabı kullanarak botunuzu test etmenizi öneririz.

Bu kodu çalıştırmak için birkaç pakete ihtiyacınız var, örneğin numpy, talib, python-binance, ve schedule gibi. Bu paketlerin yüklenmesi için önceden yüklemeniz gerekebilir.

Binance API'ını kullanarak gerçek işlemler yapmak için bir API anahtarı ve gizli anahtara ihtiyacınız olacak. Bu anahtarları güvenli bir şekilde sakladığınızdan emin olun.

Bu kodu çalıştırırken doğru simgeyi (symbol) belirlemeniz ve doğru futures sözleşmesini (contract_type) belirlemeniz gerekir.

Bu kodda belirtilen strateji, piyasanın nasıl hareket edeceğine dair bir tahmin yapmaktır. Hiçbir strateji kesin kazanç sağlamaz ve bazı durumlarda zarar edebilirsiniz. Bu nedenle, botunuzu çalıştırmadan önce risk yönetimi stratejilerini anlamak ve kullanmak önemlidir.

Binance API'nın kullanımıyla ilgili belirli sınırlamalar vardır. Aşırı kullanım, API anahtarınızın geçici olarak veya kalıcı olarak kapatılmasına neden olabilir. Bu nedenle, botunuzu çalıştırmadan önce API sınırlamalarını ve kısıtlamalarını öğrenmeniz önemlidir.
