# ALEXIA - Orðtökutól

ALEXIA er málheildartól sem er keyrt í gegnum skipanalínuna og tilgangur
þess er að bera saman orðaforða gagnasafns við orðaforða stórrar málheildar.
Það er nauðsynlegt til þess að viðhalda orðasöfnum, orðabókum og íðorðabönkum 
að geta farið kerfisbundið í gegnum mikið magn texta sem er álitinn táknrænn 
fyrir tungumálið eða efnisflokkinn sem er verið að skoða hverju sinni. ALEXIA
býður upp á auðvelda leið til þess að smíða slíka orðalista.

**Til þess að nota orðtökutólið með góðum árangri þarf notandinn að keyra main.py
í gegnum skipanalínuna**2
Skriftan býður upp á tvo tungumálavalmöguleika, ensku og íslensku. Hún leiðir
notandann í gegnum ýmsa valmöguleika, þar á meðal uppsetningu SQL-gagnagrunna.
Að uppsetningunni lokinni er notandanum boðið að halda áfram í keyrsluhluta
forritsins.**  

**HÉR FYRIR NEÐAN ERU LÝSINGAR Á VIRKNI TVEGGJA AÐALHLUTA FORRITSINS**

**setup_icelandic.py eða setup.py**
Þessi skrifta (þær eru eins fyrir utan tungumálið) leiðir notandann í gegnum
uppsetningu nauðsynlegra gagnagrunna fyrir ALEXIU. 

Notandinn er spurður hvort eigi að búa til gagnagrunna í gegnum sjálfvirka
uppsetningu eða hvort hann vilji leggja til eigin orðasafnsskjöl. 

Ef notendauppsetning er valin þarf notandinn að skrifa fulla slóð skjals
sem á að nota til þess að búa til orðasafnsgagnagrunn sem bera á saman við
textamálheild. **Þetta skjal á að vera á txt-sniði og innihalda fyrirsögnina
word ásamt orðalista þar sem eitt orð er í hverri línu (sjá dæmiskjalið
lexicon.txt).**

Valkvætt er að leggja til skjal sem inniheldur lista af orðum sem á að hunsa
í niðurstöðunum, þ.e.a.s. stopporðalista sem notaður er til þess að sía úttakið.
**Þetta skjal á einnig að vera á txt-sniði, með fyrirsögninni filter og orðalista
þar sem eitt orð er í hverri línu (sjá fylgiskjalið IGC_filters.txt).** 

Ef sjálfgefin uppsetning er valin þarf notandinn að gefa til kynna hvort nota eigi
Beygingarlýsingu íslensks nútímamáls (BÍN) eða Nútímamálsorðabókina (NMO) sem inntak.
Skjölunum sem þarf að nota við uppsetningu gagnagrunnana er hlaðið niður sjálfvirkt
og síðan er SQL-gagnagrunnur búinn til. Í sama skrefi er búinn til gagnagrunnur úr
stopporðalista sem var safnað úr Risamálheildinni, en hann inniheldur meðal annars
erlend orð, stafsetningarvillur, lemmuvillur, ljóslestrarvillur o.s.frv. Hafðu í 
huga að þessi gagnagrunnur er búinn til úr skjalinu IGC_filters.txt sem fylgir með
pakkanum.

**run_icelandic.py eða run.py**
Þessi skrifta leiðir notandann í gegnum ýmsa valmöguleika sem skilgreina úttakið.
Fyrst er notandinn spurður hvort hann vilji fara í gegnum demóútgáfur forritsins
eða nota sín eigin gögn. 

**Hafðu í huga að til þess að geta keyrt demóútgáfurnar rétt þarf Risamálheildin
að vera vistuð á sama hátt og er sýnt í sýnismöppunum sem fylgja pakkanum. Yfirmappan
inniheldur undirmöppuna malheildir (athugið að nöfnum mappanna er breytt sjálfvirkt 
úr ensku yfir á íslensku þegar main.py er keyrt). Hún inniheldur undirmöppuna RMH
sem aftur inniheldur undirmöppurnar CC_BY og MIM (opni hluti Risamálheildarinnar 
og Mörkuð íslensk málheild). Notandinn þarf að ganga úr skugga um að Risamálheildin
sé vistuð á sama hátt.**

Ef notandinn velur að nota eigin gögn þarf hann að skrifa fulla slóð SQL-gagnagrunnsins
sem á að bera saman við textamálheildina. Notandinn þarf síðan að skrifa fulla slóð
málheildarinnar sem hann vill nota, en hún þarf að vera á txt-sniði. Ef notandinn
vill nota stopporðagagnagrunn þarf hann að skrifa slóðina að honum en ef slíkur 
gagnagrunnur er ekki fyrir hendi skrifar hann N og ýtir á enter. **Úttakstegundirnar
sem eru í boði eru eftirfarandi:** 

