# 📚 Manual d'Usuari CoopConsum

## 🏠 Introducció

**CoopConsum** és un sistema complet de gestió per cooperatives de consum responsable. Aquesta aplicació web permet gestionar comandes col·lectives, inventari, saldos dels socis i molt més.

### 🔐 Com Accedir al Sistema

1. **URL d'accés**: `http://your-server-ip/accounts/login/`
2. **Credencials**: Usuari i contrasenya proporcionats per l'administrador
3. **Primer accés**: Canvia la contrasenya per defecte

---

## 👤 Funcionalitats dels Socis (Intranet)

### 📅 Dashboard Principal - Calendari

**Accés**: Menú lateral > "Calendari" o després del login

**Funcionalitats**:
- **Calendari visual** amb dates d'obertura i tancament de comandes
- **Vista mensual** amb esdeveniments de la cooperativa
- **Colors diferenciats** per tipus d'esdeveniments
- **Navegació** entre mesos per planificar participacions

**Com utilitzar-ho**:
1. Les dates marcades mostren quan s'obren/tanquen comandes
2. Fes clic en un esdeveniment per veure detalls
3. Utilitza les fletxes per navegar entre mesos

---

### 🏠 Panell del Soci

**Accés**: Menú lateral > "Socis" o icona d'usuari al navbar

#### 📊 Informació Personal
- **Comandes recents** amb estat i imports
- **Saldo actual** del moneder digital
- **Historial de moviments** de la compte
- **Desitjos actius** amb seguiment d'estat

#### 💰 Gestió del Moneder

**Consulta de Saldo**:
- Saldo actual visible a la pantalla principal
- Historial complet de moviments
- Estats: Validat, Pendent, Descomptat

**Enviar Ingrés per Validar**:
1. Omple l'**import** en euros
2. Adjunta **justificant** (opcional) - captura de la transferència
3. Afegeix **comentari** (opcional) - pots deixar-ho en blanc
4. Si no poses comentari, s'assigna automàticament "Ingrés enviat per validar"
5. Fes clic a "Enviar per a validar"
6. L'administrador validarà l'ingrés

#### 📋 Comandes Recents i Anteriors

**Comandes Recents**:
- Llista de comandes amb **estat actual**
- **Import total** gastat en cada comanda
- **Botó "Veure"** per detalls dels productes
- **Botó d'edició** si la comanda està oberta

**Comandes Anteriors**:
- **Paginació** per navegar l'historial
- **Detalls complets** de cada participació
- **Dates de lliurament** i imports finals

#### 💡 Sistema de Desitjos

**Desitjos Actius**:
- Llista de **cartes de desitjos** disponibles
- **Estat de cada carta**: Activa, Mínim Aconseguit, Completada
- **Els teus interessos** registrats en cada carta
- **Botó d'accés** per veure/editar interessos

---

### 📦 Productes i Catàleg

**Accés**: Menú lateral > "Productes" (submenú)

#### 🗂️ Navegació per Productes

**Tots els Productes**:
- **Llistat complet** de productes disponibles
- **Informació detallada**: Nom, preu, proveïdor, categoria
- **Imatges** dels productes quan disponibles
- **Unitat de venda**: Unitat, kg, g, litre

**Categories**:
- **Filtratge per categoria**: Verdures, Fruites, Cereals, etc.
- **Navegació intuïtiva** per trobar productes específics
- **Comptador** de productes per categoria

**Proveïdors**:
- **Llistat de proveïdors** amb informació de contacte
- **Productes per proveïdor** per conèixer l'origen
- **Informació de contacte** i descripció del proveïdor

---

### 🛒 Sistema de Comandes

**Accés**: Menú lateral > "Comandes" (badge amb número si hi ha obertes)

#### 🔄 Cicle de Vida d'una Comanda

**Procés complet** que segueixen totes les comandes col·lectives:

##### **1. ESTAT OBERT** 🟢
- **Durada**: Des de l'obertura fins la data límit
- **Socis poden**: Afegir, modificar i eliminar productes
- **Gestors poden**: Supervisar participacions
- **Master pot**: Monitoritzar activitat

