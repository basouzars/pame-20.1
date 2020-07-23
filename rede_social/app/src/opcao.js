import React from 'react';

function Opcao(props) {
    return (
        <div>
            <img src={props.icone} alt=""/>
            <p>{props.nome}</p>
        </div>
    );
};

export default Opcao;