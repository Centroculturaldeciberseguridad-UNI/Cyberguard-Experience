const API_URL = import.meta.env.VITE_API_URL || '';

async function apiFetch(endpoint, options = {}) {
    const url = `${API_URL}${endpoint}`;
    const config = {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    };

    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
        const mensaje =
            typeof data.detail === 'string'
                ? data.detail
                : Array.isArray(data.detail)
                    ? data.detail.map((d) => d.msg).join('. ')
                    : 'Error en la solicitud';
        const error = new Error(mensaje);
        error.status = response.status;
        error.data = data;
        throw error;
    }

    return data;
}

export const api = {
  /* Usuarios */
  registrarNickname: (nickname) =>
    apiFetch('/usuarios/registro', {
      method: 'POST',
      body: JSON.stringify({ nickname }),
    }),

  obtenerUsuario: (nickname) =>
    apiFetch(`/usuarios/${nickname}`),

  /* Ranking */
  obtenerRanking: (top = 10) =>
    apiFetch(`/ranking?top=${top}`),
  obtenerPosicion: (nickname) =>
    apiFetch(`/ranking/posicion/${nickname}`),
  obtenerEstadoRetos: (nickname) =>
    apiFetch(`/ranking/estado-retos/${nickname}`),

  /* Reto 1 - Fuerza Bruta / Contraseñas */
  evaluarPassword: (nickname, password) =>
    apiFetch('/reto1/evaluar', {
      method: 'POST',
      body: JSON.stringify({ nickname, password }),
    }),

  completarReto1: (nickname, puntos = null) =>
    apiFetch('/reto1/completar', {
      method: 'POST',
      body: JSON.stringify({ nickname, puntos }),
    }),
  
  /* Reto 2 - Phishing Detective */
  iniciarReto2: (nickname) =>
    apiFetch('/reto2/session', {
      method: 'POST',
      body: JSON.stringify({ nickname }),
    }),

  obtenerCasoActualReto2: (nickname) =>
    apiFetch(`/reto2/current/${nickname}`),

  pedirPistaReto2: (nickname) =>
    apiFetch('/reto2/hint', {
      method: 'POST',
      body: JSON.stringify({ nickname }),
    }),

  enviarRespuestaReto2: (nickname, user_answer) =>
    apiFetch('/reto2/answer', {
      method: 'POST',
      body: JSON.stringify({ nickname, user_answer }),
    }),

  obtenerResultadoReto2: (nickname) =>
    apiFetch(`/reto2/result/${nickname}`),

  completarReto2: (nickname, puntos = null) =>
    apiFetch('/reto2/completar', {
      method: 'POST',
      body: JSON.stringify({ nickname, puntos }),
    }),

  /* Reto 3 — Perfiles del sandbox */
  obtenerPerfilMarco: () => apiFetch('/reto3/perfil/marco'),
  obtenerPerfilCarlos: () => apiFetch('/reto3/perfil/carlos'),
  obtenerPerfilNexova: () => apiFetch('/reto3/perfil/nexova'),
  obtenerPerfilCamila: () => apiFetch('/reto3/perfil/camila'),

  /* Reto 3 — Pistas (solo preguntas) */
  obtenerPistas: () => apiFetch('/reto3/pistas'),

  /* Reto 3 — Hallazgos */
  enviarHallazgo: (nickname, clave, valor) =>
    apiFetch('/reto3/hallazgo', {
      method: 'POST',
      body: JSON.stringify({ nickname, clave, valor }),
    }),

  /* Reto 3 — Pista pagada */
  obtenerInfoPistaPagada: (clave) =>
    apiFetch(`/reto3/pista-pagada/${clave}`),

  usarPistaPagada: (nickname, clave, valor) =>
    apiFetch('/reto3/pista-pagada', {
      method: 'POST',
      body: JSON.stringify({ nickname, clave, valor }),
    }),

  /* Reto 3 — Contraseña corporativa */
  intentarPassword: (nickname, password) =>
    apiFetch('/reto3/password', {
      method: 'POST',
      body: JSON.stringify({ nickname, password }),
    }),

  /* Reto 3 - Control de tiempo */
  iniciarReto3: (nickname) =>
    apiFetch('/reto3/iniciar', {
      method: 'POST',
      body: JSON.stringify({ nickname }),
    }),

  finalizarReto3: (nickname) =>
    apiFetch('/reto3/finalizar', {
      method: 'POST',
      body: JSON.stringify({ nickname }),
    }),

  /* Reto 3 — Progreso */
  obtenerProgreso: (nickname) =>
    apiFetch(`/reto3/progreso/${nickname}`),
};