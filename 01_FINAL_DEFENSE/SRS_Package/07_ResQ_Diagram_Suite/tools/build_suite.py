"""Generate the seven source-backed diagram families and every requested scope."""
from pathlib import Path
from collections import defaultdict, deque
import json
import math
import re
import sys

from catalog import OUT, ROOT, UCROOT, build_catalog, export_catalog
from drawing import Diagram, Node, Edge, P, COLOR, esc, wrap, text_width

FAMILIES=[('01_ERD','Entity Relationship Diagram'),('02_Use_Case','Use Case Diagram'),('03_Flow_Chart','Flow Chart'),('04_Swim_Lane','Swim Lane Diagram'),('05_Data_Flow','Data Flow Diagram'),('06_System_Architecture','System Architecture'),('07_Tech_Stack','Tech Stack')]
LANES=['Household Mobile','Rescuer Mobile','HQ Web','Laravel API','External']
LANE_COLOR=['blue','cyan','navy','slate','slate']
CLIENT_LABEL={'household':'Household Mobile','rescuer':'Rescuer Mobile','web':'HQ Web'}
MODULE_ACTIONS=['Manage Account Access','Administer System Accounts','Set Up Household','Report Household Safety','Publish / Read Disaster Alerts','Monitor Operational Records','Coordinate Rescue Dispatch','Record Field Assessment','Navigate Assigned Mission','Exchange Voice Clips','Manage Resource Requests','Generate Operational Reports']
FLOW_LABELS={
 '01_access':{'start':'Open Application','credentials':'Enter Credentials','reject':'Show Sign-In Error','verify':'Credentials Valid?','owner':'Owner Selection Required?','authorize':'Validate Access Scope','choose':'Select Household Member','workspace':'Open Authorized Workspace'},
 '02_administration':{'entry':'Choose Administrative Task','public':'Public Inquiry?','inquiry':'Submit Public Inquiry','staff':'Staff Access Allowed?','validate':'Validate Account Changes','deny':'Show Access Denied','result':'Display Saved Result','changes':'Review Administrative Records','save':'Save Authorized Changes'},
 '03_household_setup':{'entry':'Sign In','select':'Select Household Member','pin':'Enter Household Location','owner':'Owner Selection Required?','check':'Validate Owner Token','valid':'Household Data Valid?','error':'Show Setup Error','done':'Open Household Overview','save':'Save Household Setup'},
 '04_safety':{'start':'Choose Safety Report','send':'Submit Safety Status','choose':'Load Event Options','scope':'Report Scope Valid?','reject':'Show Report Error','save':'Save Status Evidence','show':'Refresh Safety History'},
 '05_alerts':{'start':'Prepare Event Alert','authorize':'Publication Allowed?','ready':'Recipients Available?','accepted':'Provider Accepted Delivery?','reject':'Show Publication Error','save':'Save Delivery Plan','empty':'Record No Recipients','failed':'Retain Delivery Failure','id':'Save Provider Reference','submit':'Send Targeted Alert','phone':'Display Available Notification'},
 '06_monitoring':{'start':'Open Monitoring Module','gate':'Module Access Allowed?','derive':'Calculate Operational Summaries','ready':'Source Data Available?','deny':'Show Access Denied','none':'Show Unavailable Data','view':'Display Operational Records','read':'Read Scoped Evidence'},
 '07_dispatch':{'start':'Review Rescue Needs','select':'Select Team Targets','gate':'Dispatch Scope Valid?','error':'Show Dispatch Error','save':'Save Rescue Assignment','evidence':'Save Field Progress','deliver':'Publish Assignment Update','rescuer':'Update Assigned Mission','review':'Review Completion Approval'},
 '08_assessment':{'start':'Open Assigned Household','entry':'Capture Assessment Findings','reject':'Show Assessment Error','gate':'Assessment Scope Valid?','save':'Save Field Assessment','review':'Review Field Evidence'},
 '09_navigation':{'start':'Open Mission Navigation','follow':'Record Mission Progress','gate':'Route Access Valid?','none':'Show Route Unavailable','network':'Network Available?','cached':'Saved Route Available?','ack':'Apply Sync Acknowledgment','route':'Return Available Route','queue':'Retain Pending Events','sync':'Validate Replayed Events'},
 '10_radio':{'start':'Select Communication Channel','talk':'Transmit Voice Clip','permit':'Transmission Allowed?','fail':'Show Communication Error','upload':'Validate Uploaded Audio','file':'Store Voice Recording','meta':'Save Clip Metadata','review':'Review Available Recording'},
 '11_requests':{'start':'Submit Logistics Need','gate':'Request Data Valid?','accept':'Partner Accepted Handoff?','error':'Show Request Error','pending':'Save Pending Request','return':'Record Returned Decision','retry':'Retain Handoff Failure','track':'Track Fulfillment Evidence','review':'Review Resource Request','valid':'Release Authorized?','forward':'Forward Validated Request'},
 '12_reports':{'start':'Select Report Scope','gate':'Report Access Valid?','external':'External Release Required?','error':'Show Report Error','deliver':'Retrieve Authorized File','pending':'Save Release Request','reject':'Record Release Rejection','review':'Review Report Decision','accept':'Release Accepted?','snapshot':'Compile Recorded Findings','file':'Generate Authorized Export'},
}


def scopes(c):
    all_cases=list(c['functions'])
    yield {'key':'01_Full/full_system','title':'Full System','cases':all_cases,'modules':c['modules'],'compact':False,'role':None,'mode':'full'}
    yield {'key':'02_Compacted/compacted_system','title':'Compacted System','cases':all_cases,'modules':c['modules'],'compact':True,'role':None,'mode':'compact'}
    for role in c['roles']:
        cases=[k for k in role['cases'] if k in c['functions']]
        mods=[m for m in c['modules'] if any(k in cases for k in m['cases'])]
        yield {'key':'03_Per_User_Role/'+role['key'],'title':role['title'],'cases':cases,'modules':mods,'compact':False,'role':role,'mode':'role'}
    for module in c['modules']:
        yield {'key':'04_Per_Module/'+module['key'],'title':module['title'],'cases':module['cases'],'modules':[module],'compact':False,'role':None,'mode':'module'}


