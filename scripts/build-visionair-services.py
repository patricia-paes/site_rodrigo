#!/usr/bin/env python3
"""Generate the five editorial service pages without a runtime/build dependency."""
from pathlib import Path
from html import escape
import json
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://rodrigovictor.com.br'
SERVICES = [
    {
        'slug': 'filmagem-drone-imoveis', 'label': 'Imobiliário',
        'title': 'Filmagem com Drone para Imóveis no Rio de Janeiro | VISIONAIR',
        'heading': 'Filmagem com drone para imóveis no Rio de Janeiro.',
        'description': 'Apresente imóveis, terrenos e empreendimentos com filmagem e fotografia aérea no Rio de Janeiro. Conheça a produção da VISIONAIR e solicite orçamento.',
        'lead': 'Mostre o imóvel por inteiro: arquitetura, áreas externas e a relação com o entorno. Imagens aéreas ajudam o público a entender o espaço antes de uma visita.',
        'image': 'imovel-real.webp', 'alt': 'Vista aérea de uma residência com piscina em Vilamoura, Portugal, em fotografia de referência.',
        'intro_title': 'Uma apresentação que coloca o imóvel em contexto.',
        'intro': 'Para corretores, imobiliárias e proprietários, a captação com drone permite apresentar a implantação de uma casa, a área de lazer de um condomínio ou a dimensão visual de um terreno. A VISIONAIR planeja os enquadramentos conforme o que precisa ser mostrado e o canal em que o material será utilizado.',
        'uses': [('Casas e empreendimentos', 'Fachadas, acessos e áreas externas, com uma sequência que ajuda a compreender a distribuição dos espaços.'), ('Terrenos e entorno', 'Visão geral da área e de suas relações com a paisagem, sem substituir levantamento topográfico ou medição de limites.'), ('Anúncios e apresentações', 'Imagens para páginas de imóveis, redes sociais e apresentações comerciais, nos formatos definidos no orçamento.')],
        'planning': 'Informe o endereço do imóvel, as áreas prioritárias e o responsável pela liberação de acesso. Em condomínios, alinhe previamente as condições de entrada e captação. A análise considera obstáculos, circulação de pessoas, privacidade dos vizinhos e condições de operação no local.',
        'delivery': 'A proposta pode reunir fotografias aéreas, cenas captadas ou vídeo editado. Quantidade de imagens, duração, orientação vertical ou horizontal, trilha e aplicação de marca são combinadas antes da produção. Se precisar de arquivos brutos ou de mais de uma versão, inclua essa necessidade no briefing.',
        'questions': [('A captação inclui o interior do imóvel?', 'Esta página trata da captação aérea. Filmagem interna, imagens em solo e outros complementos precisam ser avaliados e descritos na proposta.'), ('O drone comprova a metragem do terreno?', 'Não. As imagens têm finalidade de apresentação audiovisual. Medições, demarcações e laudos técnicos não fazem parte deste serviço.'), ('Posso receber versões para anúncios e redes sociais?', 'Sim, esses usos podem orientar a produção. Informe os canais e formatos desejados para definir as versões e a edição no orçamento.')],
        'brief': 'Endereço, tipo de imóvel, áreas que precisam aparecer, canais de divulgação e data desejada.'
    },
    {
        'slug': 'filmagem-aerea-arquitetura-obras', 'label': 'Arquitetura e construção',
        'title': 'Filmagem Aérea de Obras e Arquitetura no Rio | VISIONAIR',
        'heading': 'Filmagem aérea para arquitetura e obras no Rio de Janeiro.',
        'description': 'Registre arquitetura, canteiros e etapas de obras com imagens aéreas no Rio de Janeiro. Planejamento de captação e edição conforme o projeto. VISIONAIR.',
        'lead': 'Dê visibilidade à escala de um projeto e registre suas transformações. Captação aérea para apresentar arquitetura, documentar etapas e comunicar a evolução de uma obra.',
        'image': 'obra-real.webp', 'alt': 'Canteiro de obras com guindaste visto do alto, em fotografia de referência.',
        'intro_title': 'Da implantação à obra concluída.',
        'intro': 'Um projeto arquitetônico ganha contexto quando se vê sua relação com o terreno, o entorno e os volumes construídos. Na obra, registros em datas diferentes ajudam a contar a evolução visual das etapas. A VISIONAIR organiza a captação a partir dos pontos que a equipe deseja documentar e comunicar.',
        'uses': [('Arquitetura e implantação', 'Enquadramentos que apresentam volumes, acessos e a integração do projeto à paisagem.'), ('Etapas de construção', 'Registros audiovisuais das fases previstas no briefing, em visitas pontuais ou em uma sequência de captações contratadas.'), ('Comunicação do projeto', 'Material para apresentações, relatórios visuais, redes sociais e comunicação com clientes e parceiros.')],
        'planning': 'A produção precisa ser coordenada com o responsável pelo canteiro. Informe horários de atividade, circulação de máquinas, guindastes, áreas restritas e regras de acesso. Para visitas recorrentes, datas e pontos de referência são combinados para favorecer a comparação visual, sempre sujeitos à viabilidade de cada operação.',
        'delivery': 'Podem ser planejadas fotografias por etapa, cenas selecionadas e vídeos editados. A frequência das visitas, a identificação das datas, as versões e o prazo de cada entrega ficam descritos na proposta. A contratação audiovisual não inclui inspeção com laudo, diagnóstico de engenharia ou levantamento topográfico.',
        'questions': [('É possível contratar registros em mais de uma etapa?', 'Sim. O orçamento pode prever visitas em datas ou marcos da obra, com escopo e entrega definidos para cada captação.'), ('As imagens substituem uma inspeção técnica?', 'Não. O serviço registra e apresenta visualmente o projeto; não emite parecer de engenharia, certificação ou laudo de segurança.'), ('O que acontece se a obra mudar o cronograma?', 'Comunique a alteração para revisar a disponibilidade e as condições de reagendamento previstas na proposta. A nova data depende de agenda e viabilidade operacional.')],
        'brief': 'Endereço, etapa da obra, responsável pelo acesso, número de visitas, cronograma e finalidade das imagens.'
    },
    {
        'slug': 'filmagem-eventos-drone', 'label': 'Eventos',
        'title': 'Filmagem de Eventos com Drone no Rio de Janeiro | VISIONAIR',
        'heading': 'Filmagem de eventos com drone no Rio de Janeiro.',
        'description': 'Imagens aéreas para eventos sociais, corporativos e esportivos no Rio de Janeiro. Consulte a viabilidade da captação e peça uma proposta à VISIONAIR.',
        'lead': 'Apresente o cenário, a estrutura e a atmosfera do seu evento por um novo ponto de vista. Uma produção planejada para complementar a narrativa dos momentos importantes.',
        'image': 'evento-real.webp', 'alt': 'Recepção ao ar livre em Acapulco, México, em fotografia de referência.',
        'intro_title': 'O cenário também faz parte da história.',
        'intro': 'As imagens aéreas podem situar o público, apresentar o espaço e criar transições para o filme de um evento. Em encontros sociais, ações corporativas ou atividades esportivas, o roteiro precisa respeitar a programação e as condições reais do local. A VISIONAIR avalia o que é possível captar antes de confirmar a proposta.',
        'uses': [('Eventos sociais', 'Apresentação do ambiente e cenas externas que complementam o registro da ocasião.'), ('Encontros corporativos', 'Imagens do espaço e da estrutura para comunicação institucional e divulgação do evento.'), ('Eventos esportivos', 'Planos do cenário e de áreas viáveis para captação, definidos com a organização e sujeitos à análise operacional.')],
        'planning': 'Compartilhe endereço, data, programação e previsão de circulação de pessoas. A área de operação e os horários de captação precisam ser alinhados com a organização. A contratação não pressupõe sobrevoo de público, cobertura de todas as atividades ou autorização de voo em qualquer ponto do evento.',
        'delivery': 'O material pode ser entregue como cenas para a equipe de edição do evento ou como um vídeo final, quando contratado. Duração, formatos, trilha, inserção de identidade visual e prazo são definidos na proposta. Para momentos que não podem ser repetidos, alinhe também alternativas de cobertura com a organização.',
        'questions': [('É possível voar durante todo o evento?', 'Não há promessa de voo contínuo. A operação depende de condições do local, segurança, clima, autonomia do equipamento e autorizações aplicáveis.'), ('A autorização do organizador é suficiente?', 'Ela é necessária para coordenar o acesso e a produção, mas não substitui a análise operacional nem as demais autorizações e cuidados exigíveis.'), ('A VISIONAIR entrega o vídeo editado?', 'A edição pode ser incluída. Informe se precisa apenas das cenas aéreas ou de um filme com montagem, trilha e versões para divulgação.')],
        'brief': 'Tipo de evento, endereço, data, horários principais, estimativa de público e contato da organização.'
    },
    {
        'slug': 'filmagem-drone-turismo-destinos', 'label': 'Turismo e destinos',
        'title': 'Filmagem com Drone para Turismo no Rio | VISIONAIR',
        'heading': 'Filmagem com drone para turismo e destinos.',
        'description': 'Apresente paisagens, hospedagens e experiências com imagens aéreas. Produção da VISIONAIR com base no Rio de Janeiro e deslocamentos sob consulta.',
        'lead': 'Mostre o lugar e a experiência que ele oferece. Imagens aéreas para aproximar o público de paisagens, hospedagens e destinos, com base de atendimento no Rio de Janeiro.',
        'image': 'rio.jpg', 'alt': 'Pão de Açúcar e Baía de Guanabara, no Rio de Janeiro, em fotografia de referência.',
        'intro_title': 'Um convite para conhecer o destino.',
        'intro': 'A vista do alto pode mostrar o contexto de uma hospedagem, a proximidade com a paisagem e a atmosfera de uma experiência. A VISIONAIR organiza a produção a partir do público que você deseja alcançar e da mensagem que o lugar precisa transmitir, com cenas pensadas para os canais de divulgação do projeto.',
        'uses': [('Hospedagens e espaços', 'Apresentação de áreas externas, implantação e relação com a paisagem, respeitando a privacidade de hóspedes e visitantes.'), ('Paisagens e destinos', 'Planos que situam o lugar e ajudam a construir uma narrativa visual sobre sua experiência.'), ('Campanhas de turismo', 'Material para site, redes sociais, apresentações e peças audiovisuais, conforme o escopo aprovado.')],
        'planning': 'Informe o endereço ou os pontos de captação, os períodos de maior movimento e as áreas que precisam aparecer. Parques, áreas protegidas, propriedades privadas e espaços com regras próprias exigem análise prévia das condições de acesso e filmagem. A luz e a meteorologia também influenciam a janela de produção.',
        'delivery': 'A proposta pode combinar fotografias aéreas e vídeos, com versões para o site e para redes sociais. O roteiro, as locações, a duração e os formatos são definidos antes da captação. Produções fora da cidade do Rio de Janeiro dependem de consulta sobre disponibilidade, logística e deslocamento.',
        'questions': [('Vocês fazem produções fora do Rio?', 'A VISIONAIR tem base no Rio de Janeiro. Outros locais são avaliados individualmente; informe o destino para confirmar disponibilidade e condições.'), ('Posso pedir captação em um parque ou área protegida?', 'O local precisa ser avaliado previamente. Não se garante voo ou captação sem verificar as regras do espaço e as autorizações aplicáveis.'), ('O material pode ser usado em campanhas?', 'Sim, o uso pretendido deve orientar a proposta, inclusive os formatos de entrega e as licenças de trilha ou de outros elementos utilizados na edição.')],
        'brief': 'Destino, endereços ou pontos de interesse, objetivo da campanha, canais de divulgação e período desejado.'
    },
    {
        'slug': 'producao-audiovisual-rio-de-janeiro', 'label': 'Produção audiovisual',
        'title': 'Produção Audiovisual com Drone no Rio | VISIONAIR',
        'heading': 'Produção audiovisual com drone no Rio de Janeiro.',
        'description': 'Captação aérea e edição para marcas, campanhas e projetos no Rio de Janeiro. Planeje seu vídeo com a VISIONAIR, de Rodrigo Victor. Solicite orçamento.',
        'lead': 'Imagens aéreas com uma função na sua história. Da definição do objetivo à entrega, a produção parte do que você quer comunicar e de onde o vídeo será exibido.',
        'image': 'barco-real.webp', 'alt': 'Embarcação vista do alto na Tailândia, em fotografia de referência.',
        'intro_title': 'Uma nova perspectiva para a sua comunicação.',
        'intro': 'Uma cena aérea pode apresentar um lugar, conectar momentos ou dar escala a uma narrativa. A VISIONAIR trabalha o enquadramento e o movimento a partir do briefing, para integrar a captação ao projeto de uma marca, de uma agência ou de uma produção independente.',
        'uses': [('Conteúdo para marcas', 'Imagens para apresentar espaços, experiências e projetos em peças de comunicação.'), ('Campanhas e redes sociais', 'Captação planejada para o enquadramento e a duração das versões que serão publicadas.'), ('Apoio a outras produções', 'Cenas aéreas para integrar uma montagem conduzida por outra equipe, conforme especificações combinadas.')],
        'planning': 'Compartilhe roteiro ou referências, objetivo da peça, público, locações e orientações da equipe de edição. A preparação organiza as cenas prioritárias e verifica as condições de voo. Movimentos e enquadramentos são avaliados conforme os limites do local e da operação.',
        'delivery': 'É possível combinar captação e edição no mesmo escopo ou contratar cenas para uma produção maior. Versões verticais e horizontais, duração, resolução, trilha licenciada, legendas, aplicação de marca e revisões precisam estar descritas na proposta. O prazo é definido conforme o volume e a complexidade da entrega.',
        'questions': [('Posso contratar só as cenas para minha equipe editar?', 'Sim. Especifique o que precisa receber, inclusive arquivos brutos, organização e requisitos técnicos. Esses itens devem constar do orçamento.'), ('Qual é o prazo para receber o vídeo?', 'Não há prazo único para todos os projetos. O cronograma é definido antes da contratação conforme captação, edição, versões e revisões.'), ('Há um exemplo de produção disponível?', 'O portfólio da VISIONAIR apresenta o filme vertical “Histórias à beira-mar”, com 33 segundos. Ele pode ser assistido na página principal.')],
        'brief': 'Objetivo do vídeo, referências, locações, canais de exibição, formatos, necessidade de edição e data desejada.'
    }
]

