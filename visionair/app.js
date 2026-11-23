'use strict';
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#nav');
function closeMenu(){menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Abrir menu');nav.classList.remove('open');}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Fechar menu':'Abrir menu');nav.classList.toggle('open',open);});
nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&nav.classList.contains('open')){closeMenu();menu.focus();}});
document.addEventListener('click',event=>{if(!event.target.closest('.header'))closeMenu();});
document.querySelectorAll('a[data-project]').forEach(link=>link.addEventListener('click',()=>{document.querySelector('#type').value=link.dataset.project;}));
const motion=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth';
function setupDots(track){const dots=document.querySelector('[data-track="'+track.id+'"]');const items=[...track.children].filter(item=>!item.hidden);dots.replaceChildren();items.forEach((item,index)=>{const dot=document.createElement('button');dot.type='button';dot.setAttribute('aria-label','Mostrar '+(item.dataset.title||item.querySelector('h3')?.textContent||'item '+(index+1)));dot.setAttribute('aria-pressed',String(index===0));dot.addEventListener('click',()=>track.scrollTo({left:item.getBoundingClientRect().left-track.getBoundingClientRect().left+track.scrollLeft,behavior:motion()}));dots.append(dot);});const update=()=>{const left=track.getBoundingClientRect().left;let best=0,min=Infinity;items.forEach((item,index)=>{const distance=Math.abs(item.getBoundingClientRect().left-left);if(distance<min){min=distance;best=index;}});[...dots.children].forEach((dot,index)=>dot.setAttribute('aria-pressed',String(index===best)));};track.onscroll=update;update();}
document.querySelectorAll('.carousel').forEach(setupDots);
const gallery=document.querySelector('.gallery');
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(other=>{const active=other===button;other.classList.toggle('active',active);other.setAttribute('aria-pressed',String(active));});let count=0;gallery.querySelectorAll('.gallery-card').forEach(card=>{card.hidden=button.dataset.filter!=='all'&&!card.dataset.category.split(' ').includes(button.dataset.filter);if(!card.hidden)count++;});gallery.classList.toggle('filtered',button.dataset.filter!=='all');gallery.scrollTo({left:0,behavior:'instant'});setupDots(gallery);document.querySelector('#gallery-status').textContent=count+' itens exibidos.';}));
const lightbox=document.querySelector('.lightbox');
const lightboxImage=document.querySelector('#lightbox-image');
const video=document.querySelector('#lightbox-video');
document.querySelectorAll('button.gallery-card').forEach(card=>card.addEventListener('click',()=>{const img=card.querySelector('img');lightboxImage.src=img.src;lightboxImage.alt=img.alt;const isVideo=Boolean(card.dataset.video);lightboxImage.hidden=isVideo;if(video){video.hidden=!isVideo;if(isVideo){video.src=card.dataset.video;video.poster=img.src;}}
document.querySelector('#lightbox-title').textContent=card.dataset.title;document.querySelector('#lightbox-description').textContent=card.dataset.description;document.querySelector('.lightbox .eyebrow').textContent=isVideo?'Filme VISIONAIR':'Referência visual ilustrativa';document.querySelector('#lightbox-contact').dataset.project=card.dataset.project;lightbox.showModal();}));
function closeLightbox(){lightbox.close();}
document.querySelector('.lightbox-close').addEventListener('click',closeLightbox);
lightbox.addEventListener('click',event=>{if(event.target===lightbox){const box=lightbox.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)closeLightbox();}});
lightbox.addEventListener('close',()=>{if(video){video.pause();video.removeAttribute('src');video.load();}});
document.querySelector('#lightbox-contact').addEventListener('click',event=>{document.querySelector('#type').value=event.currentTarget.dataset.project;closeLightbox();});
function createBriefMessage(data){const lines=['Olá, Rodrigo! Vim pelo site da VISIONAIR.','','Nome: '+data.name.trim(),'Projeto: '+data.type];if(data.email.trim())lines.push('E-mail: '+data.email.trim());if(data.phone.trim())lines.push('WhatsApp: '+data.phone.trim());lines.push('','Mensagem: '+data.message.trim(),'','Gostaria de conversar sobre um orçamento.');return lines.join('\n');}
document.querySelector('#brief-form').addEventListener('submit',event=>{event.preventDefault();const form=event.currentTarget;if(!form.reportValidity())return;const data=Object.fromEntries(new FormData(form));const url='https://wa.me/5521996160489?text='+encodeURIComponent(createBriefMessage(data));window.location.assign(url);});
document.querySelector('#year').textContent=new Date().getFullYear();
