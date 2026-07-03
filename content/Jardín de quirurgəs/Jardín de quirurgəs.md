---
title: Jardín de quirurgəs
slug: jardin-de-quirurges
estado: simbionte
tags:
  - simbionte
publish: true
origen: simbionte
toot_id: "116847149245628222"
---

![[IMG_20241212_214217894_AE.jpg]]

## Bienvenidə al Jardín de quirurges.

Un espacio de colaboración para compartir referentes, materiales y potencias en torno a la organización social, la labor cultural y los saberes digitales.

> Este no es un proyecto sino una operación en permanente construcción.

---
*Aquí es la bandeja de entrada de todos los aportes desde el Fediverso. Para aportar al semillero basta con usar la etiqueta [#JardinDeQuirurgəs](https://social.anartist.org/tags/JardinDeQuirurg%C9%99s) . Muy recomendable incluir una descripción o comentario al material compartido.*

<div id="mastodon-hashtag"></div>

<script>
(function() {
  const INSTANCE = "social.anartist.org";
  const TAG = "JardinDeQuirurg%C9%99s";
  const container = document.getElementById('mastodon-hashtag');
  if (!container) return;

  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString("es-CO", {
      year: "numeric", month: "long", day: "numeric"
    });
  }

  function sanitizeHTML(str) {
    const div = document.createElement("div");
    div.innerHTML = str;
    return div.innerHTML;
  }

  async function load() {
    container.innerHTML = '<p class="masto-loading">Cargando desde el fediverso...</p>';
    try {
      const res = await fetch(`https://${INSTANCE}/api/v1/timelines/tag/${TAG}?limit=20`);
      if (!res.ok) throw new Error("Error de conexión");
      const toots = await res.json();
      if (!toots.length) {
        container.innerHTML = '<p class="masto-empty">Aún no hay toots con esta etiqueta.</p>';
        return;
      }
      const header = `<p class="masto-invite">Toots con <a href="https://${INSTANCE}/tags/JardinDeQuirurg%C9%99s" target="_blank">#JardinDeQuirurgəs</a> — únete desde cualquier cuenta del fediverso</p>`;
      const items = toots.map(t => `
        <div class="masto-comment">
          <div class="masto-comment-header">
            <img class="masto-avatar" src="${t.account.avatar_static}" alt="${t.account.display_name}" width="40" height="40" loading="lazy">
            <div class="masto-meta">
              <a class="masto-name" href="${t.account.url}" target="_blank">${t.account.display_name}</a>
              <span class="masto-handle">@${t.account.acct}</span>
              <a class="masto-date" href="${t.url}" target="_blank">${formatDate(t.created_at)}</a>
            </div>
          </div>
          <div class="masto-content">${sanitizeHTML(t.content)}</div>
        </div>
      `).join('');
      container.innerHTML = header + items;
    } catch(err) {
      container.innerHTML = `<p class="masto-error">No se pudieron cargar los toots: ${err.message}</p>`;
    }
  }

  load();
})();
</script>