##### **2. ESTAT PENDENT** 🟡  
- **Quan**: Després de la data límit de participació
- **Socis**: NO poden modificar res
- **Gestors de comanda poden**: 
  - Afegir/eliminar productes si algú s'ha oblidat
  - Ajustar quantitats segons necessitats especials
  - Revisar participacions abans d'enviar al proveïdor
- **Master pot**: Enviar revisions i correccions a la comanda

##### **3. REVISIÓ ACCEPTADA** 🔄
- **Quan**: El gestor accepta una revisió del Master
- **NINGÚ pot modificar** ja la comanda
- **Gestors només poden**: Finalitzar la comanda
- **Estat temporal** abans del tancament definitiu

##### **4. ESTAT INACTIU** ⚫
- **Comanda finalitzada** completament
- **Es descompta del moneder** de tots els socis participants
- **No es pot modificar** per ningú
- **Procés completat** - productes llestos per recollir

#### 📝 Participar en Comandes Obertes

**Procés de participació** (només en estat 🟢 OBERT):
1. **Selecciona una comanda oberta** de la llista
2. **Afegeix productes** amb les quantitats desitjades
3. **Revisa el total** abans de confirmar
4. **Guarda la comanda** - es descomptarà quan passi a INACTIU

#### ✏️ Editar les Teves Participacions

**Quan pots modificar**:
- **Només en estat 🟢 OBERT**: Pots afegir, canviar i eliminar productes
- **En estat 🟡 PENDENT o posterior**: NO es pot modificar

**Modificacions permeses** (estat OBERT):
- **Afegir nous productes** a la teva participació
- **Canviar quantitats** dels productes existents
- **Eliminar productes** que no vols
- **Veure total actualitzat** en temps real

**Limitacions sempre**:
- Les modificacions han de respectar el **saldo disponible**
- No pots modificar participacions d'altres socis

---

### 📊 Stock i Inventari

**Accés**: Menú lateral > "Estoc" (submenú)

#### 📋 Consulta d'Estoc

**Tots els Productes d'Estoc**:
- **Nivells d'inventari** actuals
- **Productes disponibles** per compra immediata
- **Preus actuals** i unitats de venda

**Estoc per Categories**:
- **Filtratge per categoria** per trobar productes específics
- **Nivells de stock** per categoria

**Estoc per Proveïdors**:
- **Disponibilitat per proveïdor**
- **Comparació de preus** entre proveïdors

#### 🛍️ Compres d'Estoc

**Procés de compra**:
- Els productes d'estoc es poden **comprar individualment**
- **Descompte immediat** del moneder
- **Registre automàtic** de la transacció

---

### 💡 Sistema de Desitjos

**Accés**: Menú lateral > "Desitjos"

#### 🌟 Cartes de Desitjos

**Què són les cartes de desitjos**:
- **Propostes de productes** que la cooperativa pot incorporar
- **Sistema de pre-comandes** per avaluar demanda
- **Mínims necessaris** per fer viable la compra

**Estats de les cartes**:
- **📝 Esborrany**: En preparació
- **✅ Activa**: Oberta per expressions d'interès
- **⏸️ Pausada**: Temporalment inactiva
- **🎯 Mínim Aconseguit**: Suficient demanda, es procesarà
- **✅ Completada**: Processada i finalitzada
- **📁 Arxivada**: Guardada per referència

#### 🙋 Expressar Interès

**Com participar**:
1. **Explora les cartes** disponibles
2. **Selecciona una carta** que t'interessi
3. **Indica la quantitat** que voldries de cada producte
4. **Confirma el teu interès**
5. **Segueix l'evolució** de la carta

**Beneficis**:
- **Influir en el catàleg** de la cooperativa
- **Accés prioritari** a nous productes
- **Preus més competitius** per volum

---

## 🔧 Funcionalitats Avançades (Permisos Especials)

### 🌱 Gestió de Productes

**Qui hi té accés**: Socis amb permís "gestiona_productos" i superusuaris

