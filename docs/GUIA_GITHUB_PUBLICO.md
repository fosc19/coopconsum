# 📋 Guia per Crear Repositori Públic a GitHub

## 🎯 Objectiu
Crear un repositori públic a GitHub perquè altres cooperatives puguin usar el nostre codi i contribuir al projecte.

## 📝 Passos a Seguir

### 1. **Preparar el Repositori Local**

#### Netejar arxius sensibles
Abans de fer públic el repositori, assegura't que aquests arxius estiguin a `.gitignore`:
```
# Configuració sensible - NO pujar a producció
coopconsum/settings.py
coopconsum/settings_local.py
coopconsum/settings_production.py
*.env
.env.*
db.sqlite3
media/
```

#### Crear arxius de documentació
- [x] `README.md` - Descripció principal del projecte
- [x] `API_COOPERATIVAS.md` - Documentació de l'API
- [x] `README_API.md` - Estat i exemples de l'API
- [ ] `INSTALL.md` - Guia d'instal·lació pas a pas
- [ ] `CONTRIBUTING.md` - Com contribuir al projecte
- [ ] `LICENSE` - Llicència del projecte (recomanat: MIT)

### 2. **Crear el Repositori a GitHub**

#### Opció A: Des de GitHub Web
1. Ves a [github.com](https://github.com)
2. Fes clic a "New repository"
3. Configura:
   - **Repository name**: `lacivada-cooperativa`
   - **Description**: `Sistema de gestió per cooperatives de consum - Codi obert`
   - **Visibility**: ✅ Public
   - **Initialize**: ❌ No afegir README (ja el tens)
4. Fes clic a "Create repository"

#### Opció B: Des de línia de comandos
```bash
# Al teu directori local
git remote add origin https://github.com/fosc19/lacivada-cooperativa.git
git branch -M main
git push -u origin main
```

### 3. **Configurar el Repositori**

#### Afegir topics/etiquetes
A GitHub, ves a Settings > General > Topics i afegeix:
- `cooperativa`
- `django`
- `python`
- `open-source`
- `cooperative`
- `agroecology`
- `api`

#### Configurar README principal
Crear un `README.md` atractiu amb:
- Logo de la cooperativa
- Descripció del projecte
- Captures de pantalla
- Guia d'instal·lació ràpida
- Enllaços a documentació
- Informació de contacte

#### Configurar Issues i Discussions
- Habilitar Issues per reportar bugs
- Habilitar Discussions per preguntes de la comunitat
- Crear templates per issues

### 4. **Estructura Recomanada del Repositori Públic**

```
lacivada-cooperativa/
├── README.md                    # Descripció principal
├── LICENSE                      # Llicència MIT
├── INSTALL.md                   # Guia d'instal·lació
├── CONTRIBUTING.md              # Guia per contribuir
├── requirements.txt             # Dependències Python
├── docker-compose.yml           # Configuració Docker (futur)
├── .env.example                 # Plantilla de configuració
├── docs/                        # Documentació addicional
│   ├── API_COOPERATIVAS.md
│   ├── README_API.md
│   └── DEPLOYMENT.md
├── scripts/                     # Scripts d'instal·lació
│   ├── install.sh
│   └── setup_database.py
└── [resta del codi Django]
```

### 5. **Contingut del README.md Principal**

```markdown
# 🌱 La Civada - Sistema de Gestió per Cooperatives

> Sistema complet de gestió per cooperatives de consum responsable

## ✨ Característiques

- 👥 **Gestió de Socis**: Comptes, moviments, saldos
- 🛒 **Sistema de Comandes**: Comandes col·lectives i esporàdiques  
- 📦 **Gestió d'Estoc**: Control d'inventari
- 🏪 **Catàleg Web**: Pàgina pública amb productes
- 🤝 **API Pública**: Compartir dades entre cooperatives
- 📅 **Calendari**: Esdeveniments i activitats

## 🚀 Instal·lació Ràpida

```bash
git clone https://github.com/fosc19/lacivada-cooperativa.git
cd lacivada-cooperativa
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📖 Documentació

- [Guia d'Instal·lació](INSTALL.md)
- [API per Cooperatives](docs/API_COOPERATIVAS.md)
- [Com Contribuir](CONTRIBUTING.md)

## 🌐 Demo

- **Web**: https://lacivada.com
- **API**: https://lacivada.com/api/

## 🤝 Comunitat

Tens una cooperativa? Uneix-te a la xarxa!
- Email: cooperatives@lacivada.com
- Issues: Per reportar bugs
- Discussions: Per preguntes i idees

## 📄 Llicència

MIT License - Veure [LICENSE](LICENSE)
```

### 6. **Actualitzar la Pàgina Web**

Un cop creat el repositori, actualitzar l'enllaç a:
- `web/templates/web/cooperatives.html` línia amb `href="#"`
- Canviar per: `href="https://github.com/fosc19/lacivada-cooperativa"`

### 7. **Promoció del Projecte**

#### A xarxes socials
- Anunciar a les xarxes de la cooperativa
- Compartir en grups de cooperatives
- Contactar amb altres cooperatives conegudes

#### A comunitats tècniques
- Publicar en fòrums de Django
- Compartir en comunitats de codi obert
- Presentar en esdeveniments de cooperativisme

## ✅ Checklist Final

- [ ] Repositori creat a GitHub
- [ ] Arxius sensibles a `.gitignore`
- [ ] README.md atractiu creat
- [ ] Documentació completa
- [ ] Enllaços actualitzats a la web
- [ ] Topics/etiquetes configurades
- [ ] Issues i Discussions habilitades
- [ ] Llicència MIT afegida

## 🎉 Llest!

Un cop completats aquests passos, el teu projecte estarà disponible públicament i altres cooperatives podran:
- Descarregar i usar el codi
- Contribuir amb millores
- Reportar bugs
- Fer preguntes
- Crear una xarxa de cooperatives col·laboratives

---

**Necessites ajuda?** Contacta amb l'equip tècnic de La Civada.