# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Pessoas sem experiência prévia em modelagem, estudantes de graduação, pesquisadores e profissionais que queiram compreender ou operar uma simulação do 3-PG.

## Product Purpose

Oferecer uma aplicação web interativa do 3-PG para divulgação científica. A pessoa usuária manipula variáveis e cenários e recebe explicações visuais, acessíveis e ligadas aos processos ecofisiológicos que ajudam a interpretar a resposta simulada da floresta.

## Positioning

A aplicação aproxima execução e compreensão: permite explorar uma simulação e acompanhar o fluxo matemático e ecofisiológico que a produz, em vez de apresentar apenas parâmetros ou resultados isolados.

## Operating Context

A experiência oferece um Modo Aprender, “Como uma floresta cresce?”, e um Modo Científico, com parâmetros completos do 3-PG para estudantes, pesquisadores e profissionais. O simulador baseia-se no 3-PG original; a desfolha é uma extensão opcional, separada do fluxo original e acessível como módulo próprio.

## Capabilities and Constraints

- A plataforma existente executa o 3-PGpjs no navegador e apresenta cenários, parâmetros, resultados e conteúdo explicativo.
- O mecanismo científico deve permanecer inalterado nesta evolução de interface.
- O mapa mental deve representar o fluxo conectado da simulação, incluindo o ciclo mensal e suas entradas, processos, estados e saídas.
- A desfolha não deve ser ativada nem apresentada como parte do núcleo original do 3-PG.
- Alegações, equações, parâmetros e resultados devem permanecer rastreáveis às fontes e aos registros existentes; ausência de evidência deve permanecer explícita.

## Brand Commitments

O nome do produto é Akademia Florestal. A interface e as explicações são em português do Brasil, com linguagem acessível sem apagar a precisão científica.

## Evidence on Hand

O repositório contém a aplicação web em `plataforma/`, o motor 3-PGpjs, o módulo de desfolha como extensão separada, registros de equações e fontes, além de testes e dados de cenários usados pela plataforma.

## Product Principles

- Começar pelo 3-PG original e manter suas extensões claramente identificadas.
- Ligar explicações ao cenário, ao processo executado e à resposta simulada.
- Tornar o conteúdo compreensível a iniciantes sem limitar o modo científico.
- Distinguir resultados de simulação de evidência empírica.
- Preservar a rastreabilidade e não preencher lacunas de evidência com suposições.

## Accessibility & Inclusion

As explicações devem ser compreensíveis para pessoas sem experiência em modelagem; a informação científica deve continuar disponível para quem precisa de parâmetros e detalhes completos.
