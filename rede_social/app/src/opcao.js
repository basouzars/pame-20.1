import React from 'react';

function Opcao(props) {
    return (
        <div>
            <img src={props.icone}/>
            <p>{props.nome}</p>
        </div>
    );
};

export default Opcao;