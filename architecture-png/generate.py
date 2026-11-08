from pathlib import Path
from html import escape
import subprocess
import zipfile
from PIL import Image

OUT = Path(__file__).resolve().parent
CHROME = Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
NAVY, BLUE, TEXT, MUTED = '#0f1c2d', '#1f3e5a', '#0a1520', '#3a4d61'
PALE, BORDER, LIGHT = '#edf1f6', '#b0bfce', '#f2f4f7'


class Diagram:
    def __init__(self, title, subtitle, height):
        self.h = 354 if height == 480 else 658
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="{self.h}" viewBox="0 60 1240 {self.h}">',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1L10 5L0 9Z" fill="#1f3e5a"/></marker></defs>',
            '<rect y="60" width="1240" height="100%" fill="white"/>',
            '<style>text{font-family:Aptos,"Segoe UI",Arial,sans-serif} .edge{fill:none;stroke:#1f3e5a;stroke-width:1.6;stroke-linejoin:round}</style>']

    def text(self, x, y, value, size=16, color=TEXT, weight=500, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')

    def lane(self, x, y, w, h, title):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{LIGHT}" stroke="#d0d9e4"/>')
        self.text(x+12, y+24, title, 15, NAVY, 700)

    def node(self, x, y, w, h, lines, kind='normal', size=16):
        fill, stroke, color = (PALE, BLUE, TEXT)
        if kind == 'primary': fill, stroke, color = BLUE, BLUE, '#ffffff'
        dash = ' stroke-dasharray="5 4"' if kind in ('external', 'shared') else ''
        if kind in ('db','shared'):
            self.parts.append(f'<path d="M{x} {y+6} A{w/2} 6 0 0 1 {x+w} {y+6} V{y+h-6} A{w/2} 6 0 0 1 {x} {y+h-6} Z" fill="white" stroke="{stroke}" stroke-width="1.4"{dash}/><path d="M{x} {y+6} A{w/2} 6 0 0 0 {x+w} {y+6}" fill="none" stroke="{stroke}" stroke-width="1.2"{dash}/>')
        else:
            self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{dash}/>')
        lineheight=size+5
        first=y+h/2-(len(lines)-1)*lineheight/2+size*.33+(3 if kind in ('db','shared') else 0)
        for i,line in enumerate(lines): self.text(x+w/2,first+i*lineheight,line,size,color,600,'middle')

    def edge(self, path, dashed=False, both=False, arrow=True):
        self.parts.append(f'<path class="edge" d="{path}"'+(' stroke-dasharray="5 4"' if dashed else '')+(' marker-end="url(#arrow)"' if arrow else '')+(' marker-start="url(#arrow)"' if both else '')+'/>')

    def label(self,x,y,line):
        self.text(x,y,line,12,MUTED,500,'middle')

    def save(self, name):
        self.parts.append('</svg>')
        svg=''.join(self.parts)
        (OUT/f'{name}.svg').write_text(svg,encoding='utf-8')
        page=f'<!doctype html><html><head><meta charset="utf-8"><title>{name}</title><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1240px;height:{self.h}px;overflow:hidden;background:white}}svg{{display:block}}@page{{size:landscape;margin:8mm}}</style></head><body>{svg}</body></html>'
        target=OUT/f'{name}.html'
        target.write_text(page,encoding='utf-8')
        subprocess.run([str(CHROME),'--headless','--disable-gpu','--hide-scrollbars','--no-pdf-header-footer','--force-device-scale-factor=3',f'--window-size=1240,{self.h}',f'--screenshot={OUT / (name+".png")}',target.as_uri()],capture_output=True,check=True,timeout=60)
        png=OUT/f'{name}.png'
        with Image.open(png) as im:
            assert im.size == (3720,self.h*3), im.size
            im.save(png,dpi=(300,300))
        print(name,im.size)


def compact():
    d=Diagram('RESQPERATION | Compact System Architecture','Logical architecture • clients, backend controls, data ownership and configured integrations',480)
    d.lane(16,72,210,242,'CLIENT APPLICATIONS')
    d.lane(288,72,634,330,'LARAVEL BACKEND')
    d.lane(986,72,238,176,'DATA STORES')
    d.lane(986,262,238,140,'EXTERNAL SYSTEMS')
    d.node(28,117,186,68,['HQ / Admin Web'])
    d.node(28,219,186,76,['Household / Rescuer','Mobile'])
    d.node(304,117,168,68,['Laravel JSON API'], 'primary')
    d.node(500,117,182,68,['Authentication,','Validation, Permissions'])
    d.node(710,117,196,68,['Operational','Workflow Services'],'primary')
    d.node(710,290,196,94,['Integration and','Notification Services'])
    d.node(1002,108,206,57,['Operational MySQL','and File Storage'],'db',15)
    d.node(1002,180,206,54,['Authorized Shared','Household Records'],'shared',15)
    d.node(1002,300,206,38,['SafeTrack / EvaTrack /','TrackingAid'],'external',14)
    d.node(1002,350,206,38,['Weather / Maps /','Routing / Messaging'],'external',14)
    d.edge('M214 151H304',both=True)
    d.label(259,140,'HTTPS / JSON')
    d.edge('M214 257H252V151',arrow=False)
    d.edge('M472 151H500')
    d.edge('M682 151H710')
    d.edge('M906 137H1002')
    d.edge('M906 168H955V207H1002',both=True)
    d.label(954,224,'Authorized')
    d.label(954,238,'access')
    d.edge('M808 185V290')
    d.edge('M906 319H1002',True)
    d.label(954,281,'API / DB')
    d.edge('M906 369H1002',True)
    d.edge('M710 337H388V185')
    d.label(535,329,'Provider Status')
    d.save('01-compacted-system-architecture')


def detailed(name,title,client_title,client_nodes,modules,mode):
    d=Diagram(title,'Logical architecture • backend-enforced access • explicit owned, shared and external boundaries',800)
    d.lane(16,72,210,478,client_title)
    d.lane(288,72,634,634,'SHARED LARAVEL BACKEND')
    d.lane(986,72,238,334,'DATA STORES')
    d.lane(986,422,238,284,'EXTERNAL SYSTEMS')
    for y,h,lines in client_nodes: d.node(28,y,186,h,lines,size=15)
    d.node(304,112,168,94,['Laravel JSON API','/api/v1'],'primary')
    d.node(500,112,182,94,['Authentication,','Request Validation,','Role / Module Access'],size=15)
    d.node(710,112,196,94,['Operational','Workflow Rules'],'primary')
    d.label(259,148,'HTTPS / JSON')
    if mode=='full':
        d.edge('M214 159H304',both=True)
        d.edge('M214 275H250V159',arrow=False)
        d.edge('M214 391H250V275',arrow=False)
    else:
        d.edge('M121 196V216')
        d.edge('M121 310V330')
        d.edge('M121 424V444')
        d.edge('M214 485H250V159H304',both=True)
    d.edge('M472 159H500')
    d.edge('M682 159H710')
    d.text(304,265,'APPLICATION SERVICE MODULES',13,MUTED,700)
    d.edge('M808 206V237H608V578',arrow=False)
    for i,lines in enumerate(modules):
        x=304 if i%2==0 else 626
        y=282+(i//2)*92
        d.node(x,y,280,74,lines,size=15)
        d.edge(f'M608 {y+37}H{584 if i%2==0 else 626}')
    d.node(304,590,602,72,['Integration Adapters, Notifications and Background Jobs','Provider / Delivery Status'],size=16)
    d.edge('M608 578V590')
    d.edge('M304 626H278V218H388V206')
    d.label(417,232,'Results / Provider Status')
    d.node(1002,112,206,78,['Active MySQL','Operational Records'],'db')
    d.node(1002,222,206,78,['Authorized Shared','Household / Member','Records'],'shared',15)
    d.node(1002,330,206,58,['File Storage, Cache,','Jobs and Outbox'],'db',15)
    d.edge('M906 142H1002')
    d.edge('M906 179H955V261H1002',both=True)
    d.label(955,284,'Authorized')
    d.label(955,298,'access')
    d.edge('M906 503H965V359H1002')
    d.node(1002,460,206,68,['SafeTrack / EvaTrack /','TrackingAid'],'external',15)
    d.node(1002,542,206,64,['Weather, Advisories,','Maps and Routing'],'external',15)
    d.node(1002,620,206,64,['Push Notifications','and SMS Providers'],'external',15)
    d.edge('M906 608H945V494H1002',True)
    d.edge('M906 626H969V574H1002',True)
    d.edge('M906 648H1002',True)
    d.save(name)


compact()
detailed('02-full-system-architecture','RESQPERATION | Full System Architecture','CLIENT APPLICATIONS',[
    (112,94,['HQ / Admin Web']),(228,94,['Household Mobile']),(344,94,['Rescuer Mobile'])],[
    ['Household Directory and Status','Evacuation Check-in'],
    ['Rescue Dispatch and Teams','Field Reports / Communications'],
    ['Disaster Broadcasts and Alerts','Resource Request Workflows'],
    ['Mapping and Hazard Layers','Navigation and Weather'],
    ['Situation / External Reports','Archives and Export Files'],
    ['Accounts, Roles and Profiles','Dashboard and Inquiries']], 'full')
detailed('03-web-system-architecture','RESQPERATION | Web System Architecture','HQ / ADMIN WEB',[
    (112,84,['Authorized HQ / Admin']),(216,94,['Login, Session and','Role-aware Navigation']),
    (330,94,['Operational Screens','Forms, Maps and Reports']),(444,82,['Authenticated API Client','Visible Errors and Status'])],[
    ['Dashboard and Inquiries','Household Directory / Status'],
    ['Rescue Dispatch / Teams','Field Reports / Communications'],
    ['Disaster Broadcasts','Resource Requests / Check-in'],
    ['Mapping / Hazard Layers','Weather and Route Requests'],
    ['Situation / External Reports','Archives, PDF and Exports'],
    ['Personnel, Accounts and Roles','Profiles / Administration']], 'web')
detailed('04-mobile-system-architecture','RESQPERATION | Mobile System Architecture','MOBILE APPLICATION',[
    (112,84,['Household Users','and Rescuers']),(216,94,['Expo React Native','Login and Role Navigation']),
    (330,94,['Role-specific Screens','Maps, Alerts and Reports']),(444,82,['Authenticated API Client','Visible Errors and Status'])],[
    ['Household Profile / Members','Household Status Workflows'],
    ['Rescuer Assignments','Dispatch Progress and Updates'],
    ['Assistance Requests','Evacuation Information / Check-in'],
    ['Field Reports','Field Communications'],
    ['Mapping and Navigation','Weather and Hazard Information'],
    ['Account Access and Profiles','Device Registration / Alerts']], 'mobile')

with zipfile.ZipFile(OUT/'resqperation-architecture-pngs.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(OUT.glob('0*.png')): archive.write(file,file.name)
print('PNG bundle created.')
