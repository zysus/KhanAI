# 🎨 Khan AI - Assets e Imágenes

## Carpeta: `app/templates/img/`

Esta carpeta debe contener los siguientes assets visuales para Khan AI.

---

## 📋 Archivos Necesarios

### 1. Favicon
**Nombre:** `favicon.ico`
**Tamaño:** 16x16, 32x32, 48x48 px
**Descripción:** Icono que aparece en la pestaña del navegador

**Sugerencia de diseño:**
- Color: Cyan (#00ffff) sobre fondo oscuro
- Símbolo: Letra "K" estilizada o símbolo cuántico
- Estilo: Futurista, minimalista

### 2. Logo Principal
**Nombre:** `logo.png`
**Tamaño:** 512x512 px (PNG transparente)
**Descripción:** Logo de Khan AI para la aplicación

**Sugerencia de diseño:**
- Letra "K" grande con efecto de neón cyan
- Elementos geométricos (hexágonos, circuitos)
- Efecto de glow/resplandor
- Fondo transparente

### 3. Logo Pequeño
**Nombre:** `logo-small.png`
**Tamaño:** 128x128 px
**Descripción:** Versión pequeña para sidebar

---

## 🎨 Paleta de Colores Khan AI

```css
Cyan Principal:    #00ffff
Magenta Secundario: #ff00ff
Verde Acento:      #00ff00
Rojo Peligro:      #ff0055
Azul Oscuro:       #0a0e27
```

---

## 🖼️ Crear Logo SVG (Opcional)

Si prefieres un logo SVG para mejor escalabilidad:

**Nombre:** `logo.svg`

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Hexágono de fondo -->
  <polygon 
    points="100,20 170,60 170,140 100,180 30,140 30,60" 
    fill="none" 
    stroke="#00ffff" 
    stroke-width="2"
    opacity="0.3"
  />
  
  <!-- Letra K estilizada -->
  <text 
    x="100" 
    y="130" 
    font-family="Arial, sans-serif" 
    font-size="100" 
    font-weight="bold" 
    fill="#00ffff" 
    text-anchor="middle"
    filter="url(#glow)"
  >K</text>
  
  <!-- Líneas decorativas -->
  <line x1="100" y1="20" x2="100" y2="50" stroke="#00ff00" stroke-width="2"/>
  <line x1="100" y1="150" x2="100" y2="180" stroke="#00ff00" stroke-width="2"/>
</svg>
```

---

## 🎯 Placeholder mientras creas los logos

### Opción 1: Usar texto como logo (CSS)
Ya está implementado en el HTML actual con la clase `.khan-logo`

### Opción 2: Generadores online
Puedes usar estos servicios gratuitos:
- **Canva** (https://canva.com) - Plantillas de logos
- **LogoMakr** (https://logomakr.com) - Editor simple
- **Figma** (https://figma.com) - Diseño profesional

---

## 📸 Screenshots Sugeridos

Para documentación, podrías crear:

**Nombre:** `screenshot-login.png`
**Descripción:** Captura de la pantalla de login

**Nombre:** `screenshot-dashboard.png`
**Descripción:** Captura del dashboard principal

**Nombre:** `screenshot-admin.png`
**Descripción:** Captura del panel de admin

---

## 🎨 Iconos Adicionales (Opcional)

Si quieres mejorar la interfaz:

```
app/templates/img/icons/
├── chat.svg       (Icono de chat)
├── settings.svg   (Icono de configuración)
├── history.svg    (Icono de historial)
├── user.svg       (Icono de usuario)
└── logout.svg     (Icono de salir)
```

---

## 🔧 Integrar los Assets

### En HTML (login.html, index.html, admin.html):

```html
<!-- Favicon -->
<link rel="icon" type="image/x-icon" href="/img/favicon.ico">

<!-- Logo en login -->
<img src="/img/logo.png" alt="Khan AI Logo" class="login-logo">

<!-- Logo en sidebar -->
<img src="/img/logo-small.png" alt="Khan" class="sidebar-logo">
```

### En CSS:

```css
.login-logo {
    width: 150px;
    height: 150px;
    margin-bottom: 2rem;
    filter: drop-shadow(0 0 20px var(--primary));
}

.sidebar-logo {
    width: 40px;
    height: 40px;
}
```

---

## 💡 Nota Importante

**Khan AI funciona perfectamente sin imágenes personalizadas.** Los logos actuales están implementados con CSS y texto, lo cual es completamente funcional.

Solo necesitas crear estos assets si quieres personalizar aún más la apariencia.

---

## 🎨 Recursos de Diseño Gratuitos

- **Unsplash** - Fondos abstractos cyber
- **Flaticon** - Iconos tech gratuitos
- **FontAwesome** - Iconos web
- **Google Fonts** - Fuentes modernas

---

**Creado por zysus para Khan AI v4.0**