def make(c,s,family):return Diagram(f'{FAMILIES[family][1]} — {s["title"]}',FAMILIES[family][0],s['key'])


def system_set(c,s):
    if s['role']:return [s['role']['system']]
    systems={system for key in s['cases'] for system in c['functions'][key]['systems']}
    return [system for system in ('household','rescuer','web') if system in systems]


def module_label(c,s,module,verb=False):
    if module.get('diagram_label'):return module['diagram_label'] if verb else module['title']
    selected=[c['functions'][key] for key in module['cases'] if key in s['cases']]
    if s['role']:
        if len(selected)==1:return selected[0]['title']
        return ('Use ' if verb else '')+module['title']
    return MODULE_ACTIONS[c['modules'].index(module)] if verb else module['title']


def domain(table):
    if any(w in table for w in ('user','role','password','device','token','session','audit')):return 'navy'
    if any(w in table for w in ('household','member','address','geotag','barangay','purok','sitio','evacuation','region','province','cit','gender','relationship','occupation','education','vulnerable','zipcode','civil')):return 'blue'
    if any(w in table for w in ('responder','rescue','dispatch','route','trip','hazard','disaster','severity','field_report','damage')):return 'cyan'
    return 'slate'


def ordered_tables(names,rels):
    adjacent=defaultdict(set)
    for r in rels:
        if r['parent'] in names and r['child'] in names:adjacent[r['parent']].add(r['child']);adjacent[r['child']].add(r['parent'])
    result=[];remaining=set(names)
    while remaining:
        first=min(remaining,key=lambda t:(-len(adjacent[t]),t));q=deque([first])
        while q:
            t=q.popleft()
            if t not in remaining:continue
            remaining.remove(t);result.append(t)
            q.extend(sorted(adjacent[t]&remaining,key=lambda k:(domain(k)!=domain(t),-len(adjacent[k]),k)))
    return result


def erd(c,s):
    d=make(c,s,0)
    if s['mode'] in ('full','compact'):main=set(c['tables'])
    elif s['role'] and s['role']['actor']=='public':main={'landing_inquiries'}
    else:main={t for m in s['modules'] for t in m['tables']}
    context={r['parent'] for r in c['relationships'] if r['child'] in main}-main
    names=main|context;rels=[r for r in c['relationships'] if r['child'] in main and r['parent'] in names]
    order=ordered_tables(names,rels);cols=min(5,3 if len(names)<=18 else 5,len(names));card_w=440;gap=96
    cards={}
    for t in order:
        fields=c['tables'][t]['fields']
        if t in context:fields=[f for f in fields if 'PK' in f['keys']]
        elif s['compact']:fields=[f for f in fields if any(k in ('PK','FK') for k in f['keys'])]
        header=max(48,len(wrap(t,card_w-32,18))*24+16)
        rows=[]
        for f in fields:
            label_lines=wrap(f['name'],card_w-150,16,600 if 'PK' in f['keys'] else 400)
            ref_lines=wrap('→ '+f['references'],card_w-96,14,400) if f.get('references') else []
            h=max(36,len(label_lines)*22+12+len(ref_lines)*20)
            rows.append((f,h,label_lines,ref_lines))
        cards[t]={'fields':rows,'header':header,'h':header+sum(r[1] for r in rows)}
    y=140
    for row_start in range(0,len(order),cols):
        row=order[row_start:row_start+cols];row_h=max(cards[t]['h'] for t in row)
        for col,t in enumerate(row):
            x=100+col*(card_w+gap);card=cards[t];color=domain(t);h=card['h'];head=card['header'];key='table'+str(order.index(t))
            n=d.add(Node(key,x,y,card_w,h,t,'process',color,'white'),False);cards[t].update({'x':x,'y':y,'key':key,'ports':{}})
            d.raw(f'<g id="{key}" data-node="{key}" data-kind="table" data-table="{t}"><rect x="{x}" y="{y}" width="{card_w}" height="{h}" rx="12" fill="{P["white"]}" stroke="{P[color]}" stroke-width="1.5"/>')
            d.raw(f'<path d="M{x+12} {y}H{x+card_w-12}Q{x+card_w} {y} {x+card_w} {y+12}V{y+head}H{x}V{y+12}Q{x} {y} {x+12} {y}Z" fill="{P[color]}"/>')
            d.center_text(x,y,card_w,head,t,18,'white')
            yy=y+head
            for i,(f,rh,lines,refs) in enumerate(card['fields']):
                if i%2:
                    if i==len(card['fields'])-1:d.raw(f'<path d="M{x+1} {yy}H{x+card_w-1}V{yy+rh-12}Q{x+card_w-1} {yy+rh-1} {x+card_w-12} {yy+rh-1}H{x+12}Q{x+1} {yy+rh-1} {x+1} {yy+rh-12}Z" fill="{P["mist"]}"/>')
                    else:d.raw(f'<rect x="{x+1}" y="{yy}" width="{card_w-2}" height="{rh}" fill="{P["mist"]}"/>')
                if i:d.raw(f'<path d="M{x} {yy}H{x+card_w}" stroke="{P["border"]}" stroke-width="1"/>')
                pk='PK' in f['keys'];fk='FK' in f['keys'];badge='PK' if pk else 'FK' if fk else ''
                if badge:
                    bf=P[color] if pk else P['blue-tint'];bc='white' if pk else 'navy'
                    d.raw(f'<rect x="{x+12}" y="{yy+9}" width="34" height="20" rx="10" fill="{bf}"/>');d.center_text(x+12,yy+9,34,20,badge,12,bc)
                    if pk and fk:
                        d.raw(f'<rect x="{x+12}" y="{yy+33}" width="34" height="20" rx="10" fill="{P["blue-tint"]}"/>');d.center_text(x+12,yy+33,34,20,'FK',12,'navy')
                d.text(x+58,yy+25,'\n'.join(lines),16,'ink',600 if pk else 400,line_height=22)
                d.text(x+card_w-14,yy+25,f['type'],14,'muted',400,'end')
                if refs:d.text(x+58,yy+25+len(lines)*22,'\n'.join(refs),14,'blue',400,line_height=20)
                cards[t]['ports'][f['name']]=yy+rh/2;yy+=rh
            d.raw(f'<rect x="{x}" y="{y}" width="{card_w}" height="{h}" rx="12" fill="none" stroke="{P[color]}" stroke-width="1.5"/></g>')
        y+=row_h+gap
    for r in rels:
        a,b=cards[r['parent']],cards[r['child']]
        right=b['x']>=a['x'];ss='e' if right else 'w';ts='w' if right else 'e'
        if a['x']==b['x']:ss=ts='e'
        sy=a['ports'].get(r['parent_column'],a['y']+a['header']/2);ty=b['ports'].get(r['column'],b['y']+b['header']/2)
        d.connect(a['key'],b['key'],color='navy',source_side=ss,target_side=ts,source_offset=sy,target_offset=ty,relation=r)
    return d


