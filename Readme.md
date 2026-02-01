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
2.02.2026 Specifikācija
4.03.2026 Funkcionalitātes pabeigšana, tostarp, jaunas funkcijas un iespēja modificēt lietotni saviem nolukiem.
31.03.2026 UI un Frontend nobeigšana, tostarp dizains un iespēja modifiēt lietotni uz lietotāja velmi
21.04.2026 Testēšana un DeBug funkcionalitāte
8.05.2026 beigu projekta prezentācija
  
