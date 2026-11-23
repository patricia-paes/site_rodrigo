# Rodrigo Victor — Personal Trainer

Site institucional de Rodrigo Victor, personal trainer na Zona Sul do Rio de Janeiro.
CREF 041487-G/RJ.

Páginas em HTML, CSS e JavaScript, com dois pontos PHP 8 para negociação de conteúdo e consultas MCP. A produção usa Hostinger/LiteSpeed.

## Publicação

O repositório `patricia-paes/site_rodrigo`, branch `main`, é a fonte da implantação existente na Hostinger. Preserve todos os diretórios, inclusive `visionair/` e `.well-known/`, e o arquivo `.htaccess`.

Não mudar este domínio para GitHub Pages: Pages não executa o PHP necessário para a home em Markdown, os cabeçalhos HTTP e o endpoint MCP.

- `index.php` serve o `index.html` aprovado ou `index.md`, conforme `Accept` e seus pesos `q`.
- A resposta da home anuncia `llms.txt`, o Markdown alternativo e o MCP Server Card pelo cabeçalho `Link`; `Vary: Accept` separa as representações.
- `.htaccess` define `DirectoryIndex index.php index.html`, MIME de Markdown e a rota adicional `/mcp/server-card`.
- `mcp/index.php` é um endpoint público, sem estado e somente leitura. Não consulta agenda, clientes, preços privados nem sistemas externos.
- `site-data.json` alimenta as consultas. Atualize-o junto com as páginas e as versões Markdown quando contatos ou serviços mudarem.
- `robots.txt` permite busca e uso como contexto (`search=yes, ai-input=yes`) e declara oposição a treinamento (`ai-train=no`). Trata-se de uma preferência de uso, não um bloqueio de segurança.
- O endereço estruturado contém apenas a localidade confirmada (Rio de Janeiro/RJ/BR). Não há endereço de rua publicado ou inventado.

### Verificação

O MCP responde a `initialize`, `ping`, `tools/list`, `tools/call`, `resources/list` e `resources/read`. Aceita os protocolos 2025-11-25, 2025-06-18 e 2025-03-26. Requisições POST usam JSON-RPC; GET retorna 405 porque não há stream SSE. As únicas consultas são `get_business_information` e `list_services`, com `business` igual a `personal_trainer` ou `visionair`.

O Server Card está em `/.well-known/mcp/server-card.json`, mantendo o caminho solicitado pelo auditor. O formato segue os campos atuais da extensão de Server Cards, sucessora da SEP-1649. O campo adicional `capabilities` reflete a resposta real de inicialização.

A integração WebMCP está preparada, mas ainda não ativada nas páginas: o navegador de validação não oferece essa API, e a ativação experimental está bloqueada neste ambiente. Os testes de contrato passaram; falta chamar as ferramentas em um navegador com suporte nativo antes de incluir `<script src="/assets/js/agent-tools.js" defer></script>` nas páginas. O arquivo detecta `document.modelContext` e a implementação antiga em `navigator.modelContext`. O navegador precisa oferecer a API; navegadores comuns continuam usando os controles normais. As consultas do navegador também são somente leitura.

Para verificar o PHP localmente, use PHP 8. As regras de `.htaccess` precisam de Apache/LiteSpeed e devem ser confirmadas na hospedagem. Um servidor estático simples permite revisar o visual, mas não valida negociação HTTP ou MCP.

---

## Estrutura

```
index.html            página principal
privacidade.html      política de privacidade (LGPD)
assets/
  css/style.css       estilos, com os tokens de cor e tipografia no topo
  js/main.js          menu, header fixo, máscara de telefone, envio do formulário
  fonts/              Cormorant Garamond e Jost auto-hospedados (88 KB)
  img/                imagens responsivas em JPG e WebP, logos e favicons
CNAME, robots.txt, sitemap.xml, site.webmanifest, .nojekyll
```

---

## O que ainda precisa ser preenchido

### Depoimentos

A seção `#depoimentos` no `index.html` está com três blocos vazios marcados com `TODO`.
Os textos do mockup original não foram aproveitados: eram fictícios e um deles comparava
resultados de forma que o código de ética do CONFEF restringe.

Para cada depoimento real, substitua o bloco por:

```html
<li class="card-depo">
  <p>Texto do depoimento, nas palavras do próprio aluno.</p>
  <p class="card-depo__meta">Nome do aluno</p>
</li>
```

Antes de publicar, colha **autorização por escrito** de cada aluno para uso do nome e do
texto. Evite frases que prometam ou comparem resultados.

### Contato

Já configurados:

- WhatsApp: `(21) 99616-0489` → `wa.me/5521996160489`
- Instagram: `@coachrodrigovictor`
- LinkedIn: `linkedin.com/in/rodrigo-ferreira-62576147`
- CREF: `041487-G/RJ`

O e-mail `contato@rodrigovictor.com.br` veio do mockup e **ainda não foi confirmado**.
Se estiver errado, ele aparece em três lugares: no `index.html` (bloco de contato e
JSON-LD) na home. A página de contato e a política de privacidade usam o WhatsApp confirmado.

Para trocar o número de WhatsApp, altere a constante `WHATSAPP` no topo de
`assets/js/main.js` e os links `wa.me` no `index.html`.

### Blog

O mockup previa uma seção de artigos, que não foi incluída: quatro posts que nunca são
atualizados prejudicam mais do que ajudam. Se o Rodrigo for publicar com regularidade,
vale reintroduzir — é bom para SEO. Se não for, o feed do Instagram cumpre o papel.