def use_case(c,s):
    d=make(c,s,1);systems=system_set(c,s);x0=60
    phase_order={'Account Access and Permissions':0,'First-Login Household Setup':1,'Household Profile and Identity':2,'Disaster Alerts and Safety':3,'Evacuation Maps and Saved Data':4,'Assigned Rescue Missions':5,'Rescue Field Assessments':6}
    mission_order={'UC15':0,'UC16':1,'UC41':2,'UC19':3}
    for system in systems:
        color=COLOR[system];selected=[]
        for key in s['cases']:
            f=c['functions'][key]
            if system not in f['systems']:continue
            if s['role'] and s['role']['title'] not in f['roles']:continue
            item=dict(f);item['title']=f.get('system_titles',{}).get(system,f['title'])
            item['subcases']=[] if s['compact'] else f.get('system_subcases',{}).get(system,f['subcases'])
            selected.append(item)
        selected.sort(key=lambda f:(phase_order.get(f['phase'],7),f['phase'],mission_order.get(f['key'],9)))
        if not selected:continue
        primary_w=340;sub_w=320;has_sub=any(f['subcases'] for f in selected);panel_w=primary_w+40+(sub_w+144 if has_sub else 0)
        rows=[];headings=[];yy=204;previous_phase=None
        for f in selected:
            if f['phase']!=previous_phase:
                headings.append((yy+12,f['phase']));yy+=40;previous_phase=f['phase']
            height=max(112,88*len(f['subcases']));rows.append((f,yy,height));yy+=height+24
        boundary_x=x0+204;boundary_y=140;boundary_h=max(200,yy-140+8)
        d.container(boundary_x,boundary_y,panel_w,boundary_h,CLIENT_LABEL[system],color,'white',True)
        for hy,heading in headings:d.text(boundary_x+20,hy,heading.upper(),14,color,600,group='Labels')
        def captions(f):
            if s['role']:return [s['role']['title']]
            allowed=[r['title'] for r in c['roles'] if r['system']==system and f['key'] in r['cases']]
            return allowed or f.get('external_actors') or ['Authorized Partner System']
        actors={}
        for f,y,h in rows:
            for caption in captions(f):actors.setdefault(caption,[]).append(y+h/2)
        actor_nodes={}
        for i,(caption,ys) in enumerate(actors.items()):
            cy=sum(ys)/len(ys);ay=max(156,cy-29)
            while any(abs(ay-n.y)<148 for n in actor_nodes.values()):ay+=148
            key=f'{system}Actor{i}';actor_nodes[caption]=d.add(Node(key,x0,ay,164,140,caption,'actor',color,'white'))
        for f,y,h in rows:
            children=f['subcases'];ny=y+(h-80)/2;key=f'{system}{f["key"]}'
            primary=d.add(Node(key,boundary_x+20,ny,primary_w,80,f['title'],'usecase',color,color+'-tint',18,data={'function':f['key']}))
            for caption in captions(f):
                actor=actor_nodes[caption];d.connect(actor.key,key,association=True,color='navy',source_side='e',target_side='w',source_offset=actor.y+29)
            for j,(label,relationship) in enumerate(children):
                child_key=key+'Sub'+str(j);child_y=y+j*88+4
                d.add(Node(child_key,primary.right+144,child_y,sub_w,72,label,'usecase',color,'white',18))
                if relationship=='include':d.connect(key,child_key,label='«include»',color='navy',dashed=True,source_side='e',target_side='w',via=[])
                else:d.connect(child_key,key,label='«extend»',color='navy',dashed=True,source_side='w',target_side='e',via=[])
                d.edges[-1].data_uml=True
        x0=boundary_x+panel_w+64
    return d


