# Rodrigo Victor — Personal Trainer

Site institucional de Rodrigo Victor, personal trainer na Zona Sul do Rio de Janeiro.
CREF 041487-G/RJ.

Site estático em HTML, CSS e JavaScript puro. Sem build, sem dependências de runtime,
sem framework. Basta servir os arquivos.

---

## Publicar no GitHub Pages

1. Crie o repositório e envie os arquivos:

```bash
git init
git add .
git commit -m "Site inicial"
git branch -M main
git remote add origin git@github.com:USUARIO/REPOSITORIO.git
git push -u origin main
```

2. No GitHub, vá em **Settings → Pages** e aponte *Source* para a branch `main`, pasta `/ (root)`.

3. O arquivo `CNAME` já contém `rodrigovictor.com.br`. No painel do registrador do domínio,
   crie os registros:

| Tipo  | Nome  | Valor |
|-------|-------|-------|
| A     | `@`   | `185.199.108.153` |
| A     | `@`   | `185.199.109.153` |
| A     | `@`   | `185.199.110.153` |
| A     | `@`   | `185.199.111.153` |
| CNAME | `www` | `USUARIO.github.io` |

4. Depois que o DNS propagar, marque **Enforce HTTPS** em Settings → Pages.

O arquivo `.nojekyll` está no repositório para o GitHub Pages não processar o conteúdo
com Jekyll.

### Rodar localmente

```bash
python3 -m http.server 8000
```

Abra `http://localhost:8000`. Não abra o `index.html` direto pelo `file://`: as fontes
locais são bloqueadas por CORS nesse protocolo.

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
JSON-LD) e no `privacidade.html`.

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
