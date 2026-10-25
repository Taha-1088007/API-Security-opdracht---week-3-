# Werkplaats 3 - Test-Correct
Gemaakt door:\
-Donovan Feller (1073598) \
-Lucas Reedijk (1054292) \
-Taha Ditta (1088007)

Iemand anders die ook gewerkt heeft aan het project:\
-Chris de Lijster (1035052) 

**Beschrijving:**\
Wij als groep 1C2 Hyena's hebben een webapplicatie gebouwd waarvan 2 soorten mensen gebruik kunnen maken, deze zullen hieronder verder worden uitgelicht met hierbij ook de funcitonaliteiten van de webapplicatie.
Allereerst een student die kan inloggen met zijn/haar e-mailadres en wachtwoord, zodra de student is ingelogd komt hij/zij terecht op de homepagina waarin hij/zij direct zijn gemiddelde score, hoeveelheid vakken op niveau en het volledige aantal vakken dat hij/zij heeft ziet.
Vervolgens kan hij/zij via de navigatiebar worden omgeleid naar diverse pagina's waarin hij/zij de volgende dingen kan zien: zijn/haar voortgang over de tijd in een grafiek, 
ook kan hij/zij zien welke leerdoelen voor hem/haar zwak en sterk zijn, daarnaast heeft hij/zij inzicht in zijn/haar vakken met hierbij direct de status per vak.
Tot slot heeft de student ook een eigen profielpagina waarin hij/zij een aantal persoonsgebonden gegevens en huidige (voortgangs)status in een oogopslag kan zien.

Naast de studentenrol hebben wij ook een docentenrol waarin hij/zij ook kan inloggen met zijn/haar e-mailadres en wachtwoord,
zodra de docent is ingelogd komt hij/zij terecht op de homepagina waarin hij/zij direct de hoeveelheid leerlingen in zijn klas en de hoeveelheid leerlingen die extra aandacht nodig hebben kan zien. 
Vervolgens kan hij/zij via de navigatiebar worden omgeleid naar diverse pagina's waarin hij de volgende dingen kan zien: een klassenoverzicht met hierin de namen van alle studenten die hij/zij les geeft gepaard met hun status (hoe ze ervoor staan bij het vak van de docent). 
Ook heeft de docent een analyse pagina waarin hij een grafiek terugziet met alle scores op basis van alle 4 de taxonomieniveau's: Analyseren, Begrijpen, Onthouden, Toepassen. Daarnaast wordt hier ook aangegeven op welke taxonomieniveaus de klas laag scoort en welke onderwerpen hierbij belangrijk zijn om terug te brengen in de les.
Daarnaast heeft de docent ook een onderwerpen pagina waarin hij/zij in een grafiek van zijn gehele klas (alle studenten) kan hij/zij per student de score's van kennen en kunnen zijn en op basis hiervan wordt bepaald voor welke leerdoelen de klas zwak heeft gescoord en daarnaast worden ook individueel per kennen en kunnen onderwerpen die van belang zijn om in de les te behandelen benoemd.
Tot slot heeft de docent ook een profielpagina waarin hij/zij een aantal persoonsgebonden gegevens in een oogopslag kan zien. 

Wij hebben bewust gekozen om het gemiddelde te nemen van kennen + kunnen om zo een accuraat cijfer te kunnen berekenen op basis van zowel de student zijn/haar kennis als uitvoering en implementatie van deze kennis.
Bij het verwerken hiervan hebben we bewust gekozen om motiverende teksten te gebruiken gepaard met gepaste kleurkeuzes om de student een zo goed mogelijk beeld te geven van zijn voortgang. Ook hebben we hier dus bewust overnagedacht om (los van in het profiel) zo min mogelijk exacte cijfers te tonen om de student zo een fijne, positieve maar toch accurate update te geven over zijn voortgang.

Bij de docent hebben we overigens ook gebruik gemaakt van dezelfde keuzes die we bewust hebben gemaakt bij de student maar hier hebben we ervoor gekozen om wat meer exacte resultaten van zowel kennen en kunnen los van elkaar als het gemiddelde van beiden bij elkaar opgeteld te vertonen in grafieken en een klassenoverzicht. Dit zodat de docent exact kan weten hoe zijn studenten ervoor staan en ze hierbij ook individueel en klasikaal zo goed mogelijk hulp kan bieden wanneer nodig.

Dit alles is zo verwerkt dat het voor de gebruiker toegankelijk en fijn in gebruik is, ook hebben we hierbij de WCAG-richtlijnen geïmplementeerd/opgevolgd.







# Installatie instructies 
In stappen hieronder zal ik beschrijven hoe u onze bestanden kunt installeren:
1. Download onze zip file.
2. Haal de Folder uit die zipfile (het is de bedoeling dat je 1 folder heb waarin alle bestanden en overige folders behorend bij het project staan, als je dit hebt dan is dat voldaan)
3. Open de folder met een door u gekozen IDE (bijvoorbeeld PyCharm of Visual Studio Code).
4. Zorg ervoor dat u Python versie 3.13 gebruikt als Python interpreter in dit project.
5. Installeer de benodigdheden het bestand genaamd "requirements.txt" (zie de command hieronder)

