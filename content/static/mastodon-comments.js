// Mastodon comments for Quartz
// Coloca este archivo en: content/static/mastodon-comments.js

(function () {
  const INSTANCE = "social.anartist.org";

  function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString("es-CO", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  function sanitizeHTML(str) {
    const div = document.createElement("div");
    div.innerHTML = str;
    // Permitir solo p, br, a, em, strong
    const allowed = ["P", "BR", "A", "EM", "STRONG", "SPAN"];
    div.querySelectorAll("*").forEach((el) => {
      if (!allowed.includes(el.tagName)) {
        el.replaceWith(...el.childNodes);
      }
    });
    return div.innerHTML;
  }

  function buildComment(reply) {
    const avatar = reply.account.avatar_static || "";
    const displayName = reply.account.display_name || reply.account.username;
    const username = reply.account.acct;
    const url = reply.url;
    const date = formatDate(reply.created_at);
    const content = sanitizeHTML(reply.content);

    return `
      <div class="masto-comment">
        <div class="masto-comment-header">
          <img class="masto-avatar" src="${avatar}" alt="${displayName}" width="40" height="40" loading="lazy">
          <div class="masto-meta">
            <a class="masto-name" href="https://${INSTANCE}/@${username}" target="_blank" rel="noopener">${displayName}</a>
            <span class="masto-handle">@${username}</span>
            <a class="masto-date" href="${url}" target="_blank" rel="noopener">${date}</a>
          </div>
        </div>
        <div class="masto-content">${content}</div>
      </div>
    `;
  }

  async function loadComments(statusId, container) {
    container.innerHTML = `<p class="masto-loading">Cargando comentarios...</p>`;

    try {
      const response = await fetch(
        `https://${INSTANCE}/api/v1/statuses/${statusId}/context`
      );

      if (!response.ok) throw new Error("No se pudo conectar con el fediverso.");

      const data = await response.json();
      const replies = data.descendants || [];

      if (replies.length === 0) {
        container.innerHTML = `
          <p class="masto-empty">
            Aún no hay comentarios. 
            <a href="https://${INSTANCE}/interact/${statusId}" target="_blank" rel="noopener">
              Responde desde el fediverso
            </a>
          </p>`;
        return;
      }

      const header = `
        <p class="masto-invite">
          Comenta desde cualquier cuenta del fediverso —
          <a href="https://${INSTANCE}/interact/${statusId}" target="_blank" rel="noopener">
            responde a este toot
          </a>
        </p>`;

      const comments = replies.map(buildComment).join("");
      container.innerHTML = header + comments;
    } catch (err) {
      container.innerHTML = `<p class="masto-error">No se pudieron cargar los comentarios: ${err.message}</p>`;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("mastodon-comments");
    if (!container) return;

    const statusId = container.dataset.statusId;
    if (!statusId) return;

    loadComments(statusId, container);
  });
})();
