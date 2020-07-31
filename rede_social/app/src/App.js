import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import Home from './Home';
import Nav from './navegacao';
import Post from './Post';

/* imagens */
import fundobranco from './img/fundobranco.jpg';


export default function App() {
  return (
    <Router>
      <div>
        {/*barra de navegação*/}
        <Nav/>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/eletronicos">
            {mostrarItens("eletronicos")}
          </Route>
          <Route path="/videogames">
            {mostrarItens("videogames")}
          </Route>
          <Route path="/jardinagem">
            {mostrarItens("jardinagem")}
          </Route>
          <Route path="/musica">
            {mostrarItens("musica")}
          </Route>
          <Route path="/pets">
            {mostrarItens("pets")}
          </Route>
          <Route path="/roupas">
            {mostrarItens("roupas")}
          </Route>
          {/* página principal */}
          <Route path="/">
            <Home/>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function mostrarItens(categoria) {
  return <div>
  {Object.entries(vendas[categoria]).map(([chave, {nome, descricao, preco, vendedor, foto_vendedor, local, img}]) =>
    <Post
      chave = {chave}
      nome_item = {nome}
      descricao = {descricao}
      preco = {preco}
      vendedor = {vendedor}
      foto_vendedor = {foto_vendedor}
      local = {local}
      imagem = {img}
    />
  )}</div>
}

const vendas = {
  "eletronicos": [
    {
      nome: "(Produto 1)",
      descricao: "(Descrição do produto 1)",
      preco: "XXX",
      vendedor: "user1",
      foto_vendedor: fundobranco,
      local: "Rio de Janeiro",
      img: fundobranco
    },

    {
      nome: "(Produto 2)",
      descricao: "(Descrição do produto 2)",
      preco: "XXX",
      vendedor: "user2",
      foto_vendedor: fundobranco,
      local: "São Paulo",
      img: fundobranco
    },
  ],



  "videogames": [
    {
      nome: "(Produto 1)",
      descricao: "(Descrição do produto 1)",
      preco: "XXX",
      vendedor: "user1",
      foto_vendedor: fundobranco,
      local: "Rio de Janeiro",
      img: fundobranco
    },

    {
      nome: "(Produto 2)",
      descricao: "(Descrição do produto 2)",
      preco: "XXX",
      vendedor: "user2",
      foto_vendedor: fundobranco,
      local: "São Paulo",
      img: fundobranco
    },
  ],



  "jardinagem": [
    {
      nome: "(Produto 1)",
      descricao: "(Descrição do produto 1)",
      preco: "XXX",
      vendedor: "user1",
      foto_vendedor: fundobranco,
      local: "Rio de Janeiro",
      img: fundobranco
    },

    {
      nome: "(Produto 2)",
      descricao: "(Descrição do produto 2)",
      preco: "XXX",
      vendedor: "user2",
      foto_vendedor: fundobranco,
      local: "São Paulo",
      img: fundobranco
    },
  ],
  
  "musica": [
    {
      nome: "(Produto 1)",
      descricao: "(Descrição do produto 1)",
      preco: "XXX",
      vendedor: "user1",
      foto_vendedor: fundobranco,
      local: "Rio de Janeiro",
      img: fundobranco
    },
  ],



  "pets": [
    {
      nome: "(Produto 1)",
      descricao: "(Descrição do Produto 1)",
      preco: "XXX",
      vendedor: "user2",
      foto_vendedor: fundobranco,
      local: "Rio de Janeiro",
      img: fundobranco
    },
  ],



  "roupas": [
    {
      nome: "(Produto 1)",
      descricao: "(Descrição do produto 1)",
      preco: "XXX",
      vendedor: "user1",
      foto_vendedor: fundobranco,
      local: "Rio de Janeiro",
      img: fundobranco
    },
  ]
}