---

## Como as imagens foram tratadas

As fotos originais são de céu azul e luz forte, e não conviviam com a paleta escura do
mockup aprovado. Todas passaram por uma graduação de cor: dessaturação, escurecimento e
deslocamento dos médios em direção ao tom da marca (`#0B1214`).

A seção **Sobre** usa fundo claro (`--bone`) e a foto da corrida na orla, recortada em 0,62:1.
Nessa seção a imagem preenche a altura da coluna de texto (posicionamento absoluto acima de
900px), de modo que a base da foto e a do quadro de credenciais coincidem exatamente. O
quadro fica em duas colunas no desktop e em uma abaixo de 720px.

O hero foi recortado para 2:1 na mesma proporção e enquadramento do modelo aprovado, o
que deixa o Rodrigo à direita e livra a área de texto à esquerda. O hero mobile usa um
recorte vertical separado, posicionando o rosto acima do bloco de texto.

Cada imagem foi exportada em JPG e WebP, em várias larguras, servidas por `srcset`.

**Os arquivos de logo originais não tinham transparência.** Apesar do nome,
`logosemfundo.png` estava sobre um fundo taupe sólido (RGB 186,179,167). O
`assets/img/logo-lockup.png` foi extraído com canal alfa real, preservando a textura
dourada. Os favicons vieram do selo circular.

### Substituir uma imagem

Mantenha o mesmo nome e as mesmas larguras dos arquivos existentes. Para gerar as
variações a partir de um original novo:

```python
from PIL import Image, ImageEnhance
import numpy as np
exec(open('grade.py').read())   # script de graduação, na raiz do projeto
img = Image.open('foto-nova.jpg').convert('RGB')
emit(grade(img), 'sobre', [640, 960, 1280])
```

---

## Paleta e tipografia

Os tokens ficam em `:root`, no topo do `style.css`.

| Token | Valor | Uso |
|---|---|---|
| `--ink-800` | `#0B1214` | fundo escuro base |
| `--ink-700` | `#0E1719` | seções alternadas |
| `--ink-900` | `#070C0D` | rodapé e CTA |
| `--bone` | `#EFEDE8` | seção clara |
| `--gold` | `#B57F4D` | dourado da marca, amostrado do arquivo do logo |
| `--gold-lt` | `#C79A6A` | dourado para texto sobre fundo escuro |
| `--gold-dp` | `#8A5F34` | dourado para texto sobre fundo claro |

Display em **Cormorant Garamond**, corpo em **Jost**, que acompanha a geometria do
wordmark do logo. Ambas auto-hospedadas em `assets/fonts/`, sem chamada ao Google Fonts —
mais rápido e um ponto a menos de exposição de dados do visitante.

Todos os pares de texto e fundo passam em WCAG AA. O mais apertado é o dourado sobre a
seção clara, em 4,76:1.

---

## Notas técnicas

- **Formulário**: não há back-end. O envio monta uma mensagem e abre o WhatsApp já
  preenchido. Por isso não há dados trafegando ou armazenados em servidor, o que
  simplifica bastante a conformidade com a LGPD.
- **Consentimento**: o checkbox é obrigatório e validado antes do envio.
- **SEO local**: `Person` e `LocalBusiness` em JSON-LD, com os bairros atendidos em
  `areaServed`. Vale abrir também um Google Business Profile.
- **Acessibilidade**: link de pular para o conteúdo, foco visível, navegação por teclado
  no menu, `prefers-reduced-motion` respeitado, textos alternativos descritivos.
- **Movimento**: só a entrada do hero, uma vez no carregamento. Sem animações de scroll.


## VISIONAIR — produção audiovisual com drone

A página de drone integra este mesmo site em `https://rodrigovictor.com.br/visionair/`.
Os arquivos de `visionair/` são estáticos e não precisam de build. Os estilos e scripts
são independentes dos arquivos de Personal Trainer. A home inclui um acesso no
rodapé para `/visionair/`, identificado como “VISIONAIR · Filmagens com drone”.
A página de drone está incluída no sitemap e mantém conteúdo e navegação próprios.

Contatos da VISIONAIR:
- WhatsApp: +55 21 99616-0489
- Instagram: https://www.instagram.com/rv.visionair/

O formulário abre o WhatsApp com uma mensagem para revisão e envio pelo visitante.
Não armazena dados e não envia mensagens automaticamente.

A logomarca usa o desenho original da VISIONAIR com fundo transparente. A seção de
operação responsável apresenta o cadastro ANAC/SISANT PP-996160489, sem divulgar
o modelo, a validade da certidão, CPF, número de série ou o documento integral.

A fotografia de Rodrigo e o vídeo de 33 segundos foram fornecidos pela proprietária.
O vídeo está em MP4/H.264, otimizado para a web, sem reprodução automática.
As quatro publicações do Instagram foram reutilizadas com autorização da proprietária;
cada miniatura leva ao respectivo post em @rv.visionair.
As imagens de apresentação e serviços são ilustrativas, geradas por IA; a paisagem
fotográfica é de Shai Pal / Unsplash, com crédito na página:
https://unsplash.com/photos/sugarloaf-mountain-and-guanabara-bay-at-sunset-G3qe7t13s1I

O layout segue o mockup aprovado: hero, sobre, cinco serviços, galeria com filtros,
diferenciais, cinco etapas, operação responsável, seis perguntas e contato.
No celular, serviços e galeria usam navegação horizontal com indicadores acessíveis.