**macOS gebruikers:** op macOS kan het zijn dat de onderstaande commands niet werken, gebruik dan pip3 in plaats van pip & python3 in plaats van python bij de commands. 

````
```
pip install -r requirements.txt
```
````


# Opstart instructies
Hier zal ik beschrijven hoe u onze webapplicatie opstart nadat u de bestanden in een IDE open hebt staan: 

Mocht u bij het openen van uw folder al een app.db hebben staan in de folder "data" verwijder deze dan en voer daarna pas de onderstaande stappen uit.

Mocht er iets verkeerd gaan begin dan opnieuw en voer ALLE stappen op chronologische wijze opnieuw uit om (vervolg)conflicten te voorkomen.

1. Open jouw File Explorer en open de folder van dit project, vervolgens open je de "data" folder, in deze data folder staat een (compressed) zip folder genaamd data-sample/data-sample.zip, 
ga in deze zip folder en daarin zie je een JSON Source File genaamd data-sample, 
haal dit bestand (data-sample (JSON Source File)) uit die zip folder en 
zet hem (als los bestand) in de "data" folder. 
Als je dit gedaan hebt hoort jouw "data" folder er als volgt (zie hieronder) uit te zien in jouw File Explorer & IDE (het is de bedoeling/normaal dat u nog geen app/app.db ziet staan in uw "data" folder, 
deze wordt later aangemaakt bij het verder uitvoeren van de stappen, dus raak niet verward als je het wel ziet staan in de onderstaande afbeeldingen).

__File Exporer:__ \
![File Explorer WP3 (data folder).png](static/images/File%20Explorer%20WP3%20%28data%20folder%29.png)


__IDE:__ \
![IDE WP3 (data folder).png](static/images/IDE%20WP3%20%28data%20folder%29.png)

2. Wanneer u ons project open hebt staan in de door u gekozen IDE, kunt u in de terminal "python app.py" typen en op enter klikken (dit creeërt de tabellen en kolommen van de database)
````
```
python app.py
```
````

3. **BELANGRIJK**: Hierbij (het runnen van de bovenstaande command) kan er een error tevoorschijn komen, schrik hier niet van en run vervolgens de onderstaande command. & Mocht je geen error ontvangen/zien in je terminal sluit dan je terminal, open hem opnieuw en run de onderstaande command.
````
```
python import_data.py
```
````


Wacht vervolgens en voer GEEN command uit (ga niet over naar de volgende stap), totdat je dit ziet in de terminal: *Import voltooid.*


4. Wanneer u de bovenstaande stappen heeft uitgevoerd, kunt u in de terminal (opnieuw) "python app.py" typen en op enter klikken. 
````
```
python app.py
```
````
5. Klik op de link die u onderin het scherm (in de terminal) ziet.
6. Als het gelukt is bent u nu op het inlog scherm terecht gekomen. (hier kunt u een rol kiezen: docent of student)
7. U vult de gegevens die hieronder bij "Inloggen gebruikers" staan in om verder te gaan. 


__Terminal voorbeeld bij de opstartinstructies (screenshot):__ \
![Terminal opstartinstructies voorbeeld (screenshot).png](static/images/Terminal%20opstartinstructies%20voorbeeld%20%28screenshot%29.png)



# Inloggen gebruikers

Voor onze website zijn er 2 rollen: **docenten** en **studenten**
 

**Als docent kunt u inloggen met deze gegevens:**\
Email: willem@school.nl \
Wachtwoord: secret

Email: jolanthe@school.nl \
Wachtwoord: secret

Email: pamela@school.nl \
Wachtwoord: secret

Email: alexander@school.nl \
Wachtwoord: secret 



**Als student kunt u inloggen met deze gegevens:**\
Email: sam@school.nl \
Wachtwoord: secret

Email: alex@school.nl \
Wachtwoord: secret

Email: jamie@school.nl \
Wachtwoord: secret

Email: taylor@school.nl \
Wachtwoord: secret

Email: robin@school.nl \
Wachtwoord: secret

Email: noah@school.nl \
Wachtwoord: secret

Email: emma@school.nl \
Wachtwoord: secret

Email: milan@school.nl \
Wachtwoord: secret

Email: lotte@school.nl \
Wachtwoord: secret

Email: daan@school.nl \
Wachtwoord: secret 


- __Andere dingen die wij willen melden en/of belangrijk zijn (bonus functionaliteiten):__
1. We hebben een dynamische homepage gemaakt voor zowel student als docent waarin bepaalde kerninformatie (zoals verder uitgelicht in de beschrijving) in 1 oogopslag zichtbaar is.
2. We hebben een dynamische profielpagina voor zowel student als docent gemaakt waarin bepaalde persoonsgebonden informatie en (bij de student) de status van een student met de gemiddelde cijfers van alle vakken zichtbaar is

- **ERD:**
De ERD van de database staat in hieronder & in hetzelfde path als deze README.md. \
![ERD_bij_database_WP3 V2.png](ERD_bij_database_WP3%20V2.png) 
.
.
.
- __Bronvermelding:__ \
De bronvermelding van elk projectlid is terug te vinden in de folder "bronnen" (met daarin ook een folder AI-bronnen) in dit project.