- Tíðnilisti þar sem orðin sem koma ekki fyrir í inntaksgagnagrunninum (og stopporðunum,
ef þau eru fyrir hendi) eru birt ásamt tíðni þeirra í málheildinni. Listanum er raðað í 
lækkandi tíðniröð.

- Eins listi og lýst er fyrir ofan nema að hann inniheldur einnig 5-orða orðstöðulykla
úr málheildinni. Listinn og orðstöðulyklarnir eru í lækkandi tíðniröð. 

Ef önnur demóútgáfanna er valin er notandinn leiddur í gegnum ferlið skref fyrir skref
þar sem hann velur hvers konar úttak hann vill. Demóútgáfurnar eru annars vegar með 
inntaksgögnum úr Beygingarlýsingu íslensks nútímamáls (BÍN) eða Nútímamálsorðabókinni (NMO).
Samanburðarmálheildin sem er notuð í báðum tilfellum er Risamálheildin (RMH). Eftir að hafa
valið hvaða hluta Risamálheildarinnar skuli nota við samanburðinn er notandinn beðinn
um að velja hvort eigi að hunsa sérnöfn í niðurstöðunum eða ekki. Ef BÍN er valið þarf
notandinn að ákveða hvort grunnmyndin sem er notuð við samanburðinn eigi að vera lemmur
eða orðmyndir (þetta þarf ekki að gera ef Nútímamálsorðabókin er valin). Að lokum þarf
notandinn að velja tegund úttaksskjalsins. Eftirfarandi valmöguleikar eru í boði:

**LEMMUR:** 
- Listi með lemmum sem eru ekki til í inntaksgögnunum eða stopporðagagnagrunninum og 
tíðni þeirra í Risamálheildinni. Listanum er raðað í lækkandi tíðniröð. Meðfylgjandi 
eru jafnframt upplýsingar um tíðni nafnorða í eintölu og fleirtölu. Þetta getur verið
nytsamlegt til þess að átta sig á því hvort um lemmunarvillu er að ræða (eins og þegar
lemman er í eintölu en birtist í raun og veru aðeins í fleirtölu sem orðmynd) eða til 
þess að kanna hvort tiltekið orð sé aðeins til í annarri tölunni. 

- Listi með lemmum sem eru ekki til í inntaksgögnunum eða stopporðagagnagrunninum og
tíðni þeirra í Risamálheildinni en jafnframt koma fram allar orðmyndir sem fylgja
lemmunni í gögnunum. Þetta getur verið nytsamlegt til þess að athuga hvort tiltekið
orð birtist aðeins í ákveðnu samhengi (t.d. í föstu orðasambandi) eða til þess að sjá
svart á hvítu að um lemmunarvillu sé að ræða (til dæmis ef lemman er í eintölu en 
eintalan birtist aldrei í orðmyndunum). Listinn er í lækkandi tíðniröð. 

- Listi með lemmum sem eru ekki til í inntaksgögnunum eða stopporðagagnagrunninum og
tíðni þeirra í Risamálheildinni en jafnframt er tíðni hverrar lemmu innan vissra
textategunda tekin fram, s.s. í íþróttafréttum, lagatexta eða viðskiptafréttum. 
Listinn er í lækkandi tíðniröð. 

- Listi með lemmum sem eru ekki til í inntaksgögnunum eða stopporðagagnagrunninum og
tíðni þeirra í Risamálheildinni en jafnframt fylgja allt að fimm 5-orða orðstöðulyklar 
úr Risamálheildinni fyrir hverja lemmu. Listinn og orðstöðulyklarnir eru í lækkandi
tíðniröð. 

**ORÐMYNDIR (AÐEINS BÍN):**
- Listi með orðmyndum sem eru ekki til í inntaksgögnunum eða stopporðagagnagrunninum og
tíðni þeirra í Risamálheildinni. Listinn er í lækkandi tíðniröð. 

- Listi með orðmyndum sem eru ekki til í inntaksgögnunum eða stopporðagagnagrunninum og
tíðni þeirra í Risamálheildinni en jafnframt fylgja með allar lemmur sem birtast með 
orðmyndinni í Risamálheildinni. Þetta getur verið nytsamlegt til þess að átta sig á því
hvort orðmynd getur tilheyrt fleiri en einni lemmu og til þess að átta sig á umfangi
lemmuvillna. Listinn er í lækkandi tíðniröð. 

Dæmi um þessi skjöl (á ensku) fylgja með í pakkanum.

**ALEXIA er gefin út í opinni útgáfu og má auðveldlega aðlaga að öðrum tegundum
málheilda. Kóðinn inniheldur athugasemdir sem eru til þess ætlaðar að auðvelda
lagfæringar og breytingar eftir höfði notandans. Við hvetjum fólk til þess að gera
sínar eigin útgáfur sem henta þeirra þörfum.**

__Ef upp koma vandræði eða villur við notkun orðtökutólsins má hafa samband við 
Steinunni Rut Friðriksdóttur (srf2@hi.is) eða Atla Jasonarson (atlijas@simnet.is)__