def provider():
    return {'@type':'LocalBusiness','@id':BASE+'/visionair/#business','name':'VISIONAIR — Rodrigo Victor','url':BASE+'/visionair/','telephone':'+55-21-99616-0489','address':{'@type':'PostalAddress','addressLocality':'Rio de Janeiro','addressRegion':'RJ','addressCountry':'BR'},'areaServed':{'@type':'City','name':'Rio de Janeiro'},'sameAs':['https://www.instagram.com/rv.visionair/']}

def render(s):
    url=BASE+'/visionair/'+s['slug']+'/'
    e=escape
    related=''.join(f'<a href="/visionair/{x["slug"]}/">{e(x["label"])} <span aria-hidden="true">↗</span></a>' for x in SERVICES if x is not s)
    uses=''.join(f'<article><span class="use-number">0{i}</span><h3>{e(t)}</h3><p>{e(p)}</p></article>' for i,(t,p) in enumerate(s['uses'],1))
    faqs=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in s['questions'])
    wa='https://wa.me/5521996160489?text='+quote(f'Olá, Rodrigo! Vim pelo site da VISIONAIR e gostaria de um orçamento para {s["label"].lower()}.')
    graph={'@context':'https://schema.org','@graph':[provider(),{'@type':'Service','@id':url+'#service','name':s['heading'].rstrip('.'),'serviceType':s['label'],'url':url,'description':s['description'],'provider':{'@id':BASE+'/visionair/#business'},'areaServed':{'@type':'City','name':'Rio de Janeiro'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'VISIONAIR','item':BASE+'/visionair/'},{'@type':'ListItem','position':2,'name':s['label'],'item':url}]}]}
    html=f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(s['title'])}</title><meta name="description" content="{e(s['description'])}"><meta name="theme-color" content="#05131b">
