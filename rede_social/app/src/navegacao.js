import React from 'react';
import { Link } from "react-router-dom";

// logo e icones
import logo from './img/icons/sell.svg'
import user_icon from './img/icons/user.svg';

function Nav(props) {
    return (
    <div className="nav">
        <Link to="/"><img className="logo" src={logo} width="50px" height="50px"/></Link>
        <input type="text" placeholder="Pesquisar"/>

        <div className="nav-direita">
            <a href="#"><img className="usuario" src={user_icon} width="30px" height="30px"/></a>
        </div>
    </div>
    );
};

export default Nav;