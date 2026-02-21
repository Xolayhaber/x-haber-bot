print("Xolayhaber çalışıyor")

haber = "Yapay zeka sektöründe büyük yatırım dalgası başladı."

if len(haber) <= 280:
    print("Tweet hazır:")
    print(haber)
else:
    print("Metin çok uzun")
