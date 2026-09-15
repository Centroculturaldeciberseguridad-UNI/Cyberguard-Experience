import { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Reto1Pagina from './pages/Reto1_Password_AlvaroCa/Reto1Pagina';
import Reto2Pagina from './pages/Reto2_Phishing_MartinBe/Reto2Pagina';
import Reto3Pagina from './pages/Reto3_OSINT_ReginaVi/Reto3Pagina';
import ResultadoFinal from './pages/ResultadoFinal';
import RankingPagina from './pages/RankingPagina';

function App() {
    const [nickname, setNickname] = useState(() => {
        return localStorage.getItem('nickname') || '';
    });

    useEffect(() => {
        if (nickname) {
            localStorage.setItem('nickname', nickname);
        } else {
            localStorage.removeItem('nickname');
        }
    }, [nickname]);

    return (
        <div className="app">
            <Navbar nickname={nickname} />
            <Routes>
                <Route path="/" element={<Home nickname={nickname} setNickname={setNickname} />} />
                <Route path="/ranking" element={<RankingPagina />} />
                <Route path="/reto1" element={<Reto1Pagina nickname={nickname} setNickname={setNickname} />} />
                <Route path="/reto2" element={<Reto2Pagina nickname={nickname} setNickname={setNickname} />} />
                <Route path="/reto3" element={<Reto3Pagina nickname={nickname} setNickname={setNickname} />} />
                <Route path="/resultado" element={<ResultadoFinal nickname={nickname} setNickname={setNickname} />} />
            </Routes>
        </div>
    );
}

export default App;
