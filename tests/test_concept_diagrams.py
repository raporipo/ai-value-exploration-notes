"""Run with python -m unittest discover -s tests."""
from pathlib import Path
from html.parser import HTMLParser
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('diagrams',ROOT/'scripts/embed_concept_diagrams.py')
diagrams=importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagrams)

class FigureParser(HTMLParser):
    def __init__(self):
        super().__init__();self.images=[];self.ids=[];self.details=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='img':self.images.append(attrs)
        if tag=='details':self.details+=1

class ConceptDiagrams(unittest.TestCase):
    def test_bilingual_figures_and_self_contained_semantics(self):
        for item in diagrams.DATA:
            payloads=[]
            for lang in ['ja','en']:
                page=ROOT/'docs'/('en' if lang=='en' else '')/item['page']
                source=page.read_text()
                ident='diagram-'+item['id']
                match=re.search(rf'<!-- {ident}:start -->(.*?)<!-- {ident}:end -->',source,re.S)
                self.assertIsNotNone(match)
                parser=FigureParser();parser.feed(match[1])
                self.assertEqual(len(parser.images),1)
                self.assertEqual(parser.details,1)
                self.assertEqual(len(parser.ids),len(set(parser.ids)))
                image=parser.images[0]
                self.assertTrue(image['alt'])
                asset=(page.parent/image['src']).resolve()
                self.assertTrue(asset.is_relative_to(ROOT/'docs/assets/diagrams'))
                svg=ET.parse(asset).getroot()
                self.assertEqual(svg.get('viewBox').split()[2:],[image['width'],image['height']])
                raw=re.search(r'<script type="application/json"[^>]*>(.*?)</script>',match[1],re.S)[1]
                data=json.loads(raw);payloads.append(data)
                self.assertEqual(data,json.loads(svg.find('{http://www.w3.org/2000/svg}metadata').text))
                ids=set(data.get('nodes',data.get('states',{})))
                for rel in data.get('relations',[])+data.get('transitions',[]):
                    self.assertIn(rel[0],ids);self.assertIn(rel[2],ids)
                    self.assertIn(rel[1],data['notation']['relation_definitions'])
                for a,b in data.get('judgment_domain',{}).items():
                    self.assertIn(a,ids);self.assertIn(b,ids)
                self.assertTrue(set(data.get('mutual_revision',[]))<=ids)
            self.assertEqual(payloads[0],payloads[1])

    def test_regeneration_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            copy=Path(folder)/'repo'
            shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('__pycache__','.git'))
            files=list((copy/'docs').rglob('*.html'))+list((copy/'docs/assets/diagrams').glob('*.svg'))
            before={p.relative_to(copy):p.read_bytes() for p in files}
            for _ in range(2):
                subprocess.run([sys.executable,str(copy/'scripts/embed_concept_diagrams.py')],check=True)
                self.assertEqual(before,{p.relative_to(copy):p.read_bytes() for p in files})

if __name__=='__main__':unittest.main()
