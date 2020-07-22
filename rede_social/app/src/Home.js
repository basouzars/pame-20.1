import React from 'react';
import { Link } from 'react-router-dom';

import Opcao from './opcao';

/* icones */
import computador from './img/icons/computer.svg';
import jogos from './img/icons/fun.svg';
import jardinagem from './img/icons/garden.svg';
import instrumentos from './img/icons/guitar.svg';
import animais from './img/icons/pet.svg';
import roupas from './img/icons/tshirt.svg';

function Home() {
    return (
        <div className="App">
          {/* icones de compra */}
          <div className="container">
            <Link to="/eletronicos"><Opcao nome={"Eletrônicos"} icone={computador}/></Link>
            <Link to="/videogames"><Opcao nome={"Brinquedos"} icone={jogos}/></Link>
            <Link to="/jardinagem"><Opcao nome={"Jardinagem"} icone={jardinagem}/></Link>
            <Link to="/musica"><Opcao nome={"Instrumentos"} icone={instrumentos}/></Link>
            <Link to="/pets"><Opcao nome={"Pets"} icone={animais}/></Link>
            <Link to="/roupas"><Opcao nome={"Vestuário"} icone={roupas}/></Link>
          </div>
        </div>
    );
};

export default Home;