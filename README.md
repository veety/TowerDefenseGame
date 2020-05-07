**Kouluprojektina toteutettu tornipuolustuspeli.**

Kansio TowerDefense on peli python-projektina. Pelin voi käynnistää ajamalla launcher.py-tiedoston python-tulkilla.
Kansiossa gui on graafiseen käyttöliittymään liittyviä png-kuvia ja kansiossa items muita grafiikkaesineiden kuvia.
Config.txt on tekstitiedosto, johon kenttä ja vihollisaallot ovat tallennettu. Sitä voi halutessaan muokata seuraavien ohjeiden mukaan.

Config.txt:n muokkausohjeet:
- Voit muokata money- ja health-parametrejä vaihtamalla kokonaislukua kaksoispisteen perässä
- Voit muokata vihollisten polkua "EnemyPath:" perässä seuraavasti:
    - Kirjaimet U,R,D,L (englannin kielestä) merkkaavat polun, esimerkiksi UURRD tarkoittaa "kaksi ylös, kaksi oikealle, yksi alas"
    - Ensimmäinen ja viimeinen kirjain tulisi olla R ja lukumäärä(R)-lukumäärä(D)==19, jotta polku alkaa vasemmasta reunasta ja päättyy oikeaan
    - Polku voi leikata itseään vapaasti
- Voit muokata aaltorakennetta "Wave:" perässä seuraavasti:
    - Jokainen listan alkio (alalista) on oma aaltonsa
    - Rivijaolla ja whitespace-merkeillä ei ole väliä
    - Kirjaimet a,b,c vastaavat erilaisia vihollisia, a on näistä helpoin
    - Kokonaisluvut kirjainten välissä kertovat viiveestä näiden vihollisten välillä. Viiveen voi myös jättää merkitsemättä, jolloin seuraava vihollinen tulee yhden aikayksikön jälkeen.
    - Älä lisää mitään turhaa listan väliin tai sen jälkeen

Python-versio tarvitsee PyQt5-kirjaston. ("pip install pyqt5")

Pythonversio ajetaan launcher.py-tiedostosta. Tein myös exe-ohjelman, jonka voi ladata google drivestani. Linkki siihen löytyy master-haarasta. Paina drivessa "lataa kaikki".
Exe-ohjelma tulee samanlaisessa kansiossa kuin py-ohjelma. Kuvia ja config.txt:tä voi siis vapaasti muokata siinäkin. Suorita launcher.exe pelataksesi peliä.

Peliohjeet:
- Toimii kuten geneerinen tornipuolustus.
- Torneja voi ostaa klikkaamalla sellaista kaupasta ja klikkaamalla ruutua kentällä.
- Nuolipainikkeesta voi säätää nopeutta (myös [Space]) ja pelin voi pausettaa painamalla [P].
- Kentällä olevaa tornia klikkaamalla saa päivitysvalikon auki.
- Aloita uusi aalto painamalla "Next wave"
- Pelin päätyttyä voit exe-versiossa käynnistää sen uudelleen painamalla "Restart"