def parse_module_flow(module):
    path=UCROOT/'02_MODULES'/f'{module["key"]}_swimlane.mmd';text=path.read_text(encoding='utf-8');nodes={};edges=[];lane='Laravel API'
    for line in text.splitlines():
        m=re.match(r'\s*subgraph\s+\w+\["([^"]+)"\]',line)
        if m:lane=m[1];continue
        if '-->' in line:
            m=re.match(r'\s*(\w+)\s*-->\s*(?:\|"([^"]+)"\|\s*)?(\w+)',line)
            if m:edges.append((m[1],m[3],m[2] or ''))
            continue
        m=re.match(r'\s+(\w+)\s*([\[({/]+).*?"([^"]+)"',line)
        if m:
            ident,shape,label=m.groups();kind='decision' if shape.startswith('{') else 'database' if shape.startswith('[(') else 'io' if shape.startswith('[/') else 'terminator' if shape.startswith('([') else 'process'
            short=FLOW_LABELS[module['key']][ident]
            # Source terminal nodes often contain a result action; give the whole
            # diagram explicit Start/End nodes rather than hiding that action.
            if kind=='terminator':kind='process'
            nodes[ident]={'key':ident,'kind':kind,'label':short,'raw_lane':lane,'source_label':label}
    # Authenticate remains a decision when its source has Valid/Invalid exits.
    for ident,n in nodes.items():
        outgoing=[e for e in edges if e[0]==ident]
        if n['label'].endswith('?') or (ident=='verify' and len(outgoing)==2):n['kind']='decision'
        if n['kind']=='decision':
            if len(outgoing)!=2:raise ValueError('Decision needs exactly two exits: '+module['key']+'/'+ident)
            for i,(a,b,label) in enumerate(edges):
                if a==ident:edges[i]=(a,b,'No' if label.lower().startswith(('invalid','no')) else 'Yes')
    return nodes,edges


def generic_flow(c,s):
    if s['compact']:
        nodes={
         'select':{'key':'select','label':'Choose Permitted Module','kind':'subprocess','raw_lane':'Web client'},
         'gate':{'key':'gate','label':'Access Scope Valid?','kind':'decision','raw_lane':'API'},
         'deny':{'key':'deny','label':'Show Access Error','kind':'process','raw_lane':'Web client'},
         'work':{'key':'work','label':'Apply Authorized Workflow','kind':'subprocess','raw_lane':'API'},
         'data':{'key':'data','label':'Read / Write Records','kind':'database','raw_lane':'API'},
         'result':{'key':'result','label':'Display Actual Result','kind':'io','raw_lane':'Web client'},
        }
        return nodes,[('select','gate',''),('gate','deny','No'),('gate','work','Yes'),('work','data',''),('data','result','')]
    if s['role'] and s['role']['actor']=='public':
        nodes={
         'inquiry':{'key':'inquiry','label':'Submit Public Inquiry','kind':'io','raw_lane':'HQ Web'},
         'gate':{'key':'gate','label':'Inquiry Data Valid?','kind':'decision','raw_lane':'API'},
         'error':{'key':'error','label':'Show Input Error','kind':'process','raw_lane':'HQ Web'},
         'save':{'key':'save','label':'Save Public Inquiry','kind':'database','raw_lane':'API'},
         'result':{'key':'result','label':'Display Submission Result','kind':'io','raw_lane':'HQ Web'},
        }
        return nodes,[('inquiry','gate',''),('gate','error','No'),('gate','save','Yes'),('save','result','')]
    if len(s['modules'])==1 and not s['role']:return parse_module_flow(s['modules'][0])
    nodes={
      'startTask':{'key':'startTask','label':'Choose Authorized Task','kind':'process','raw_lane':'HQ Web'},
      'gate':{'key':'gate','label':'Access Scope Valid?','kind':'decision','raw_lane':'API'},
      'reject':{'key':'reject','label':'Show Access Error','kind':'process','raw_lane':'Web client'},
      'dispatchTask':{'key':'dispatchTask','label':'Choose Permitted Module','kind':'process','raw_lane':'Web client'},
      'write':{'key':'write','label':'Record Change Required?','kind':'decision','raw_lane':'API'},
      'valid':{'key':'valid','label':'Input Data Valid?','kind':'decision','raw_lane':'API'},
      'error':{'key':'error','label':'Show Validation Error','kind':'process','raw_lane':'Web client'},
      'save':{'key':'save','label':'Save Authorized Records','kind':'database','raw_lane':'API'},
      'read':{'key':'read','label':'Read Authorized Records','kind':'database','raw_lane':'API'},
      'result':{'key':'result','label':'Display Actual Result','kind':'io','raw_lane':'Web client'},
    }
    edges=[('startTask','gate',''),('gate','reject','No'),('gate','dispatchTask','Yes')]
    for i,m in enumerate(s['modules']):
        ident='module'+str(i);nodes[ident]={'key':ident,'label':module_label(c,s,m),'kind':'subprocess','raw_lane':'API','module':m['title']};edges.extend([('dispatchTask',ident,''),(ident,'write','')])
    edges.extend([('write','read','No'),('write','valid','Yes'),('valid','error','No'),('valid','save','Yes'),('save','result',''),('read','result','')])
    return nodes,edges


def topological(nodes,edges):
    incoming={k:0 for k in nodes};outs=defaultdict(list)
    for a,b,_ in edges:incoming[b]+=1;outs[a].append(b)
    roots=[k for k in nodes if incoming[k]==0];queue=deque(roots);rank={k:0 for k in roots};order=[]
    while queue:
        a=queue.popleft();order.append(a)
        for b in outs[a]:
            rank[b]=max(rank.get(b,0),rank[a]+1);incoming[b]-=1
            if incoming[b]==0:queue.append(b)
    for k in nodes:
        if k not in rank:rank[k]=max(rank.values(),default=0)+1
    return rank,roots,[k for k in nodes if not outs[k]]


def flowchart(c,s):
    d=make(c,s,2);nodes,edges=generic_flow(c,s);ranks,roots,leaves=topological(nodes,edges)
    grouped=defaultdict(list)
    for key,n in nodes.items():grouped[ranks[key]].append((key,n))
    maxcols=min(4,max(map(len,grouped.values())));center=100+maxcols*344/2
    d.add(Node('flowStart',center-90,140,180,56,'Start','terminator','navy','navy'))
    y=248
    for rank,items in sorted(grouped.items()):
        for start in range(0,len(items),4):
            chunk=items[start:start+4];hh=max(136 if n['kind']=='decision' else 80 if n['kind']=='database' else 72 for _,n in chunk)
            left=center-(len(chunk)*344-64)/2
            for i,(key,n) in enumerate(chunk):
                kind=n['kind'];w=280;h=136 if kind=='decision' else 80 if kind=='database' else 72;color='blue' if kind=='decision' else 'cyan' if kind=='io' else 'navy';fill=color+'-tint' if kind in ('decision','io','database') else 'white'
                d.add(Node(key,left+i*344,y+(hh-h)/2,w,h,n['label'],kind,color,fill))
            y+=hh+80
    d.add(Node('flowEnd',center-90,y,180,56,'End','terminator','navy','navy'))
    for key in roots:d.connect('flowStart',key)
    for a,b,label in edges:d.connect(a,b,label=label)
    for key in leaves:d.connect(key,'flowEnd')
    return d


