Konceptuālais modelis: 
https://www.canva.com/design/DAHA2_dy_1Q/EhjGU5iwLxaJDN0iCdjsQQ/edit?utm_content=DAHA2_dy_1Q&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
Lietojumprogrammas loģikas slānis nodrošina visu sistēmas funkcionālo darbību. Tas apstrādā lietotāja darbības, piemēram, tēmas maiņu un paneļa atsvaidzināšanu, 
kā arī veic nepieciešamos aprēķinus un datu sagatavošanu attēlošanai. Šajā slānī tiek apstrādāts aktuālais datums un laiks, aprēķināts dienu skaits 
līdz mājasdarbu izpildes termiņiem, kā arī ģenerēti dati līniju grafikam. Kļūdu apstrāde ir ieviesta, lai nodrošinātu lietotnes stabilu darbību gadījumos, 
kad ārējie datu avoti nav pieejami.

Datu avotu slānis sastāv no ārējiem un iekšējiem datiem. Ārējie dati tiek iegūti no laikapstākļu tīmekļa pakalpojuma wttr.in, kas nodrošina informāciju 
par aktuālo temperatūru, sajūtu kā temperatūru un laikapstākļu aprakstu. Iekšējie dati tiek glabāti pašā lietojumprogrammā un ietver mājasdarbu sarakstu, 
kas strukturēts Pandas DataFrame formātā, kā arī nejauši ģenerētus skaitliskus datus grafika attēlošanai.

Stāvokļa un veiktspējas pārvaldībai tiek izmantoti Streamlit mehānismi st.session_state un st.cache_data. Sesijas stāvoklis nodrošina lietotāja iestatījumu, 
piemēram, izvēlētās tēmas un ievadīto piezīmju saglabāšanu lietošanas laikā. Kešatmiņa tiek izmantota laikapstākļu datu saglabāšanai noteiktu laika periodu,
tādējādi samazinot atkārtotu ārējo API pieprasījumu skaitu un uzlabojot lietojumprogrammas darbības ātrumu.

Kopumā lietojumprogramma ir izstrādāta kā monolīta tīmekļa lietotne bez atsevišķas datubāzes, kurā visi komponenti darbojas vienotā izpildes vidē. 
Šāda arhitektūra ir piemērota neliela mēroga projektiem, mācību nolūkiem un prototipiem, jo tā ir vienkārši uzturama, 
viegli paplašināma un nodrošina skaidru struktūru starp lietotāja interfeisu, loģiku un datu apstrādi.
Digitālais informācijas panelis ir personisks un interaktīvs rīks,
kas ļauj lietotājam uzreiz pārskatīt un organizēt svarīgāko ikdienas informāciju vienā centrālā vietā. Tā mērķis ir uzlabot lietotāja 
laika plānošanu, produktivitāti un informācijas pārvaldību, piedāvājot vienkāršu, vizuāli pievilcīgu un lietotājam draudzīgu saskarni.

Paneļa funkcionalitāte ietver vairākus galvenos moduļus:

Reāllaika pulkstenis un datums – panelī tiek parādīts aktuālais laiks un datums, ļaujot lietotājam vienmēr būt informētam par laiku,
kas ir svarīgi gan mācībām, gan ikdienas aktivitātēm. 
Laikapstākļu informācija – tiek parādīta aktuālā temperatūra, sajūta kā temperatūra un īss laikapstākļu apraksts izvēlētajā pilsētā (piemēram, Rīgā). 
Dati tiek iegūti no publiska API, un informācija tiek regulāri atsvaidzināta, lai nodrošinātu precīzus laikapstākļu datus.

Mājasdarbu un uzdevumu pārvaldība – lietotājs var sekot līdzi visiem saviem uzdevumiem, redzot priekšmetu, uzdevuma veidu, komentārus 
un termiņu. Paneļa tabula aprēķina, cik dienas atlicis līdz katra uzdevuma nodošanai, ļaujot vieglāk plānot laiku un prioritizēt darbus. 
Šis modulis palīdz samazināt aizmāršību un veicina disciplīnu, nodrošinot vizuālu pārskatu par gaidāmajām saistībām.

Ātrās piezīmes (notepad funkcionalitāte) – lietotājs var rakstīt un saglabāt īsas piezīmes, idejas vai atgādinājumus tieši panelī. 
Šīs piezīmes tiek saglabātas sesijas līmenī, nodrošinot, ka svarīgā informācija paliek pieejama tik ilgi, kamēr panelis ir atvērts. 
Šī funkcija palīdz koncentrēties un ātri pierakstīt svarīgas domas bez nepieciešamības atvērt papildu rīkus.

Datu vizualizācija (grafiki) – panelis piedāvā vienkāršu datu grafiku, kas ļauj lietotājam vizualizēt informāciju vai trendus. 
Šī funkcija var tikt pielāgota, lai attēlotu dažādu veidu datus, piemēram, mācību progresu, aktivitāšu statistiku vai citus kvantitatīvus rādītājus,
padarot informāciju vieglāk uztveramu.