**Funcionalitats**:
- **Afegir nous productes** al catàleg
- **Editar informació** de productes existents
- **Gestionar imatges** i descripcions
- **Establir preus** i unitats de venda
- **Assignar categories** i proveïdors

**Procés d'afegir producte**:
1. Accedeix a la gestió de productes
2. Omple la informació: nom, descripció, preu
3. Selecciona categoria i proveïdor
4. Puja imatge (opcional)
5. Defineix unitat de venda
6. Marca si és producte d'estoc

---

### 📋 Gestió de Comandes

**Qui hi té accés**: Responsables de comandes i gestors

#### 🔄 Gestió d'Estats de Comandes

**Responsabilitats del Gestor de Comandes**:

##### **Estat 🟢 OBERT**
- **Supervisar participacions** dels socis
- **Resoldre dubtes** sobre productes i quantitats
- **Monitoritzar** nivells de participació per categoria

##### **Estat 🟡 PENDENT**
- **Revisar totes les participacions** abans d'enviar al proveïdor
- **Afegir productes oblidats** per socis que ho sol·licitin
- **Ajustar quantitats** segons necessitats especials
- **Preparar comanda final** per enviar al proveïdor
- **Rebre i revisar revisions** del Master

##### **Estat 🔄 REVISIÓ ACCEPTADA**
- **Acceptar revisions** proposades pel Master
- **Finalitzar la comanda** definitivament
- **NO es pot modificar** cap producte o quantitat

##### **Estat ⚫ INACTIU**
- **Comanda completada** - es descompta automàticament del moneder
- **Coordinació del lliurament** segons dates establertes
- **Resolució d'incidències** de productes no disponibles

**Funcionalitats principals**:

#### 🔄 Comandes Recurrents
- **Crear comandes setmanals/quinzenals/mensuals**
- **Definir dies d'obertura** i tancament
- **Assignar categories** i proveïdors específics
- **Gestionar el cicle de vida** de les comandes

#### 📊 Gestió de Pedidos Col·lectius
- **Revisar participacions** dels socis
- **Validar i tancar** comandes
- **Generar resums** per proveïdors
- **Controlar dates** de lliurament

#### ⚠️ Propostes de Correcció
- **Revisar propostes** de modificació
- **Aprovar/rebutjar** canvis sol·licitats
- **Comunicar decisions** als socis

---

### 📦 Gestió d'Estoc

**Qui hi té accés**: Socis amb permís "gestiona_stock" i superusuaris

**Funcionalitats**:

#### 📥 Registrar Entrades
- **Registrar compres** d'estoc
- **Actualitzar nivells** d'inventari
- **Controlar costos** i preus de venda

#### ✅ Validació de Compres
- **Revisar registres** de compra de socis
- **Validar transaccions** d'estoc
- **Gestionar sessions** de recollida

#### 📊 Control d'Inventari
- **Monitoritzar nivells** d'estoc
- **Alertes de stock mínim**
- **Historial de moviments**

---

### 🎯 Comandes Esporàdiques

**Qui hi té accés**: Socis amb permís "puede_crear_comandas_esporadicas"

**Funcionalitats**:
- **Crear comandes especials** fora del calendari regular
- **Gestionar demandes puntuals** de productes
- **Coordinar compres** per esdeveniments especials

---

### ⚙️ Master Control

**Qui hi té accés**: Tots els usuaris autenticats

**Funcionalitats**:
- **Registrar compres** manuals de socis
- **Accés a funcions** administratives bàsiques
- **Supervisió general** del sistema

---

## 🔐 Panel d'Administració (Admin Django)

**Accés**: `http://your-server-ip/admin/` (superusuaris només)

### 👥 Gestió d'Usuaris

#### 👤 Socis
- **Crear nous socis** amb informació personal
- **Assignar permisos especials**:
  - `gestiona_productos`: Pot gestionar catàleg
  - `gestiona_stock`: Pot gestionar inventari
  - `puede_crear_comandas_esporadicas`: Pot crear comandes especials
- **Modificar dades** personals i contacte

#### 💰 Comptes i Moneder
- **Gestionar saldos** dels socis
- **Validar ingressos** pendents
- **Revisar historial** de moviments
- **Generar informes** financers