def lane_for(raw,module,s):
    raw=raw.lower()
    if 'household' in raw or 'resident' in raw:return 0
    if any(k in raw for k in ('rescuer','team leader','assigned rescuer')):return 1
    if any(k in raw for k in ('provider','onesignal','weather source')):return 4
    if any(k in raw for k in ('hq','approver','dispatcher','staff','web','request reviewer')):return 2
    if any(k in raw for k in ('data','api','storage','file','integration','delivery','service','backend')):return 3
    if s['role']:return {'household':0,'rescuer':1,'web':2}[s['role']['system']]
    if module['key'] in ('03_household_setup','04_safety'):return 0
    if module['key'] in ('08_assessment','09_navigation','10_radio','11_requests'):return 1
    return 2


def swimlane(c,s):
    d=make(c,s,3)
    if s['compact']:
        compact_steps=[('status','Report Household Safety',0,'Household Safety'),('saveStatus','Save Status Evidence',3,'Household Safety'),('review','Review Rescue Needs',2,'Operational Monitoring'),('dispatch','Dispatch Rescue Team',2,'Rescue Dispatch'),('saveDispatch','Save Rescue Assignment',3,'Rescue Dispatch'),('notify','Deliver Assignment Alert',4,'Disaster Alerts'),('field','Record Mission Findings',1,'Field Assessment'),('saveField','Save Field Evidence',3,'Field Assessment'),('report','Review Operational Reports',2,'Reports and Archives')]
        steps=[{'key':key,'label':label,'kind':'process','lane':lane,'module':module} for key,label,lane,module in compact_steps]
        edges=[(a['key'],b['key'],'') for a,b in zip(steps,steps[1:])];roots=[steps[0]['key']];leaves=[steps[-1]['key']]
    elif len(s['modules'])==1 and (not s['role'] or s['role']['actor']=='public'):
        module=s['modules'][0];nodes,edges=generic_flow(c,s);ranks,roots,leaves=topological(nodes,edges)
        # One step per temporal column; dependencies stay in source order.
        order=sorted(nodes,key=lambda k:(ranks[k],list(nodes).index(k)))
        steps=[dict(nodes[key],lane=lane_for(nodes[key]['raw_lane'],module,s),module=module['title']) for key in order]
    else:
        module=None
        steps=[{'key':'open','label':'Open Authorized Workspace','kind':'process','lane':{'household':0,'rescuer':1,'web':2}.get(s['role']['system'] if s['role'] else 'household',0),'module':'Account Access'}]
        for i,m in enumerate(s['modules']):
            key='module'+str(i);lane=0 if m['key'] in ('03_household_setup','04_safety') else 1 if m['key'] in ('08_assessment','09_navigation','10_radio') else 2
            if s['role']:lane={'household':0,'rescuer':1,'web':2}[s['role']['system']]
            steps.extend([{'key':key,'label':module_label(c,s,m,True),'kind':'subprocess','lane':lane,'module':m['title']},{'key':key+'Api','label':'Apply Scoped Workflow','kind':'process','lane':3,'module':m['title']}])
        edges=[(a['key'],b['key'],'') for a,b in zip(steps,steps[1:])];roots=[steps[0]['key']];leaves=[steps[-1]['key']]
    # Wrap long timelines into readable panels, retaining left-to-right time.
    pitch=288;node_w=224;lane_h=208;left=248;max_columns=9
    initial_lane=steps[0]['lane'];final_lane=steps[-1]['lane']
    timeline=[{'key':'swimStart','label':'Start','kind':'terminator','lane':initial_lane,'module':''}]+steps+[{'key':'swimEnd','label':'End','kind':'terminator','lane':final_lane,'module':''}]
    frame_y=156
    for panel_start in range(0,len(timeline),max_columns):
        part=timeline[panel_start:panel_start+max_columns]
        active_lanes=[lane for lane in range(5) if any(step['lane']==lane for step in part)]
        if len(active_lanes)==1:active_lanes=sorted(set(active_lanes+[3]))
        lane_map={lane:i for i,lane in enumerate(active_lanes)};frame_w=len(part)*pitch+224
        d.text(60,frame_y-14,'PHASE '+str(panel_start//max_columns+1),14,'slate',600,group='Containers')
        frame_h=len(active_lanes)*lane_h;clip='laneClip'+str(panel_start)
        d.extent(60,frame_y,frame_w,frame_h)
        d.raw(f'<defs><clipPath id="{clip}"><rect x="60" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="12"/></clipPath></defs><g clip-path="url(#{clip})">','Containers')
        for lane,i in lane_map.items():
            yy=frame_y+i*lane_h
            d.add(Node(f'laneHeader{panel_start}_{lane}',60,yy,168,lane_h,LANES[lane],'header',LANE_COLOR[lane],'white'),False)
            d.raw(f'<rect x="61" y="{yy+1}" width="{frame_w-2}" height="{lane_h-2}" fill="{P["mist"] if i%2 else P["white"]}"/>','Containers')
            if lane<4:d.raw(f'<rect x="61" y="{yy+1}" width="168" height="{lane_h-2}" fill="{P[LANE_COLOR[lane]]}"/>','Containers')
            else:d.raw(f'<rect x="61" y="{yy+1}" width="168" height="{lane_h-2}" fill="{P["white"]}" stroke="{P["slate"]}" stroke-width="1.5"/>','Containers')
            d.center_text(68,yy+20,154,lane_h-40,LANES[lane],18,'white' if lane<4 else 'slate',group='Containers')
            if i:d.raw(f'<path d="M60 {yy}H{60+frame_w}" stroke="{P["border"]}" stroke-width="1.5"/>','Containers')
        d.raw(f'</g><rect x="60" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="12" fill="none" stroke="{P["navy"]}" stroke-width="2"/>','Containers')
        for column,step in enumerate(part):
            lane=step['lane'];kind=step['kind'];h=120 if kind=='decision' else 80 if kind=='database' else 56 if kind=='terminator' else 72
            x=left+column*pitch;yy=frame_y+lane_map[lane]*lane_h;y=yy+72+(104-h)/2
            if step['module']:d.text(x+node_w/2,yy+44,step['module'],14,LANE_COLOR[lane],600,'middle',group='Labels',max_width=node_w)
            color='navy' if kind=='terminator' else 'blue' if kind=='decision' else LANE_COLOR[lane]
            fill='navy' if kind=='terminator' else color+'-tint' if kind in ('decision','database','io') else 'white'
            width=144 if kind=='terminator' else node_w
            d.add(Node(step['key'],x,y,width,h,step['label'],kind,color,fill,18))
        frame_y+=len(active_lanes)*lane_h+112
    for key in roots:d.connect('swimStart',key,source_side='e',target_side='w')
    for a,b,label in edges:d.connect(a,b,label=label,source_side='e',target_side='w')
    for key in leaves:d.connect(key,'swimEnd',source_side='e',target_side='w')
    return d


def dfd_labels(module,system,role=None):
    if role and role['actor']=='public':return 'Public Inquiry Details','Inquiry Submission Receipt'
    key=module['key']
    if key.startswith('compact'):
        key=['01_access','04_safety','07_dispatch','11_requests','05_alerts','12_reports'][int(key.removeprefix('compact'))]
    labels={
      '01_access':('Sign-In / Permission Choices','Account / Permission Status'),
      '02_administration':('Account / Inquiry Changes','Saved Account / Inquiry Records'),
      '03_household_setup':('Phone Owner / Home Location','Confirmed Household Setup'),
      '04_safety':('Household / Member Status','Saved Safety Status / History'),
      '05_alerts':('Alert History Request','Disaster Alert / Instructions') if system!='web' else ('Disaster Alert Instructions','OneSignal Delivery Status'),
      '06_monitoring':('Map / Monitoring Filters','Household / Weather Overview'),
      '07_dispatch':('Assignment / Progress Details','Assigned Mission / Route') if system=='rescuer' else ('Team / Dispatch Instructions','Dispatch / Team Progress'),
      '08_assessment':('Member / Damage Findings','Saved Field Report') if system=='rescuer' else ('Field Report Filters','Rescuer Field Findings'),
      '09_navigation':('Evacuation Route Request','Available Evacuation Route') if system=='household' else ('Mission / Location Details','Mission Route / Trip History'),
      '10_radio':('Voice Clip / Channel Choice','Team Voice Recordings'),
      '11_requests':('Logistics Request Details','Own Logistics Request Status') if system=='rescuer' else ('Resource Review Decision','Request / Handoff Status'),
      '12_reports':('Report Scope / Release Decision','Situation Report / Export File'),
    }
    return labels[key]


def dataflow(c,s):
    d=make(c,s,4);mods=s['modules'];systems=system_set(c,s);row_h=196
    if s['compact']:
        groups=[('Account','Manage Accounts',[0,1]),('Household','Track Household Status',[2,3]),('Rescue','Dispatch Rescue Teams',[6,7,8,9]),('Request','Handle Resource Requests',[10]),('Alert','Deliver Alerts / Weather Data',[4,5]),('Report','Generate Operational Reports',[11])]
        mods=[{'key':'compact'+str(i),'title':name,'diagram_label':label,'cases':[key for j in indexes for key in c['modules'][j]['cases']],'providers':list(dict.fromkeys(provider for j in indexes for provider in c['modules'][j]['providers']))} for i,(name,label,indexes) in enumerate(groups)]
    base_y=156;process_x=784 if len(systems)>1 else 624
    for i,m in enumerate(mods):
        relevant=[system for system in systems if any(system in c['functions'][key]['systems'] for key in m['cases'] if key in s['cases'])]
        if not relevant:relevant=systems[:1]
        row_h=max(196,len(relevant)*96+16)
        yy=base_y+(row_h-124)/2;process='process'+str(i);store='store'+str(i)
        d.add(Node(process,process_x,yy,336,124,module_label(c,s,m,True),'dfd','navy','white',18,{'process_id':f'{i+1}.0'}))
        store_labels={'01_access':'Account / Consent Records','02_administration':'Account / Inquiry Records','03_household_setup':'Household Setup Records','04_safety':'Household Safety Records','05_alerts':'Disaster / Delivery Records','06_monitoring':'Household / Weather Records','07_dispatch':'Dispatch / Progress Records','08_assessment':'Rescue Assessment Records','09_navigation':'Route / Trip Records','10_radio':'Radio Clip Metadata','11_requests':'Resource Request Records','12_reports':'Report / Archive Records'}
        store_label='Public Inquiries' if s['role'] and s['role']['actor']=='public' else store_labels.get(m['key'],m['title']+' Records')
        d.add(Node(store,process_x+580,yy+32,328,72,store_label,'store','navy','navy-tint',18,{'store_id':f'D{i+1}'}))
        # Repeated external-entity instances denote the same actor. Local copies
        # eliminate long bundles across unrelated Level-1 process rows.
        for j,system in enumerate(relevant):
            label=s['role']['title'] if s['role'] else 'Household Resident' if system=='household' else 'Rescuer' if system=='rescuer' else 'HQ Staff'
            entity='entity'+str(i)+system;actor_y=base_y+16+j*96
            d.add(Node(entity,100,actor_y,236,80,label,'external',COLOR[system],COLOR[system],18,{'logical_entity':system}))
            incoming,outgoing=dfd_labels(m,system,s['role'])
            incoming_y=actor_y+24;target_y=yy+34+j*20;incoming_channel=process_x-24-j*48
            outgoing_y=yy+104-j*20;return_y=actor_y+64;outgoing_channel=process_x-48-j*48
            d.connect(entity,process,label=incoming,source_side='e',target_side='w',source_offset=incoming_y,target_offset=target_y,via=[(incoming_channel,incoming_y),(incoming_channel,target_y)])
            d.connect(process,entity,label=outgoing,source_side='w',target_side='e',source_offset=outgoing_y,target_offset=return_y,via=[(outgoing_channel,outgoing_y),(outgoing_channel,return_y)])
        d.connect(process,store,label='record changes',color='blue',source_side='e',target_side='w',source_offset=yy+46,target_offset=yy+50)
        d.connect(store,process,label='stored records',color='blue',source_side='w',target_side='e',source_offset=yy+80,target_offset=yy+92)
        if m['providers']:
            key='provider'+str(i);label=' / '.join(m['providers'][:2]);label+='\nProviders' if len(m['providers'])>2 else ''
            d.add(Node(key,process_x+1130,yy+16,256,88,label,'external','slate','slate',18))
            signal=m['key'] in ('05_alerts','07_dispatch')
            d.connect(process,key,label='Notification Payload' if signal else 'Provider Data Request',color='slate',dashed=True,source_side='n',target_side='n')
            d.connect(key,process,label='OneSignal Delivery Status' if signal else 'Requested Provider Data',color='slate',dashed=True,source_side='s',target_side='s')
        base_y+=row_h+32
    return d


def architecture(c,s):
    d=make(c,s,5);systems=system_set(c,s);columns=[100,388,676,1060,1876]
    for x,label in zip(columns,['Users','Apps','API Clients','Laravel API','Data / External']):d.text(x,156,label.upper(),14,'muted',600,group='Containers')
    api_rows=[]
    for system in systems:
        mods=[m for m in s['modules'] if any(system in c['functions'][key]['systems'] for key in m['cases'] if key in s['cases'])]
        if not mods:mods=s['modules']
        api_rows.append((system,mods))
    yy=184
    for system,mods in api_rows:
        if s['compact']:mods=[{'title':'HQ Operations' if system=='web' else 'Household Workflows' if system=='household' else 'Rescuer Workflows','diagram_label':'Scoped Operations'}]
        color=COLOR[system];group_h=96+math.ceil(len(mods)/2)*88;group_key='api'+system
        d.container(columns[3],yy,624,group_h,'HQ Operations · Services/Web' if system=='web' else 'Mobile Field Work · Services/Mobile',color,color+'-tint')
        # The boundary is logical, not a separate deployable microservice.
        d.add(Node(group_key,columns[3],yy,624,group_h,'Scoped Workflow Group','process',color,'white'),False)
        d.raw(f'<g data-api-group="{group_key}">')
        for i,m in enumerate(mods):
            x=columns[3]+20+(i%2)*300;y=yy+48+(i//2)*88
            # Internal module cards are visual children; outer group is the API edge anchor.
            d.raw(f'<rect x="{x}" y="{y}" width="284" height="64" rx="10" fill="{P[color]}" stroke="{P[color]}" stroke-width="1.5"/>');d.center_text(x,y,284,64,module_label(c,s,m),18,'white')
        d.raw('</g>')
        client_y=yy+group_h/2-40;actor_label=s['role']['title'] if s['role'] else 'HQ / Admin' if system=='web' else 'Household Resident' if system=='household' else 'Rescuer'
        actor='user'+system;app='app'+system;transport='transport'+system
        d.add(Node(actor,columns[0],client_y,240,80,actor_label,'primary',color,color,18))
        d.add(Node(app,columns[1],client_y,240,80,'React Web App' if system=='web' else 'Expo Mobile App','primary' if system=='web' else 'split',color,color,18))
        d.add(Node(transport,columns[2],client_y,240,80,'Web API Client' if system=='web' else 'Mobile API Client','primary' if system=='web' else 'split',color,color,18))
        d.connect(actor,app,source_side='e',target_side='w');d.connect(app,transport,source_side='e',target_side='w');d.connect(transport,group_key,label='REST / JSON',source_side='e',target_side='w')
        yy+=group_h+40
    shared_y=yy;d.container(columns[3],shared_y,624,352,'Shared Services · Services/Shared','slate','slate-tint')
    shared=d.add(Node('shared',columns[3],shared_y,624,352,'Authentication and Integrations','process','slate','white'),False)
    labels=['Authentication','Validation / RBAC','Notifications','Partner Adapters','Environment Settings','Provider Status']
    for i,label in enumerate(labels):
        x=columns[3]+20+(i%2)*300;y=shared_y+52+(i//2)*88;d.raw(f'<rect x="{x}" y="{y}" width="284" height="64" rx="10" fill="{P["slate"]}" stroke="{P["slate"]}" stroke-width="1.5"/>');d.center_text(x,y,284,64,label,18,'white')
    db_y=212;d.add(Node('database',columns[4],db_y,320,100,'Active MySQL','database','navy','navy-tint',20))
    d.add(Node('storage',columns[4],db_y+184,320,80,'Files / Jobs / Cache','database','navy','navy-tint',18))
    for system,_ in api_rows:
        d.connect('api'+system,'database',label='R / W',color='blue',source_side='e',target_side='w')
        d.connect('api'+system,'shared',label='service',color='slate',dashed=True,source_side='s',target_side='n')
    d.connect('shared','storage',label='R / W',color='blue',source_side='e',target_side='w',source_offset=shared_y+48)
    providers=list(dict.fromkeys(provider for m in s['modules'] for provider in m['providers']))
    if s['compact'] and providers:providers=['Partner / Provider APIs']
    if providers:
        for i in range(0,len(providers),2):
            key='external'+str(i);y=db_y+348+(i//2)*112
            d.add(Node(key,columns[4],y,320,80,' / '.join(providers[i:i+2]),'external','slate','white',18))
            d.connect('shared',key,label='data',color='slate',dashed=True,source_side='e',target_side='w',source_offset=shared_y+64+(i//2)*48,via=[(1684+24+(i//2)*24,shared_y+64+(i//2)*48),(1684+24+(i//2)*24,y+40)])
    return d


def tech_stack(c,s):
    d=make(c,s,6);systems=system_set(c,s);x=100;y=140;width=1744
    def row(label,chips,color='slate',split=False):
        nonlocal y
        label_w=200 if width>1000 else 168;chip_w=244 if width>1000 else 272;gap=24;per_row=max(1,min(5,int((width-label_w-48+gap)/(chip_w+gap))));nr=max(1,math.ceil(len(chips)/per_row));h=max(112,nr*72+32)
        d.container(x,y,width,h,'',color,'mist')
        if split:
            d.raw(f'<path d="M{x+16} {y}H{x+label_w/2}V{y+h}H{x+16}Q{x} {y+h} {x} {y+h-16}V{y+16}Q{x} {y} {x+16} {y}Z" fill="{P["blue"]}"/><rect x="{x+label_w/2}" y="{y}" width="{label_w/2}" height="{h}" fill="{P["cyan"]}"/>','Containers')
        else:d.raw(f'<path d="M{x+16} {y}H{x+label_w}V{y+h}H{x+16}Q{x} {y+h} {x} {y+h-16}V{y+16}Q{x} {y} {x+16} {y}Z" fill="{P[color]}"/>','Containers')
        d.center_text(x+8,y+8,label_w-16,h-16,label,19,'white',group='Containers')
        key='layer'+str(len(d.nodes));d.add(Node(key,x,y,width,h,label,'process',color,'white'),False)
        for i,chip in enumerate(chips):
            xx=x+label_w+24+(i%per_row)*(chip_w+gap);yy=y+16+(i//per_row)*72
            d.raw(f'<rect x="{xx}" y="{yy}" width="{chip_w}" height="56" rx="10" fill="{P["white"]}" stroke="{P[color]}" stroke-width="1.5"/>');d.center_text(xx,yy,chip_w,56,chip,18)
        old_y=y;y+=h+40;return key,old_y,h
    clients=[];full_width=width;client_top=y;both='web' in systems and any(system in systems for system in ('household','rescuer'))
    if both:width=(full_width-32)/2
    if 'web' in systems:
        chips=['React','Vite','JavaScript','Redux Toolkit','Axios']+(['Leaflet','Laravel Echo'] if any(m['key'] in ('06_monitoring','07_dispatch','10_radio') for m in s['modules']) else [])
        if s['compact']:chips=chips[:3]
        clients.append(row('Web Client',chips,'navy'))
    web_bottom=y
    if any(system in systems for system in ('household','rescuer')):
        if both:x=100+width+32;y=client_top
        chips=['Expo','React Native','TypeScript','Expo Router','Axios','Expo SecureStore']
        if any(m['key']=='09_navigation' for m in s['modules']):chips+=['Expo SQLite','MapLibre React Native']
        if s['compact']:chips=chips[:3]
        clients.append(row('Mobile Client',chips,'blue',split=True))
    x=100;width=full_width;y=max(y,web_bottom)
    backend=row('Backend API',['Laravel','PHP','Laravel Sanctum'] if s['compact'] else ['Laravel','PHP','Laravel Sanctum','Eloquent ORM','Laravel Queues','Laravel Reverb'])
    database=row('Database',['MySQL'])
    providers=list(dict.fromkeys(provider for m in s['modules'] for provider in m['providers']))
    if providers:row('Integrations',providers[:4] if s['compact'] else providers)
    row('Tooling',['Composer','npm','PHPUnit'] if s['compact'] else ['Composer','npm','PHPUnit','ESLint','TypeScript'])
    # Only the runtime layers have arrows; integrations/tooling are inventories.
    for key,cy,ch in clients:d.connect(key,backend[0],source_side='s',target_side='n',target_offset=d.nodes[key].cx)
    d.connect(backend[0],database[0],source_side='s',target_side='n')
    return d


BUILDERS=[erd,use_case,flowchart,swimlane,dataflow,architecture,tech_stack]


def main():
    c=build_catalog();export_catalog(c);manifest=[];errors=[]
    only=sys.argv[1:]  # Optional family IDs for focused regeneration.
    for family,(directory,_) in enumerate(FAMILIES):
        if only and directory not in only:continue
        for s in scopes(c):
            target=OUT/directory/(s['key']+'.svg')
            try:
                diagram=BUILDERS[family](c,s);entry=diagram.save(target);entry['relative']=str(target.relative_to(OUT)).replace('\\','/');entry['scope_title']=s['title'];entry['mode']=s['mode'];entry['functions']=s['cases'];entry['modules']=[m['key'] for m in s['modules']];manifest.append(entry)
                print(f'OK {directory}/{s["key"]}',flush=True)
            except Exception as error:
                errors.append({'family':directory,'scope':s['key'],'error':str(error)});print(f'FAILED {directory}/{s["key"]}: {error}',flush=True)
    old=OUT/'assets/manifest.json'
    if only and old.exists():
        previous=json.loads(old.read_text(encoding='utf-8'));manifest=[e for e in previous if e['family'] not in only]+manifest
    old.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8');(OUT/'assets/build-errors.json').write_text(json.dumps(errors,indent=2),encoding='utf-8')
    print(f'Generated {len(manifest)} diagrams; {len(errors)} failures.',flush=True)
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