Tēmas izvēle (Light/Dark režīms) un atsvaidzināšana - lietotājs var mainīt paneles vizuālo stilu atbilstoši personīgajām vēlmēm vai vides apgaismojumam, 
kā arī manuāli atsvaidzināt paneli, lai atjaunotu datus un nodrošinātu aktuālu informāciju.

Risinājuma arhitektūra:
Paneļa arhitektūra sastāv no trīs galvenajiem slāņiem:

Frontend (Lietotāja saskarne) – Streamlit lietotāja interfeiss ar sānu paneli iestatījumiem, galveno lapu ar 
moduļiem: pulkstenis, laikapstākļi, mājasdarbi, piezīmes un grafiki.

Backend (Datu apstrāde) – Laikapstākļu datu iegūšana no publiska API (wttr.in), mājasdarbu datu apstrāde ar pandas DataFrame, 
piezīmju saglabāšana sesijas līmenī (st.session_state), datu vizualizācija (st.line_chart).

Datu slānis – Laikapstākļu dati tiek iegūti tiešsaistē (JSON formātā), mājasdarbi definēti lokāli Python datu struktūrā, piezīmju dati saglabāti sesijas līmenī.

Datplūsmas modelis:
Lietotājs mijiedarbojas ar frontend, kur:

*Sesijas dati (piezīmes, tēma) tiek saglabāti lokāli.
*Laikapstākļi tiek iegūti no API, parsēti un attēloti.
*Mājasdarbi tiek rādīti tabulas formātā ar aprēķinātajām atlikušajām dienām.
*Grafiki tiek ģenerēti no testa datiem (vai nākotnē no reāliem datiem).

Lietotāji:

Galvenie lietotāji: skolēni un studenti, kuri vēlas pārskatīt laiku, uzdevumus un piezīmes vienā panelī.
Papildu lietotāji: pedagogi vai vecāki, kuri uzrauga uzdevumus.
Lietotāja prasības: vienkārša, vizuāli pievilcīga saskarne un interaktīvs saturs.

Tehnoloģijas:
Programmatūras ietvars: Python + Streamlit
Bibliotēkas: pandas, requests, datetime, random
Stils: CSS tēmas maiņai (Light/Dark)

Datu avoti: publiska laikapstākļu API (wttr.in) un lokāli definēti mājasdarbi/piezīmes
Piegādes formāts:
Tīmekļa lietotne, darbojas lokāli vai serverī ar Python.

Palaišanas komanda:

.\venv\Scripts\Activate.ps1
streamlit run 2026_projekts.py

Nepieciešams interneta pieslēgums laikapstākļu datu iegūšanai.

Darba plāns:
02.02.2026 – Projekta specifikācija
      *Definēt projekta mērķi un uzdevumus
      *Aprakstīt galvenās lietotnes funkcijas
      *Izvēlēties izmantotās tehnoloģijas (Python, Streamlit, API)
      *Izstrādāt konceptuālo arhitektūras modeli
16.02.2026 – Pamata struktūras pilnveidošana
      *Uzlabot Streamlit projekta struktūru, sadalot kodu loģiskos blokos
      *Paplašināt galveno izkārtojumu, lai tas atbalstītu dinamisku sadaļu parādīšanu
      *Papildināt tēmas pārslēgšanu ar lietotāja iestatījumu saglabāšanu
      *Paplašināt session_state, lai saglabātu lietotāja izvēles par redzamajām funkcijām
04.03.2026 – Funkcionalitātes paplašināšana
      *Izveidot iespēju lietotājam izvēlēties, kuras funkcijas tiek rādītas panelī  
      *Pievienot iespēju rediģēt mājasdarbu datus (pievienot, dzēst, labot) 
      *Izveidot iespēju mainīt laikapstākļu pilsētu
      *Pievienot iespēju pielāgot grafika attēlotos datus
      *Saglabāt lietotāja pielāgojumus sesijā

18.03.2026 – Paplašinātās funkcijas
      *e-Klases datu integrācijas prototips
      *Mājasdarbu vai stundu saraksta attēlošana
      *Iespēja manuāli pievienot / dzēst mājasdarbus
      *Datu kešošanas optimizācija
      *Kļūdu apstrādes uzlabošana

31.03.2026 – UI un Frontend pabeigšana
      *Lietotnes dizaina pilnveide
      *Tumšā režīma uzlabošana
      *Lietotāja saskarnes loģikas uzlabošana
      *Iespēja pielāgot paneli lietotāja vajadzībām

10.04.2026 – Lietotāja pielāgojumi
      *Iespēja izvēlēties pilsētu laikapstākļiem
      *Iespēja mainīt valodu (LV / EN)
      *Individuālu iestatījumu saglabāšana sesijā

21.04.2026 – Testēšana un Debug
    *Funkcionalitātes testēšana
    *e-Klases integrācijas pārbaude
    *Kļūdu labošana
    *Veiktspējas uzlabošana

01.05.2026 – Projekta gala versija
      *Koda sakārtošana un dokumentēšana
      *Projekta apraksta sagatavošana
      *Lietotnes sagatavošana demonstrācijai

08.05.2026 – Beigu projekta prezentācija
      *Gatavās lietotnes demonstrācija
      *Funkciju izskaidrošana
      *Secinājumi un nākotnes uzlabojumi
  
