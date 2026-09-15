const MESES = [
  'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
];

function formatFecha(iso) {
  if (!iso) return '';
  const [y, m, d] = iso.split('-');
  return `${parseInt(d)} de ${MESES[parseInt(m) - 1]} de ${y}`;
}

export default function PostModal({ post, profile, onClose }) {
  return (
    <div className="ig-modal-bg" onClick={onClose}>
      <div className="ig-modal" onClick={(e) => e.stopPropagation()}>
        <button className="ig-modal-x" onClick={onClose}>
          &#10005;
        </button>

        {/* Imagen */}
        <div className="ig-modal-img-wrap">
          <img src={post.imagen_url} alt="" className="ig-modal-img" />
        </div>

        {/* Detalles */}
        <div className="ig-modal-side">
          <div className="ig-modal-top">
            <img src={profile.foto_url} alt="" className="ig-modal-av" />
            <span className="ig-modal-user">{profile.username}</span>
          </div>

          <div className="ig-modal-comments">
            {/* Caption */}
            <div className="ig-modal-cmt">
              <span className="ig-modal-cmt-u">{profile.username}</span>
              {post.caption}
            </div>

            {/* Comentarios */}
            {post.comentarios.map((c, i) => (
              <div key={i} className="ig-modal-cmt">
                <span className="ig-modal-cmt-u">{c.usuario}</span>
                {c.texto}
              </div>
            ))}
          </div>

          <div className="ig-modal-foot">
            <div className="ig-modal-likes">&#10084;&#65039; {post.likes} Me gusta</div>
            {post.fecha && (
              <div className="ig-modal-date">{formatFecha(post.fecha)}</div>
            )}
            {post.ubicacion && (
              <div className="ig-modal-loc">&#128205; {post.ubicacion}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}