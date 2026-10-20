// Workspace-only adapter for missing standard-font aliases in the bundled renderer.
// Converts the installed Adobe font metrics without changing fonts or runtime files.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire,registerHooks} from 'node:module';
import {pathToFileURL} from 'node:url';
export function registerStandardFontAliases(modules,build){
  const require=createRequire(import.meta.url);
  const {Font}=require(path.join(modules,'@pdf-lib/standard-fonts'));
  const names=['Courier','Courier-Bold','Courier-BoldOblique','Courier-Oblique','Helvetica','Helvetica-Bold','Helvetica-BoldOblique','Helvetica-Oblique','Symbol','Times-Bold','Times-BoldItalic','Times-Italic','Times-Roman','ZapfDingbats'];
  const target=path.join(build,'standard-fonts');fs.mkdirSync(target,{recursive:true});
  const mappings={};
  for(const name of names){
    const f=Font.load(name),glyphs=f.CharMetrics.map(x=>x.N),indices=new Map(glyphs.map((x,i)=>[x,i]));
    const groups=new Map();
    for(const [a,b,k] of f.KernPairs){if(!indices.has(a)||!indices.has(b))continue;const group=groups.get(k)||[];group.push(indices.get(a)*glyphs.length+indices.get(b));groups.set(k,group);}
    const kernPairs=[];
    for(const [k,values] of groups){values.sort((a,b)=>a-b);let last=0;const deltas=values.map(v=>{const delta=v-last;last=v;return delta;});kernPairs.push(k,deltas);}
    const data={name,bbox:f.FontBBox,ascender:f.Ascender||0,descender:f.Descender||0,xHeight:f.XHeight||0,capHeight:f.CapHeight||0,glyphNames:glyphs.join(' '),glyphWidths:f.CharMetrics.map(x=>x.WX),kernPairs};
    const file=path.join(target,name+'.cjs');fs.writeFileSync(file,'module.exports='+JSON.stringify(data)+';');
    mappings['#standard-fonts/'+name.replaceAll('-','')]=pathToFileURL(file).href;
  }
  registerHooks({resolve(specifier,context,nextResolve){return mappings[specifier]?{url:mappings[specifier],shortCircuit:true}:nextResolve(specifier,context);}});
}
