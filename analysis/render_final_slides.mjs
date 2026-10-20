import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {registerStandardFontAliases} from './font_runtime_compat.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const modules=process.env.KAPPA_NODE_MODULES||'C:/Users/Minh Minh minh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
registerStandardFontAliases(modules,path.join(root,'.slide_build'));
const {FileBlob,PresentationFile}=await import(pathToFileURL(path.join(modules,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const deck=await PresentationFile.importPptx(await FileBlob.load(path.join(root,'deliverables/Kappa_Committee_Presentation.pptx')));
const out=path.join(root,'.slide_build/final');await fs.mkdir(out,{recursive:true});
for(let i=0;i<deck.slides.items.length;i++){
 const blob=await deck.export({slide:deck.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(out,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const pdf=await deck.export({format:'pdf'});
await fs.writeFile(path.join(root,'deliverables/Kappa_Committee_Presentation.pdf'),new Uint8Array(await pdf.arrayBuffer()));
console.log(`Rendered all ${deck.slides.items.length} final slides and the PDF from the delivered PPTX.`);
