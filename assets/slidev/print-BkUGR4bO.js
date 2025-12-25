import{d as p,$ as u,y as f,f as r,o as i,g as e,t as a,F as h,Z as g,i as v,e as x,a0 as b}from"../modules/vue-CM72cxEe.js";import{u as N,j as y,c as d,b as k}from"../index-D7HJrw8e.js";import{N as w}from"./NoteDisplay-CU2D31BE.js";import"../modules/shiki-PW05pg_G.js";const z=p({__name:"print",setup(m,{expose:n}){n();const{slides:l,total:o}=N();u(`
@page {
  size: A4;
  margin-top: 1.5cm;
  margin-bottom: 1cm;
}
* {
  -webkit-print-color-adjust: exact;
}
html,
html body,
html #app,
html #page-root {
  height: auto;
  overflow: auto !important;
}
`),y({title:`Notes - ${d.title}`});const _=f(()=>l.value.map(t=>{var s;return(s=t.meta)==null?void 0:s.slide}).filter(t=>t!==void 0&&t.noteHTML!=="")),c={slides:l,total:o,slidesWithNote:_,get configs(){return d},NoteDisplay:w};return Object.defineProperty(c,"__isScriptSetup",{enumerable:!1,value:!0}),c}}),S={id:"page-root"},D={class:"m-4"},L={class:"mb-10"},T={class:"text-4xl font-bold mt-2"},V={class:"opacity-50"},j={class:"text-lg"},B={class:"font-bold flex gap-2"},H={class:"opacity-50"},W={key:0,class:"border-main mb-8"};function C(m,n,l,o,_,c){return i(),r("div",S,[e("div",D,[e("div",L,[e("h1",T,a(o.configs.title),1),e("div",V,a(new Date().toLocaleString()),1)]),(i(!0),r(h,null,g(o.slidesWithNote,(t,s)=>(i(),r("div",{key:s,class:"flex flex-col gap-4 break-inside-avoid-page"},[e("div",null,[e("h2",j,[e("div",B,[e("div",H,a(t==null?void 0:t.no)+"/"+a(o.total),1),b(" "+a(t==null?void 0:t.title)+" ",1),n[0]||(n[0]=e("div",{class:"flex-auto"},null,-1))])]),x(o.NoteDisplay,{"note-html":t.noteHTML,class:"max-w-full"},null,8,["note-html"])]),s<o.slidesWithNote.length-1?(i(),r("hr",W)):v("v-if",!0)]))),128))])])}const O=k(z,[["render",C],["__file","/home/runner/work/zzc_2025_review/zzc_2025_review/node_modules/@slidev/client/pages/presenter/print.vue"]]);export{O as default};
