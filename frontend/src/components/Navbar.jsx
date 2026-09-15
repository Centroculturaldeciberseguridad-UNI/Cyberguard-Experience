import {Link, useLocation} from 'react-router-dom';

export default function Navbar({nickname}){
    const location = useLocation();

    return (
        <nav className="navbar">
            <div className="navbar-inner">
                <Link to="/" className="navbar-brand">
                    <span className="brand-icon">&gt;_</span>
                    <span>CyberGuard Experience</span>
                </Link>

                <div className="navbar-links">
                    <Link
                        to="/"
                        className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
                    >
                        Inicio
                    </Link>
                    <Link
                        to="/ranking"
                        className={`nav-link ${location.pathname === '/ranking' ? 'active' : ''}`}
                    >
                        Ranking
                    </Link>
                    {nickname && (
                        <span className="nav-nickname">
                            <span className="nickname-dot" />
                            {nickname}
                        </span>
                    )}
                </div>
            </div>
        </nav>
    );
}