<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="VISIONAIR | Rodrigo Victor"><meta property="og:title" content="{e(s['title'])}"><meta property="og:description" content="{e(s['description'])}"><meta property="og:image" content="{BASE}/visionair/assets/{s['image']}"><meta property="og:image:alt" content="{e(s['alt'])}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/visionair/assets/visionair-logo.png" type="image/png"><link rel="preload" as="font" href="/visionair/assets/jost-latin-400-normal.woff2" type="font/woff2" crossorigin><link rel="stylesheet" href="/visionair/style.css?v=20261123-seo1"><link rel="stylesheet" href="/visionair/services.css?v=20261123-seo1"><link rel="alternate" type="text/markdown" href="{url}index.md"><link rel="describedby" href="/llms.txt" type="text/plain">
<script type="application/ld+json">{json.dumps(graph,ensure_ascii=False)}</script></head>
<body class="service-page"><a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="interior-header"><div class="wrap"><a class="brand" href="/visionair/" aria-label="VISIONAIR — início"><img src="/visionair/assets/visionair-logo.png" alt="VISIONAIR — Rodrigo Victor" width="1752" height="897"></a><nav aria-label="Navegação principal"><a href="/visionair/#servicos">Serviços</a><a href="/visionair/#portfolio">Portfólio</a><a href="/visionair/#contato">Contato</a></nav></div></header>
<main id="conteudo"><section class="service-hero section"><div class="wrap"><nav class="breadcrumbs" aria-label="Você está aqui"><a href="/visionair/">VISIONAIR</a><span aria-hidden="true">/</span><span aria-current="page">{e(s['label'])}</span></nav><div class="service-hero-grid"><div><p class="eyebrow">{e(s['label'])}</p><h1>{e(s['heading'])}</h1><p class="service-lead">{e(s['lead'])}</p><a class="button gold" href="{wa}" target="_blank" rel="noopener noreferrer">Solicitar orçamento</a><p class="service-location">RIO DE JANEIRO, RJ · RODRIGO VICTOR</p></div><figure><img src="/visionair/assets/{s['image']}" alt="{e(s['alt'])}" fetchpriority="high" width="1400" height="1000"><figcaption>Fotografia real de referência. <a href="/visionair/creditos.html">Autoria e créditos</a>.</figcaption></figure></div></div></section>
<section class="section"><div class="wrap"><div class="service-intro"><p class="eyebrow">Possibilidades de produção</p><h2>{e(s['intro_title'])}</h2><p>{e(s['intro'])}</p></div><div class="use-grid">{uses}</div></div></section>
<section class="section"><div class="wrap service-body-grid"><div class="service-editorial"><section><p class="eyebrow">Antes da captação</p><h2>Planejamento para o seu projeto.</h2><p>{e(s['planning'])}</p></section><section><p class="eyebrow">Depois da captação</p><h2>Entregas definidas desde o início.</h2><p>{e(s['delivery'])}</p></section><section><h2>Atendimento no Rio de Janeiro.</h2><p>A VISIONAIR tem base no Rio de Janeiro e avalia cada produção pelo endereço, data e escopo. Para outros municípios, consulte a disponibilidade e as condições de deslocamento antes de planejar a contratação.</p><p>O cadastro da aeronave na ANAC/SISANT é <strong>PP-996160489</strong>. Cada voo depende das condições do local e das autorizações aplicáveis; o cadastro não representa autorização irrestrita de operação.</p></section></div><aside class="brief-card"><p class="eyebrow">Vamos conversar</p><h2>O que enviar para o orçamento.</h2><p>{e(s['brief'])}</p><p>Com essas informações, alinhamos viabilidade, escopo, valores, prazos e condições de entrega.</p><a class="button gold" href="{wa}" target="_blank" rel="noopener noreferrer">Conversar pelo WhatsApp</a><a class="brief-phone" href="tel:+5521996160489">(21) 99616-0489</a><a class="text-link" href="/visionair/#portfolio">Ver produção da VISIONAIR ↗</a></aside></div></section>
<section class="section"><div class="wrap"><p class="eyebrow">Perguntas frequentes</p><h2>Antes de contratar.</h2><div class="questions service-questions">{faqs}</div></div></section>
<section class="section"><div class="wrap"><p class="eyebrow">Explore outros serviços</p><nav class="related-services" aria-label="Outros serviços da VISIONAIR">{related}</nav></div></section></main>
<footer class="interior-footer"><div class="wrap"><p>VISIONAIR · Rodrigo Victor · Rio de Janeiro, RJ</p><nav aria-label="Informações e políticas"><a href="/visionair/#sobre">Sobre a VISIONAIR</a><a href="/visionair/#contato">Contato</a><a href="/privacidade.html">Privacidade</a><a href="/termos/">Termos de uso</a><a href="https://www.instagram.com/rv.visionair/" target="_blank" rel="noopener noreferrer">Instagram ↗</a></nav></div></footer></body></html>
'''
    md=f'# {s["heading"].rstrip(".")}\n\n> {s["lead"]}\n\nPágina oficial: {url}\n\n## {s["intro_title"]}\n\n{s["intro"]}\n\n'
    md+='\n\n'.join(f'### {t}\n\n{p}' for t,p in s['uses'])
    md+=f'\n\n## Planejamento\n\n{s["planning"]}\n\n## Entregas\n\n{s["delivery"]}\n\n## Perguntas frequentes\n\n'
    md+='\n\n'.join(f'### {q}\n\n{a}' for q,a in s['questions'])
    md+=f'\n\n## Orçamento e contato\n\nEnvie: {s["brief"]}\n\n- WhatsApp: +55 21 99616-0489 — https://wa.me/5521996160489\n- Base: Rio de Janeiro, RJ. Outros municípios, disponibilidade e deslocamento sob consulta.\n- [Portfólio](https://rodrigovictor.com.br/visionair/#portfolio)\n- [Instagram](https://www.instagram.com/rv.visionair/)\n- [Termos](https://rodrigovictor.com.br/termos/) · [Privacidade](https://rodrigovictor.com.br/privacidade.html)\n\nAeronave cadastrada na ANAC/SISANT: PP-996160489. Cada operação exige análise das condições e autorizações aplicáveis.\n\nA fotografia desta página é uma referência, não um projeto da VISIONAIR. [Créditos](https://rodrigovictor.com.br/visionair/creditos.html).\n'
    folder=ROOT/'visionair'/s['slug']; folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(html)
    (folder/'index.md').write_text(md)

if __name__=='__main__':
    for service in SERVICES: render(service)
    print('Generated 5 service pages and Markdown alternates.')
