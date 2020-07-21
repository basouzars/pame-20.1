import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import Home from './Home'
import Nav from './navegacao'
import Post from './Post'

/* imagens */
import oculos from './img/oculos.jpg';

export default function App() {
  return (
    <Router>
      <div>
        {/*barra de navegacao*/}
        <Nav/>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/eletronicos">
            <Post
              nome_usuario="vendas"
              descricao="vendo"
              imagem={vendas["venda1"].img}
            />
          </Route>
          <Route path="/videogames">

          </Route>
          <Route path="/jardinagem">

          </Route>
          <Route path="/musica">

          </Route>
          <Route path="/pets">

          </Route>
          <Route path="/roupas">

          </Route>
          {/* pagina principal */}
          <Route path="/">
            <Home/>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

const vendas = {
  "venda1": {
    nome: "venda de produto",
    descricao: "ultima geração",
    img: oculos
  }
}