#### 📊 Moviments de Comptes
- **Registres detallats** de transaccions
- **Estats**: Pendent, Validat
- **Tipus**: Ingrés, Egrés, Compra
- **Seguiment temporal** complet

---

### 🛍️ Catàleg de Productes

#### 📂 Categories
- **Organitzar productes** per tipus
- **Gestionar jerarquia** de categories
- **Controlar visibilitat** a la web pública

#### 🛒 Productes
- **Gestió completa** del catàleg
- **Preus i unitats** de venda
- **Imatges i descripcions**
- **Control d'estoc** i disponibilitat
- **Destacats** a la pàgina d'inici

#### 🏪 Proveïdors
- **Informació de contacte** completa
- **Descripcions** i imatges corporatives
- **Visibilitat** a la web pública
- **Gestió de relacions** comercials

---

### 📋 Sistema de Comandes

#### 🔄 Comandes Recurrents
- **Configurar periodicitat**: Setmanal, quinzenal, mensual  
- **Dies d'execució** i horaris
- **Categories i proveïdors** assignats
- **Socis responsables** de la gestió
- **Control d'estat**: Activa, pausada, archivada

#### ⚠️ Consideracions Importants sobre Comandes Recurrents

**Durada de les comandes**:
- Les comandes recurrents **no han de tenir data de finalització**
- Són comandes indefinides que es generen automàticament segons la periodicitat

**Solapament de comandes setmanals**:
- Les comandes setmanals poden tenir **2 dies de solapament**
- Aquest solapament pot fer que **no es vegin totes a la intranet**
- Pot generar confusió entre els socis sobre quines comandes estan disponibles
- **Recomanació**: Revisar calendari d'obertura/tancament per evitar conflictes

#### 📦 Pedidos Col·lectius
- **Seguiment d'estat** complet
- **Dates d'obertura** i tancament
- **Participacions** dels socis
- **Imports totals** i detalls
- **Gestió de lliuraments**

#### 🔧 Propostes de Correcció
- **Revisió de sol·licituds** de canvis
- **Aprovació/rebuig** de modificacions
- **Històrial de decisions**

---

### 📊 Gestió d'Estoc

#### 📥 Registres de Compra
- **Entrades d'inventari**
- **Validació de transaccions**
- **Control de costos**
- **Seguiment temporal**

#### 📈 Moviments d'Estoc
- **Entrades i sortides**
- **Nivells actuals**
- **Històrial de canvis**
- **Alertes de stock mínim**

#### ✅ Sessions de Validació
- **Gestió de recollides**
- **Validació grupal** de compres
- **Control de qualitat**

---

### 💡 Sistema de Desitjos

#### 📝 Cartes de Desitjos
- **Crear noves cartes** temàtiques
- **Definir mínims** necessaris
- **Gestionar estats** i progressió
- **Productes inclosos** en cada carta

#### 🙋 Interessos dels Socis
- **Seguiment de demanda**
- **Quantitats sol·licitades**
- **Anàlisi de viabilitat**
- **Comunicació amb socis**

---

### 🌐 Configuració Web

#### ⚙️ Configuració General
- **Nom de la cooperativa**
- **Informació de contacte**
- **Descripcions institucionals**
- **Configuració de l'API**

#### 🖼️ Galeria d'Imatges
- **Imatges de la cooperativa**
- **Galeria pública** a la web
- **Gestió de contingut** visual

#### 📄 Contingut Públic
- **Pàgines estàtiques**
- **Informació corporativa**
- **Recursos per cooperatives**

---

### 📅 Calendari d'Esdeveniments

#### 🎉 Esdeveniments Cooperatius
- **Dates importants**
- **Esdeveniments especials**
- **Reunions i assemblees**
- **Activitats de la cooperativa**

#### ⏰ Gestió de Dates
- **Calendari visual**
- **Recordatoris automàtics**
- **Sincronització** amb comandes

---

## 📖 Annexos

### 🔑 Glossari de Termes

