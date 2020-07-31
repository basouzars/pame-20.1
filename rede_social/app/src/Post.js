import React from 'react';

function Post(props) {
    return (
    <div key={props.chave} className="container-post">
        <div>
            <img src={props.imagem} alt=""/>
        </div>
        <div className="info">
            <p className="nome-item">{props.nome_item}</p>
            <p>{props.descricao}</p>
            <p className="preco">R$ {props.preco}</p>
        </div>



        <div className="compra">
            <div className="user-info-container">
                <div>
                    <img src={props.foto_vendedor} alt=""/>
                </div>
                <div>
                    <p className="nome-vendedor">{props.vendedor}</p>
                    <p>{props.local}</p>
                </div>
            </div>
            <div className="botoes-compra">
                <button className="botao-msg" type="button">Mensagem</button>
                <button className="botao-comp" type="button">Comprar</button>
            </div>
        </div>
    </div>
    );
};

export default Post;