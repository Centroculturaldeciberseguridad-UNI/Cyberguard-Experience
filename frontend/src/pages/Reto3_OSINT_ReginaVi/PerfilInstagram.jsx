import { useState, useEffect } from 'react';
import PostModal from './PostModal';
import './PerfilInstagram.css';

export default function PerfilInstagram({ profile, onNavigate }) {
  const [selectedPost, setSelectedPost] = useState(null);
  const [showSiguiendo, setShowSiguiendo] = useState(false);
  const [activeTab, setActiveTab] = useState('posts');
  const [viewingStory, setViewingStory] = useState(null);
  const [storyIndex, setStoryIndex] = useState(0);

  /* Reset al cambiar de perfil */
  useEffect(() => {
    setSelectedPost(null);
    setShowSiguiendo(false);
    setActiveTab('posts');
    setViewingStory(null);
    setStoryIndex(0);
  }, [profile]);

  if (!profile) return null;

  /* ── Stories ──────────────────────────────────────────── */

  const openStory = (highlight) => {
    setViewingStory(highlight);
    setStoryIndex(0);
  };

  const navStory = (dir) => {
    if (!viewingStory) return;
    const total = viewingStory.stories.length;
    if (dir === 'next') {
      if (storyIndex < total - 1) setStoryIndex((i) => i + 1);
      else setViewingStory(null);
    } else {
      if (storyIndex > 0) setStoryIndex((i) => i - 1);
    }
  };

  /* ── Render ───────────────────────────────────────────── */

  return (
    <div className="ig">
      {/* ─── Header ─────────────────────────────────────── */}
      <div className="ig-header">
        <div className="ig-avatar-wrap">
          <img src={profile.foto_url} alt={profile.nombre} className="ig-avatar" />
        </div>
        <div className="ig-header-info">
          <h2 className="ig-username">{profile.username}</h2>
          <div className="ig-stats">
            <span className="ig-stat">
              <strong>{profile.publicaciones}</strong> publicaciones
            </span>
            <span className="ig-stat">
              <strong>{profile.seguidores}</strong> seguidores
            </span>
            <span
              className="ig-stat ig-stat-link"
              onClick={() => setShowSiguiendo(true)}
              role="button"
              tabIndex={0}
            >
              <strong>{profile.siguiendo.length}</strong> siguiendo
            </span>
          </div>
          <div className="ig-bio">
            <p className="ig-bio-name">{profile.nombre}</p>
            <p className="ig-bio-text">{profile.bio}</p>
          </div>
        </div>
      </div>

      {/* ─── Historias destacadas ───────────────────────── */}
      {profile.historias_destacadas?.length > 0 && (
        <div className="ig-highlights">
          {profile.historias_destacadas.map((hl) => (
            <div
              key={hl.id}
              className="ig-hl"
              onClick={() => openStory(hl)}
              role="button"
              tabIndex={0}
            >
              <div className="ig-hl-ring">
                <img src={hl.portada_url} alt={hl.titulo} className="ig-hl-img" />
              </div>
              <span className="ig-hl-label">{hl.titulo}</span>
            </div>
          ))}
        </div>
      )}

      {/* ─── Tabs ───────────────────────────────────────── */}
      <div className="ig-tabs">
        <button
          className={`ig-tab ${activeTab === 'posts' ? 'ig-tab-on' : ''}`}
          onClick={() => setActiveTab('posts')}
        >
          Publicaciones
        </button>
        <button
          className={`ig-tab ${activeTab === 'reels' ? 'ig-tab-on' : ''}`}
          onClick={() => setActiveTab('reels')}
        >
          Reels
        </button>
      </div>

      {/* ─── Grid de posts ──────────────────────────────── */}
      {activeTab === 'posts' && (
        <div className="ig-grid">
          {profile.posts.map((post) => (
            <div
              key={post.id}
              className="ig-cell"
              onClick={() => setSelectedPost(post)}
              role="button"
              tabIndex={0}
            >
              <img src={post.imagen_url} alt="" className="ig-cell-img" />
              <div className="ig-cell-overlay">
                <span>&#10084;&#65039; {post.likes}</span>
                <span>&#128172; {post.comentarios.length}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ─── Grid de reels ──────────────────────────────── */}
      {activeTab === 'reels' && (
        <div className="ig-reels">
          {profile.reels.map((reel) => (
            <div key={reel.id} className="ig-reel">
              <img src={reel.miniatura_url} alt={reel.titulo} className="ig-reel-img" />
              <div className="ig-reel-foot">
                <span className="ig-reel-title">{reel.titulo}</span>
                <span className="ig-reel-meta">
                  {reel.duracion} &middot; {reel.likes} likes
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ─── Modal de post ──────────────────────────────── */}
      {selectedPost && (
        <PostModal
          post={selectedPost}
          profile={profile}
          onClose={() => setSelectedPost(null)}
        />
      )}

      {/* ─── Visor de historias ─────────────────────────── */}
      {viewingStory && (
        <div className="ig-story-bg" onClick={() => setViewingStory(null)}>
          <div className="ig-story" onClick={(e) => e.stopPropagation()}>
            {/* Barras de progreso */}
            <div className="ig-story-bars">
              {viewingStory.stories.map((_, i) => (
                <div
                  key={i}
                  className={`ig-story-bar ${i <= storyIndex ? 'ig-story-bar-on' : ''}`}
                />
              ))}
            </div>

            <button className="ig-story-x" onClick={() => setViewingStory(null)}>
              &#10005;
            </button>

            {/* Zonas clickeables izq / der */}
            <div className="ig-story-tap ig-story-tap-l" onClick={() => navStory('prev')} />
            <div className="ig-story-tap ig-story-tap-r" onClick={() => navStory('next')} />

            <img
              src={viewingStory.stories[storyIndex].imagen_url}
              alt=""
              className="ig-story-img"
            />

            {viewingStory.stories[storyIndex].texto && (
              <p className="ig-story-txt">{viewingStory.stories[storyIndex].texto}</p>
            )}
          </div>
        </div>
      )}

      {/* ─── Panel de Siguiendo ─────────────────────────── */}
      {showSiguiendo && (
        <div className="ig-sig-bg" onClick={() => setShowSiguiendo(false)}>
          <div className="ig-sig" onClick={(e) => e.stopPropagation()}>
            <div className="ig-sig-head">
              <h3>Siguiendo</h3>
              <button className="ig-sig-x" onClick={() => setShowSiguiendo(false)}>
                &#10005;
              </button>
            </div>
            <div className="ig-sig-list">
              {profile.siguiendo.map((s, i) => (
                <div
                  key={i}
                  className={`ig-sig-item ${s.id ? 'ig-sig-nav' : ''}`}
                  onClick={() => {
                    if (s.id) {
                      onNavigate(s.id);
                      setShowSiguiendo(false);
                    }
                  }}
                >
                  <img src={s.foto_url} alt={s.nombre} className="ig-sig-av" />
                  <div className="ig-sig-info">
                    <span className="ig-sig-user">{s.username}</span>
                    <span className="ig-sig-name">{s.nombre}</span>
                  </div>
                  {s.id && <span className="ig-sig-arrow">&rsaquo;</span>}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}