- **Comanda**: Pedido col·lectiu organitzat per la cooperativa
- **Comanda Recurrent**: Comanda que es repeteix periòdicament
- **Comanda Esporàdica**: Comanda especial fora del calendari regular
- **Moneder**: Sistema de saldo digital per cada soci
- **UF**: Unitat Familiar - identificador del soci
- **Carta de Desitjos**: Proposta de nous productes per avaluar demanda
- **Estoc**: Inventari de productes disponibles per compra immediata

### 👮 Permisos i Rols d'Usuari

**Soci Bàsic**:
- Participar en comandes
- Gestionar moneder personal
- Consultar catàleg i estoc
- Expressar interessos en desitjos

**Gestor de Productes** (`gestiona_productos`):
- + Afegir/editar productes
- + Gestionar catàleg
- + Assignar categories

**Gestor d'Estoc** (`gestiona_stock`):
- + Registrar entrades d'estoc
- + Validar compres
- + Gestionar inventari

**Creador de Comandes Esporàdiques** (`puede_crear_comandas_esporadicas`):
- + Crear comandes especials
- + Gestionar demandes puntuals

**Superusuari/Administrador**:
- Accés total al sistema
- Panel d'administració
- Gestió d'usuaris i permisos
- Configuració del sistema

### 🛠️ Solució de Problemes Comuns

**No puc accedir al sistema**:
- Verifica usuari i contrasenya
- Contacta amb l'administrador
- Comprova la connexió a internet

**El meu saldo no s'actualitza**:
- L'ingrés pot estar pendent de validació
- Comprova l'estat a "Moviments del Moneder"
- Contacta amb l'administrador si cal

**No veig comandes obertes**:
- Pot ser que no hi hagi comandes actives
- Comprova el calendari per dates futures
- Consulta amb els responsables de comandes

**No veig comandes obertes que haurien d'estar disponibles**:
- Comprovar si hi ha solapament entre comandes setmanals
- Les comandes amb dates conflictives poden no mostrar-se correctament
- Revisar el calendari per verificar dates d'obertura/tancament
- Contactar amb l'administrador per revisar la configuració de comandes recurrents

**No puc modificar la meva participació en una comanda**:
- **Estat 🟢 OBERT**: Hauríes de poder modificar - revisa si tens saldo suficient
- **Estat 🟡 PENDENT**: Normal, només gestors poden modificar en aquest estat
- **Estat 🔄 REVISIÓ ACCEPTADA**: Normal, ningú pot modificar
- **Estat ⚫ INACTIU**: Normal, comanda finalitzada
- Si la comanda està oberta i no pots modificar, contacta l'administrador

**No entenc per què no s'ha descomptat el diners de la comanda**:
- El descompte **només** es fa quan la comanda passa a estat ⚫ INACTIU
- En estats 🟢 OBERT, 🟡 PENDENT, 🔄 REVISIÓ: el saldo encara NO es descompta
- Espera a que el gestor finalitzi completament la comanda

**Error en afegir productes a comanda**:
- Verifica que tens saldo suficient per la compra total
- Comprova que la comanda està en estat 🟢 OBERT (no 🟡 PENDENT)
- Revisa les quantitats introduïdes
- Si la comanda diu "oberta" però no pots afegir, pot estar en estat 🟡 PENDENT

### 📞 Contacte i Suport

**Suport Tècnic**:
- Email: [civada@gmail.com](mailto:civada@gmail.com)
- Projecte open source a GitHub

**Administració de la Cooperativa**:
- Contacta amb els responsables designats
- Utilitza els canals de comunicació interns

**Documentació Tècnica**:
- GitHub: [https://github.com/fosc19/coopconsum](https://github.com/fosc19/coopconsum)
- Documentació Docker: `docs/DOCKER_README.md`

### 📚 Recursos Addicionals

- **[Pàgina d'Ajuda Interactiva](/ajuda/)** - Ajuda contextual i navegable dins del sistema
- **[Documentació d'Instal·lació Docker](docs/DOCKER_README.md)** - Guia completa per instal·lar amb Docker

---

*Manual actualitzat per la versió actual de CoopConsum*  
*Per suggeriments de millora, contacta amb l'equip tècnic*