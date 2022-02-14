# AAB_College_Exam_Auto_Alert
Është një skript që mund të përdoret nga studentët e Kolegjit AAB, skripta kontrollon rezultatet e provimeve nëse janë përditësuar, gjatë afateve të provimeve, supozohet se deri në kohen e konsultimit duhet të pranoni rezultatin, keshtu permes kesaj skripte mund te kontrolloni qdo dite per pune sekondash.  Pas Instalimit e vendos ne schedule qe te ekzekutohet qdo dite, pastaj qdo dite do te pranoni njoftimet ne email  (Nese keni nje rezultat te ri, Nese nuk keni risi, Nese fjalkalimi juaj eshte rivendosur)

[1] Klonoje.

[2] Permirsoni dosjet EMAIL.py dhe AAB.py
 _config = {
        'email': "<Email juaj>",
        'password': "<fjalkalimi juaj>",
        'smtp': "smtp.gmail.com",
        'port': 587
    }
    
 _config = {
        'username': "<perdoruesi>",
        'password': "<fjalkalimi>",
        'charset': "UTF-8"
    }
    
[3] Shtoni kredencialet tuaja te email dhe te eservice 

[4] Skripten APP.py vendoseni ne schedule per kohen 24ore

 Njoftimet do ti pranoni me email
  
 License: Perdorimi, permirsimi, feel free.
