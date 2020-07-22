import React from 'react';
// icones
import icoracao from './img/coracao.svg';
import icomente from './img/comente.svg';
import iorigami from './img/origami.svg';

function Post(props) {
    return (
    <div className="postagem">
        <img src={props.imagem}/>

        <div class="info-post">
            {/*icones*/}
            <p>
                <img src={icoracao}/>
                <img src={icomente}/>
                <img src={iorigami}/>
            </p>
            <p><a href="#">{props.nome_usuario} </a>{props.descricao}</p>
            <p><input type="text" placeholder="Adicionar um comentário..."/><button type="button">Enviar</button></p>
        </div>
    </div>
    );
};

export default Post;