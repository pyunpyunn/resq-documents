"""Validate the delivered diagrams, set PNG print metadata, and write the index."""
from pathlib import Path
from collections import Counter, defaultdict
from html import escape
import csv
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
import zlib

from PIL import Image
from catalog import OUT
from drawing import P
from build_suite import FAMILIES, LANES

Image.MAX_IMAGE_PIXELS=110_000_000


def validate():
    catalog=json.loads((OUT/'assets/catalog.json').read_text(encoding='utf-8'))
    modules={m['key']:m for m in catalog['modules']}
    assert 'UC13B' not in catalog['functions'] and 'UC38' not in catalog['functions']
    assert modules['03_household_setup']['cases']==['UC08']
    assert modules['05_alerts']['providers']==['OneSignal']
    assert {'UC15','UC16','UC41','UC19'}<=set(modules['07_dispatch']['cases'])
    assert set(catalog['functions']['UC23A']['roles'])=={'Chairperson','Operations / Admin'}
    entries=json.loads((OUT/'assets/manifest.json').read_text(encoding='utf-8'))
    rendered=json.loads((OUT/'assets/render-results.json').read_text(encoding='utf-8'))
    by_file={r['relative']:r for r in rendered}
    assert len(entries)==168 and len(rendered)==168
    assert Counter(e['family'] for e in entries)=={family:24 for family,_ in FAMILIES}
    counts=Counter();crossings=0
    data=struct.pack('>IIB',11811,11811,1)
    phys=struct.pack('>I',9)+b'pHYs'+data+struct.pack('>I',zlib.crc32(b'pHYs'+data)&0xffffffff)
    colors=set(P.values())
    for entry in entries:
        source=OUT/entry['relative'];render=by_file[entry['relative']];png=Path(render.get('output',source.with_suffix('.png')))
        entry['png_relative']=str(png.relative_to(OUT)).replace('\\','/')
        assert not render.get('error'),(source,render.get('error'))
        assert not render['clipped'] and not render['tableOverflow'] and render['font'],source
        assert hashlib.sha256(source.read_bytes()).hexdigest()==render['hash'],('Stale PNG',source)
        assert entry['audit']['label_obstructions']==0,('Label obstruction',source)
        tree=ET.parse(source).getroot()
        assert not any(e.tag.endswith('}foreignObject') for e in tree.iter()),source
        assert {e.attrib.get('id') for e in tree if e.tag.endswith('}g')}=={'Title','Containers','Nodes','Connectors','Labels'},source
        for e in tree.iter():
            assert e.tag.split('}')[-1] not in ('linearGradient','radialGradient','filter'),source
            for key in ('fill','stroke'):
                value=e.attrib.get(key,'none')
                assert value=='none' or value in colors,(source,value)
        nodes={n['key']:n for n in entry['node_data']}
        if entry['family']=='02_Use_Case':
            for edge in entry['edge_data']:
                if not edge['association']:continue
                match=re.fullmatch(r'(household|rescuer|web)(UC\d+[A-Z]?)',edge['target'])
                assert match,source
                function=catalog['functions'][match[2]];actor=nodes[edge['source']]['label']
                assert actor in function['roles'] or (not function['roles'] and actor in (function.get('external_actors') or ['Authorized Partner System'])),(source,actor,function['title'])
                if match[1]=='household':assert match[2] not in {'UC23A','UC23B','UC26B','UC26C','UC32B','UC33'},source
            assert not any('Register Push Subscription' in n['label'] or 'Verify Evacuation' in n['label'] for n in nodes.values()),source
            for element in tree.iter():
                if 'data-edge' in element.attrib:assert float(element.attrib['stroke-width'])>=2.25 and float(element.attrib.get('opacity','1'))>=.95,source
        for edge in entry['edge_data']:
            assert edge['source'] in nodes and edge['target'] in nodes,source
            if edge['association'] or edge.get('uml'):continue
            for a,b in zip(edge['points'],edge['points'][1:]):
                horizontal=abs(a[1]-b[1])<.02;vertical=abs(a[0]-b[0])<.02
                assert horizontal or vertical,('Non-orthogonal connector',source)
                for node in nodes.values():
                    if node['key'] in (edge['source'],edge['target']):continue
                    if horizontal:
                        hit=node['y']+.1<a[1]<node['y']+node['h']-.1 and max(min(a[0],b[0]),node['x'])<min(max(a[0],b[0]),node['x']+node['w'])-.1
                    else:
                        hit=node['x']+.1<a[0]<node['x']+node['w']-.1 and max(min(a[1],b[1]),node['y'])<min(max(a[1],b[1]),node['y']+node['h'])-.1
                    assert not hit,('Connector crosses unrelated card',source,edge['source'],edge['target'],node['key'])
        if entry['family']=='03_Flow_Chart':
            assert sum(n['label']=='Start' for n in nodes.values())==1
            assert sum(n['label']=='End' for n in nodes.values())>=1
            for node in nodes.values():
                if node['kind']=='decision':
                    exits=[e for e in entry['edge_data'] if e['source']==node['key']]
                    assert len(exits)==2 and {e['label'] for e in exits}=={'Yes','No'},(source,node)
                    assert len({tuple(e['points'][0]) for e in exits})==2,('Ambiguous shared decision exit',source,node)
        if entry['family'] in ('03_Flow_Chart','04_Swim_Lane'):
            for edge in entry['edge_data']:
                if edge['label'] in ('Yes','No'):assert edge['color']==edge['label'].lower(),source
        if entry['family']=='04_Swim_Lane':
            headers=[n for n in nodes.values() if n['kind']=='header']
            assert all(n['label'] in LANES for n in headers)
            for n in nodes.values():
                if n['kind']=='header':continue
                matches=[h for h in headers if n['y']>=h['y'] and n['y']+n['h']<=h['y']+h['h']]
                assert len(matches)==1,('Step not in exactly one lane',source,n)
        if entry['family']=='05_Data_Flow':
            for edge in entry['edge_data']:
                assert nodes[edge['source']]['kind']=='dfd' or nodes[edge['target']]['kind']=='dfd',source
                assert edge['label'],('Unlabeled data flow',source)
                assert edge['label'].lower() not in ('task data','task result'),source
                box=edge['label_box'];assert box,source
                x,y,w,h=box
                for a,b in zip(edge['points'],edge['points'][1:]):
                    if abs(a[1]-b[1])<.02:hit=y<a[1]<y+h and max(min(a[0],b[0]),x)<min(max(a[0],b[0]),x+w)
                    else:hit=x<a[0]<x+w and max(min(a[1],b[1]),y)<min(max(a[1],b[1]),y+h)
                    assert not hit,('DFD label masks its connector',source,edge['label'])
            for n in nodes.values():
                if n['kind']=='dfd':
                    assert any(e['source']==n['key'] for e in entry['edge_data']) and any(e['target']==n['key'] for e in entry['edge_data']),source
                if n['kind']=='store':
                    assert any(e['source']==n['key'] for e in entry['edge_data']) and any(e['target']==n['key'] for e in entry['edge_data']),source
        if entry['family']=='06_System_Architecture':
            for edge in entry['edge_data']:
                if nodes[edge['target']]['kind']=='database':assert edge['source']=='shared' or edge['source'].startswith('api'),source
        if entry['family']=='07_Tech_Stack':
            assert not any(nodes[e['source']]['label'] in ('Integrations','Tooling') or nodes[e['target']]['label'] in ('Integrations','Tooling') for e in entry['edge_data']),source
        raw=png.read_bytes()
        if b'pHYs' not in raw[:200]:png.write_bytes(raw[:33]+phys+raw[33:])
        with Image.open(png) as image:
            assert abs(image.width-render['width'])<=1 and abs(image.height-render['height'])<=1,source
            assert abs(image.info['dpi'][0]-300)<.1,source
            image.verify()
        counts[entry['family']]+=1
    full_erd=next(e for e in entries if e['family']=='01_ERD' and e['mode']=='full')
    assert full_erd['nodes']==102 and full_erd['edges']==174
    report={
      'diagrams':len(entries),'pngs':len(entries),'svgs':len(entries),'per_family':dict(counts),
      'checks':{'inter_loaded':True,'native_editable_svg_text':True,'palette_only':True,'no_clipped_text':True,'no_table_text_overflow':True,'no_connector_card_obstructions':True,'no_connector_label_obstructions':True,'orthogonal_except_uml':True,'decision_yes_no_exits':True,'distinct_decision_exit_ports':True,'green_yes_red_no_branches':True,'role_specific_use_case_associations':True,'first_login_setup_isolated':True,'onesignal_disaster_alerts_only':True,'evatrack_owns_arrival_verification':True,'dfd_labels_clear_of_connectors':True,'one_system_lane_per_step':True,'dfd_process_store_rules':True,'clients_use_api_not_database':True,'png_dpi_300':True,'png_source_hash_match':True},
      'scope':{'full':7,'compact':7,'user_role':70,'module':84},
      'source_inventory':{'functional_use_cases':50,'api_routes':211,'physical_tables':102,'foreign_keys':174},
      'limits':['Large full-system diagrams are reference atlases; role/module views are intended for page-sized academic figures.','Route checks reject card obstructions and enforce 90-degree crossings; non-planar full graphs can still require crossings.','Schema, permission and API evidence are source snapshots, not production or partner acceptance evidence.'],
    }
    (OUT/'VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return entries,report


def write_indexes(entries):
    by_family=defaultdict(list)
    for e in entries:by_family[e['family']].append(e)
    def link(e,ext):return e.get('png_relative',e['relative'].replace('.svg','.png')) if ext=='png' else e['relative']
    path_rows=[];cards=[]
    for family,title in FAMILIES:
        group=by_family[family];full=next(e for e in group if e['mode']=='full');compact=next(e for e in group if e['mode']=='compact')
        path_rows.append(f"| {title} | [{Path(link(full,'png')).name}]({link(full,'png')}) | [PNG]({link(compact,'png')}) | [{family}/]({family}/) |")
        links=f'<p class="links"><a href="{link(full,"png")}">Full PNG</a><a href="{link(full,"svg")}">Full SVG</a><a href="{link(compact,"png")}">Compact PNG</a><a href="{link(compact,"svg")}">Compact SVG</a></p>'
        details=[]
        for mode,label in [('role','10 user-role views'),('module','12 module / feature views')]:
            rows=[]
            for e in sorted((e for e in group if e['mode']==mode),key=lambda e:e['relative']):rows.append(f'<li><span>{escape(e["scope_title"])}</span><a href="{link(e,"png")}">PNG</a><a href="{link(e,"svg")}">SVG</a></li>')
            details.append(f'<details><summary>{label}</summary><ul>'+''.join(rows)+'</ul></details>')
        cards.append(f'<section id="{family}"><h2>{title}</h2><a class="preview" href="{link(compact,"svg")}"><img loading="lazy" src="{link(compact,"svg")}" alt="{title}: compact view"></a>{links}'+''.join(details)+'</section>')
        # Family-local indexes keep directory links useful in browsers and Figma handoffs.
        local=['<!doctype html><html><head><meta charset="utf-8"><title>'+title+'</title><style>body{font:16px Segoe UI,sans-serif;color:#0F1E3D;max-width:1000px;margin:40px auto}li{margin:12px 0}a{color:#12306B;margin-right:18px}</style></head><body><a href="../index.html">All diagram families</a><h1>'+title+'</h1><ul>']
        for e in sorted(group,key=lambda e:e['relative']):
            rel=str(Path(e['relative']).relative_to(family)).replace('\\','/');png_rel=str(Path(link(e,'png')).relative_to(family)).replace('\\','/');local.append(f'<li>{escape(e["scope_title"])} — <a href="{png_rel}">PNG</a><a href="{rel}">SVG</a></li>')
        local.append('</ul></body></html>');(OUT/family/'index.html').write_text(''.join(local),encoding='utf-8')
    paths=['# RESQPERATION — Seven Diagram Families','',f'Root: `{OUT}`','','Each family contains Full, Compacted, 10 user-role, and 12 module/feature views. Every diagram has PNG and editable SVG files.','','| Diagram | Full-system PNG | Compacted | All views |','| --- | --- | --- | --- |']+path_rows+['','[Open the visual index](index.html) · [Function list](FUNCTION_LIST.md) · [Function CSV](FUNCTION_LIST.csv) · [API functions](API_FUNCTION_LIST.csv) · [Validation](VALIDATION.json)','',
      'For print figures, use the compact, role or module versions; the complete physical ERD is a large reference atlas. Inter is bundled in `assets/Inter.ttf` for editable SVG imports.','',
      'Swimlanes use system lanes. Module names appear on the corresponding steps. DFD external-entity instances are repeated locally to reduce wire bundles; repeated labels refer to the same logical actor, not additional users.','',
      'The original SRS sources and earlier exports remain available. These redesigned files are collected here to avoid overwriting prior work or locked image files.']
    (OUT/'PATHS.md').write_text('\n'.join(paths)+'\n',encoding='utf-8')
    html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RESQPERATION Diagram Suite</title><style>
    @font-face{font-family:Inter;src:url(assets/Inter.ttf);font-weight:100 900}*{box-sizing:border-box}body{margin:0;background:#F5F8FD;color:#0F1E3D;font:15px/1.5 Inter,"Segoe UI",Arial,sans-serif}header{background:#12306B;color:white;padding:28px max(24px,calc((100vw - 1400px)/2))}h1{font-size:28px;margin:0 0 6px}header p{margin:0}nav{max-width:1400px;margin:20px auto;display:flex;gap:12px;flex-wrap:wrap;padding:0 20px}a{color:#12306B}nav a,.links a{padding:7px 12px;border:1px solid #CBD5E1;border-radius:8px;background:white;text-decoration:none}main{max-width:1400px;margin:20px auto;padding:0 20px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}section{border:1.5px solid #CBD5E1;border-radius:16px;background:white;padding:20px}h2{font-size:21px;color:#12306B;margin:0 0 12px}.preview{display:block;border:1px solid #E8EDF3;border-radius:10px;height:260px;overflow:hidden;background:white}.preview img{width:100%;height:100%;object-fit:contain}.links{display:flex;gap:8px;flex-wrap:wrap;font-size:13px}details{margin-top:10px;border-top:1px solid #E8EDF3;padding-top:10px}summary{cursor:pointer;font-weight:600}ul{padding:0;list-style:none}li{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #F5F8FD}li span{flex:1}footer{max-width:1400px;margin:20px auto 40px;padding:0 20px;color:#475569}@media(max-width:800px){main{grid-template-columns:1fr}}
    </style></head><body><header><h1>RESQPERATION Diagram Suite</h1><p>7 families · 168 diagrams · PNG + editable SVG · larger Inter typography</p></header><nav><a href="PATHS.md">All paths</a><a href="FUNCTION_LIST.md">50 functional use cases</a><a href="FUNCTION_LIST.csv">Function CSV</a><a href="API_FUNCTION_LIST.csv">211 API routes</a><a href="VALIDATION.json">Validation report</a><a href="assets/Inter.ttf">Inter font</a></nav><main>'''+''.join(cards)+'''</main><footer>Full diagrams cover the source-backed system scope. Compact, role and module views are the recommended academic-page figures. Use the bundled Inter font when importing SVGs into Figma. Swimlanes name systems and identify modules within the steps; DFD entity copies refer to the same logical actor.</footer></body></html>'''
    html=html.replace('<nav><a href="PATHS.md">', '<nav><a href="TECHNICAL_GUIDE.html">Technical guide</a><a href="PATHS.md">', 1)
    (OUT/'index.html').write_text(html,encoding='utf-8')
    (OUT/'DESIGN_TOKENS.json').write_text(json.dumps({'colors':P,'font':'Inter','font_sizes':{'title':34,'node':18,'table_header':18,'field':16,'data_type':14,'connector':14,'container':14,'badge':12},'outer_margin':60,'base_grid':8,'connector_width':1.75,'use_case_association_width':2.25,'use_case_association_opacity':1,'decision_branch_width':2.25,'decision_branch_colors':{'Yes':P['yes'],'No':P['no']},'radii':{'container':16,'table':12,'process':10,'label_chip':6}},indent=2),encoding='utf-8')


if __name__=='__main__':
    entries,report=validate();write_indexes(entries)
    print(f"Validated {report['diagrams']} PNG/SVG pairs. Wrote index.html, PATHS.md, seven family indexes, design tokens and validation report.")
